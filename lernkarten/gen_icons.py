import struct, zlib, sys

def create_png(size, filename):
    pixels = []
    center = size // 2
    margin = size // 5
    for y in range(size):
        row = []
        for x in range(size):
            r, g, b, a = 26, 26, 26, 255
            dx = x - center
            dy = y - center
            dist = (dx*dx + dy*dy) ** 0.5
            radius = size * 0.35
            if dist < radius:
                r, g, b = 201, 168, 76
                lx = x - (center - margin)
                ly = y - (center - margin)
                lsize = size * 0.4
                lwidth = size * 0.1
                if (margin <= lx <= margin + lwidth and ly >= 0 and ly <= lsize) or \
                   (ly >= lsize - lwidth and lx >= 0 and lx <= lsize):
                    r, g, b = 26, 26, 26
            row.extend([r, g, b, a])
        pixels.append(bytes(row))

    def make_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    header = b'\x89PNG\r\n\x1a\n'
    ihdr = make_chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0))
    raw = b''
    for row in pixels:
        raw += b'\x00' + row
    idat = make_chunk(b'IDAT', zlib.compress(raw))
    iend = make_chunk(b'IEND', b'')

    with open(filename, 'wb') as f:
        f.write(header + ihdr + idat + iend)

create_png(192, 'icon-192.png')
create_png(512, 'icon-512.png')
print('Icons created')
