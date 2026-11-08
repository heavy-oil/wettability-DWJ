#!/usr/bin/env python3
"""Check vendored junyanz CycleGAN trees against recorded upstream blob SHAs.

The trees under CycleGAN/ and pytorch-CycleGAN-and-pix2pix/ are unmodified
snapshots. This script recomputes each Git blob SHA and compares it to
docs/cyclegan-upstream-manifest.txt. It does not download weights or train.
"""

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "cyclegan-upstream-manifest.txt"
LICENSES = (
    "CycleGAN/LICENSE",
    "pytorch-CycleGAN-and-pix2pix/LICENSE",
)
ATTRIBUTION = "Jun-Yan Zhu and Taesung Park"


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    if not MANIFEST.is_file():
        print(f"missing manifest: {MANIFEST}", file=sys.stderr)
        return 1

    mismatches = []
    checked = 0
    for lineno, raw in enumerate(MANIFEST.read_text().splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or len(parts[0]) != 40:
            mismatches.append(f"{MANIFEST.name}:{lineno}: expected '<sha> <path>'")
            continue
        sha, rel = parts
        path = ROOT / rel
        if not path.is_file():
            mismatches.append(f"missing {rel}")
            continue
        got = git_blob_sha1(path.read_bytes())
        checked += 1
        if got != sha:
            mismatches.append(f"mismatch {rel}: {got} != {sha}")

    license_ok = 0
    for rel in LICENSES:
        path = ROOT / rel
        if not path.is_file():
            mismatches.append(f"missing {rel}")
            continue
        if ATTRIBUTION not in path.read_text(errors="replace"):
            mismatches.append(f"license attribution missing in {rel}")
            continue
        license_ok += 1

    if mismatches:
        print("CycleGAN upstream check failed:")
        print("\n".join(mismatches))
        return 1

    print(
        f"OK: {checked} files match the junyanz CycleGAN snapshots; "
        f"{license_ok} LICENSE files attribute {ATTRIBUTION}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
