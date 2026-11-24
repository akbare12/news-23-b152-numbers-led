#!/usr/bin/env python3
"""Regenerate entry.png for the news-23 b152 heroes-scene entry.

Stdlib only (no PIL). Validates the source PNG embedded next to this
script, then copies it byte-for-byte to MAKEFUN_OUTPUT_DIR/entry.png.
The output must be byte-identical to the checked-in entry.png.
"""
import hashlib
import os
import struct
import sys
import zlib

# SHA-256 and size of the checked-in entry.png (filled in by revision).
EXPECTED_SHA256 = "38fa72096f95326c8540ef92d0fae561af35909316ad7fa2e84e991ae2946439"
EXPECTED_SIZE = 174449

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def fail(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def read_png(path):
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature in %s" % path)
    if len(data) < 10_000:
        fail("PNG too small: %d bytes" % len(data))
    if len(data) > 1024 * 1024:
        fail("PNG over 1 MiB: %d bytes" % len(data))
    # Chunk walk: length(4) + type(4) + data + CRC(4); CRC covers type+data.
    pos = 8
    first = True
    idat_total = 0
    saw_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header at offset %d" % pos)
        clen, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        if pos + 12 + clen > len(data):
            fail("truncated chunk %r at offset %d" % (ctype, pos))
        chunk_data = data[pos + 8:pos + 8 + clen]
        crc_stored, = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])
        crc_calc = zlib.crc32(ctype + chunk_data) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            fail("CRC mismatch in chunk %r" % ctype)
        if first:
            if ctype != b"IHDR" or clen != 13:
                fail("first chunk must be a 13-byte IHDR")
            w, h, depth, ctype_code, comp, filt, inter = struct.unpack(
                ">IIBBBBB", chunk_data)
            if (w, h) != (1024, 1024):
                fail("expected 1024x1024, got %dx%d" % (w, h))
            if depth != 8:
                fail("expected bit depth 8, got %d" % depth)
            if ctype_code not in (2, 6):
                fail("expected colour type 2 or 6, got %d" % ctype_code)
            if comp != 0 or filt != 0 or inter != 0:
                fail("compression/filter/interlace must all be 0")
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
            saw_iend = True
            break
        pos += 12 + clen
    if not saw_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail("IDAT payload too small: %d bytes" % idat_total)
    return data


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    if os.path.isfile(out_dir):
        fail("MAKEFUN_OUTPUT_DIR is a file: %s" % out_dir)
    repo = os.path.dirname(os.path.abspath(__file__))
    out_dir_abs = os.path.abspath(out_dir)
    if out_dir_abs == repo or out_dir_abs.startswith(repo + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    src = read_png(SOURCE)
    if EXPECTED_SIZE and len(src) != EXPECTED_SIZE:
        fail("source size %d != expected %d" % (len(src), EXPECTED_SIZE))
    digest = hashlib.sha256(src).hexdigest()
    if EXPECTED_SHA256 != "PLACEHOLDER" and digest != EXPECTED_SHA256:
        fail("source sha256 %s != expected %s" % (digest, EXPECTED_SHA256))
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(SOURCE):
        fail("output would overwrite the source image")
    with open(dst, "wb") as f:
        f.write(src)
    with open(dst, "rb") as f:
        back = f.read()
    if back != src:
        fail("re-read output is not byte-identical to source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(back), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
