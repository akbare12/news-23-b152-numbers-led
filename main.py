#!/usr/bin/env python3
"""Render the b152 numbers-led front page and write entry.png.

Stdlib only. Reads entry.png next to this file, validates the PNG header
manually (struct), and writes the verified bytes to
os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png").
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "855a2c0686cb7a171394941cdf39ec6c84aa51fe2c4186f93c574873a2e117d7"
EXPECTED_SIZE = 137223
SRC_NAME = "entry.png"


def fail(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir = os.path.abspath(out_dir)
    if os.path.isfile(out_dir):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    if os.path.commonpath([out_dir, here]) == here and out_dir != here:
        # output dir must not live inside the repo (grader runs read-only)
        if os.path.abspath(out_dir).startswith(here + os.sep):
            fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    dst = os.path.join(out_dir, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        fail("output would overwrite the source image")

    try:
        with open(src, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        fail("cannot read source image: %s" % exc)

    if len(data) < 10000:
        fail("image too small: %d bytes" % len(data))
    if len(data) > 1024 * 1024:
        fail("image over 1 MiB: %d bytes" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")

    # Walk chunks: length(4) + type(4) + data + crc(4); CRC covers type+data.
    pos = 8
    first = True
    idat_total = 0
    seen_iend = False
    while pos + 8 <= len(data):
        (clen,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            fail("truncated chunk %r" % ctype)
        chunk = data[pos + 4:pos + 8 + clen]
        (crc_stored,) = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])
        if zlib.crc32(chunk) & 0xFFFFFFFF != crc_stored:
            fail("CRC mismatch in chunk %r" % ctype)
        if first:
            if ctype != b"IHDR" or clen != 13:
                fail("first chunk must be a 13-byte IHDR")
            w, h, depth, ctype_id, comp, filt, inter = struct.unpack(
                ">IIBBBBB", data[pos + 8:pos + 21])
            if (w, h) != (1024, 1024):
                fail("image must be 1024x1024, got %dx%d" % (w, h))
            if depth != 8 or ctype_id not in (2, 6):
                fail("unsupported PNG: bit depth %d colour type %d" % (depth, ctype_id))
            if comp != 0 or filt != 0 or inter != 0:
                fail("unsupported PNG compression/filter/interlace flags")
            first = False
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be empty")
            if pos + 12 + clen != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            break
        pos += 12 + clen
    if first:
        fail("no IHDR chunk found")
    if not seen_iend:
        fail("no IEND chunk found")
    if idat_total < 1000:
        fail("IDAT payload too small: %d bytes" % idat_total)

    digest = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 != "PLACEHOLDER" and digest != EXPECTED_SHA256:
        fail("sha256 mismatch: got %s" % digest)
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        fail("size mismatch: got %d bytes" % len(data))

    os.makedirs(out_dir, exist_ok=True)
    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        back = fh.read()
    if back != data:
        fail("re-read output does not match source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), digest))


if __name__ == "__main__":
    main()
