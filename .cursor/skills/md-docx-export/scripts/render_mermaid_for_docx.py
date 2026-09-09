# .cursor/skills/md-docx-export/scripts/render_mermaid_for_docx.py
"""Prepare markdown for Pandoc DOCX: strip KP path comment, render mermaid → PNG."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
import zlib
from pathlib import Path

FENCE_RE = re.compile(
    r"^```mermaid[^\n]*\n(.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)

PUPPETEER_CFG = Path(__file__).resolve().parent.parent / "assets" / "puppeteer.json"
USER_AGENT = "kp-md-docx-export/1.0"
MMDC_TIMEOUT_S = 180
INK_TIMEOUT_S = 60


def strip_path_comment(text: str) -> str:
    first, _, rest = text.partition("\n")
    if re.match(r"^#\s+.+\.md\s*$", first) and "/" in first:
        return rest.lstrip("\n")
    return text


def mermaid_fences(text: str) -> list[re.Match[str]]:
    return list(FENCE_RE.finditer(text))


def _npx() -> str | None:
    return shutil.which("npx")


def _mmdc() -> str | None:
    return shutil.which("mmdc")


def render_with_mmdc(source: str, png: Path) -> None:
    mmd = png.with_suffix(".mmd")
    mmd.write_text(source.rstrip() + "\n", encoding="utf-8")
    cmd: list[str]
    if _mmdc():
        cmd = [_mmdc()]
    elif _npx():
        cmd = [_npx(), "-y", "-p", "@mermaid-js/mermaid-cli", "mmdc"]
    else:
        raise RuntimeError("neither mmdc nor npx is on PATH")

    cmd += [
        "-i",
        str(mmd),
        "-o",
        str(png),
        "-b",
        "white",
        "-s",
        "2",
        "-e",
        "png",
    ]
    if PUPPETEER_CFG.is_file():
        cmd += ["-p", str(PUPPETEER_CFG)]

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=MMDC_TIMEOUT_S,
        check=False,
    )
    if proc.returncode != 0 or not png.is_file():
        err = (proc.stderr or proc.stdout or "").strip() or f"exit {proc.returncode}"
        raise RuntimeError(f"mmdc failed: {err}")


def _pako_payload(source: str) -> str:
    state = json.dumps(
        {"code": source, "mermaid": {"theme": "base"}, "autoSync": True},
        separators=(",", ":"),
    )
    compressor = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS)
    compressed = compressor.compress(state.encode("utf-8")) + compressor.flush()
    return base64.urlsafe_b64encode(compressed).decode("ascii")


def render_with_mermaid_ink(source: str, png: Path) -> None:
    url = "https://mermaid.ink/img/pako:" + _pako_payload(source) + "?type=png"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=INK_TIMEOUT_S) as resp:
            data = resp.read()
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"mermaid.ink HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"mermaid.ink unreachable: {exc.reason}") from exc
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("mermaid.ink did not return a PNG")
    png.write_bytes(data)


def render_diagram(source: str, png: Path, engine: str) -> str:
    """Return the engine that succeeded."""
    errors: list[str] = []
    order: list[str]
    if engine == "mmdc":
        order = ["mmdc"]
    elif engine == "ink":
        order = ["ink"]
    else:
        order = ["mmdc", "ink"]

    for name in order:
        try:
            if name == "mmdc":
                render_with_mmdc(source, png)
            else:
                render_with_mermaid_ink(source, png)
            return name
        except (RuntimeError, subprocess.TimeoutExpired, OSError) as exc:
            errors.append(f"{name}: {exc}")
            if png.is_file():
                png.unlink()

    raise RuntimeError(" ; ".join(errors))


def replace_mermaid(text: str, img_dir: Path, engine: str) -> tuple[str, int]:
    matches = mermaid_fences(text)
    if not matches:
        return text, 0

    img_dir.mkdir(parents=True, exist_ok=True)
    out = text
    # Replace from the end so offsets stay valid.
    for i, match in enumerate(reversed(matches), start=1):
        n = len(matches) - i + 1
        source = match.group(1).strip()
        digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:12]
        png = img_dir / f"diagram-{n:02d}-{digest}.png"
        used = render_diagram(source, png, engine)
        print(f"  mermaid {n}/{len(matches)} → {png.name} ({used})", file=sys.stderr)
        alt = f"Diagram {n}"
        # 16 cm ≈ content width with 1.5 cm margins on A4.
        image_md = f"![{alt}]({png.as_posix()}){{width=16cm}}"
        out = out[: match.start()] + image_md + out[match.end() :]
    return out, len(matches)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare MD for compact DOCX (mermaid → PNG).")
    parser.add_argument("src", type=Path)
    parser.add_argument("dest", type=Path)
    parser.add_argument("img_dir", type=Path)
    parser.add_argument(
        "--engine",
        choices=("auto", "mmdc", "ink"),
        default=os.environ.get("MERMAID_ENGINE", "auto"),
    )
    args = parser.parse_args()

    text = args.src.read_text(encoding="utf-8")
    text = strip_path_comment(text)
    text, n = replace_mermaid(text, args.img_dir, args.engine)
    args.dest.parent.mkdir(parents=True, exist_ok=True)
    args.dest.write_text(text, encoding="utf-8")
    if n:
        print(f"Rendered {n} mermaid diagram(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 — CLI
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
