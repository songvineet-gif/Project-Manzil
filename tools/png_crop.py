"""
Minimal pure-stdlib PNG top-left crop.

Headless Chromium's --screenshot renders a window --window-size px tall,
but the actual usable viewport (window.innerHeight) is consistently a
fixed amount shorter than that in this environment -- the missing rows
render as blank space at the bottom of the PNG. The fix used by
social_series_generator.py is to render into a window taller than the
target size, then crop the excess off the bottom with this function.
There is no PIL/ImageMagick in this environment, so this decodes just
enough of the PNG spec (IHDR + IDAT, non-interlaced, 8-bit RGB or RGBA)
to re-filter and re-encode a cropped copy.
"""
import struct
import zlib

_SIG = b"\x89PNG\r\n\x1a\n"


def _chunks(data):
    pos = len(_SIG)
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        cdata = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        yield ctype, cdata


def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def _unfilter(raw, width, height, bpp):
    stride = width * bpp
    out = bytearray(stride * height)
    src_pos = 0
    prev = bytearray(stride)
    for y in range(height):
        ftype = raw[src_pos]
        src_pos += 1
        row = bytearray(raw[src_pos:src_pos + stride])
        src_pos += stride
        for i in range(stride):
            a = row[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if ftype == 0:
                pass
            elif ftype == 1:
                row[i] = (row[i] + a) & 0xFF
            elif ftype == 2:
                row[i] = (row[i] + b) & 0xFF
            elif ftype == 3:
                row[i] = (row[i] + (a + b) // 2) & 0xFF
            elif ftype == 4:
                row[i] = (row[i] + _paeth(a, b, c)) & 0xFF
            else:
                raise ValueError(f"unsupported filter type {ftype}")
        out[y * stride:(y + 1) * stride] = row
        prev = row
    return bytes(out)


def _chunk(ctype, cdata):
    return (
        struct.pack(">I", len(cdata))
        + ctype
        + cdata
        + struct.pack(">I", zlib.crc32(ctype + cdata) & 0xFFFFFFFF)
    )


def crop_top_left(in_path, out_path, out_width, out_height):
    with open(in_path, "rb") as f:
        data = f.read()
    if data[:8] != _SIG:
        raise ValueError("not a PNG file")

    ihdr = None
    idat = bytearray()
    for ctype, cdata in _chunks(data):
        if ctype == b"IHDR":
            ihdr = cdata
        elif ctype == b"IDAT":
            idat += cdata

    width, height, bitdepth, colortype, comp, filt, interlace = struct.unpack(
        ">IIBBBBB", ihdr
    )
    if bitdepth != 8 or interlace != 0:
        raise ValueError("only 8-bit non-interlaced PNGs are supported")
    if colortype == 2:
        bpp = 3
    elif colortype == 6:
        bpp = 4
    else:
        raise ValueError(f"unsupported color type {colortype}")
    if out_width > width or out_height > height:
        raise ValueError("crop size exceeds source image size")

    raw = zlib.decompress(bytes(idat))
    pixels = _unfilter(raw, width, height, bpp)

    stride = width * bpp
    out_stride = out_width * bpp
    cropped = bytearray()
    for y in range(out_height):
        row_start = y * stride
        cropped.append(0)  # filter type 0 (None)
        cropped += pixels[row_start:row_start + out_stride]

    new_idat = zlib.compress(bytes(cropped), 9)
    new_ihdr = struct.pack(
        ">IIBBBBB", out_width, out_height, 8, colortype, comp, filt, interlace
    )

    with open(out_path, "wb") as f:
        f.write(_SIG)
        f.write(_chunk(b"IHDR", new_ihdr))
        f.write(_chunk(b"IDAT", new_idat))
        f.write(_chunk(b"IEND", b""))
