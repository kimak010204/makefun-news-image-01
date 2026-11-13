#!/usr/bin/env python3
"""Entry point for make.fun news-image-01.

Validates the bundled ``image.png`` (a 1024x1024 newspaper front page
summarising the world news of 13 November 2026) and copies it to the
output directory as ``entry.png``.

Pure Python 3.13 standard library. No network access, no randomness,
no clock: the output is a byte-for-byte copy of the bundled image, so
repeated runs are deterministic.
"""

import os
import shutil
import sys

MAX_IMAGE_BYTES = 1 * 1024 * 1024  # 1 MiB competition limit

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message: str) -> "SystemExit":
    """Print a clear error and exit non-zero."""
    print(f"error: {message}", file=sys.stderr)
    return SystemExit(1)


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "image.png")

    if not os.path.isfile(source):
        raise SystemExit(fail(f"bundled image not found: {source}"))

    with open(source, "rb") as handle:
        header = handle.read(len(PNG_MAGIC))
    if header != PNG_MAGIC:
        raise SystemExit(
            fail("bundled image.png is not a valid PNG (bad magic bytes)")
        )

    size = os.path.getsize(source)
    if size == 0:
        raise SystemExit(fail("bundled image.png is empty (0 bytes)"))
    if size > MAX_IMAGE_BYTES:
        raise SystemExit(
            fail(
                f"bundled image.png is {size} bytes, "
                f"over the {MAX_IMAGE_BYTES} byte limit"
            )
        )

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, "entry.png")

    try:
        shutil.copyfile(source, destination)
    except OSError as exc:
        raise SystemExit(fail(f"failed to copy image to {destination}: {exc}"))

    copied = os.path.getsize(destination)
    if copied != size:
        raise SystemExit(
            fail(
                f"output verification failed: entry.png is {copied} bytes, "
                f"expected {size} bytes"
            )
        )

    print(f"wrote {destination} ({copied} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
