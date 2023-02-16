import xm_maker

seed = int.from_bytes("aretadou".encode('utf-8'), byteorder='little')

def random():
        global seed
        a = 1664525
        c = 1013904223
        m = 2**32
        seed = (a * seed + c) % m
        return seed

def gerate_image(height = 16,width = 16):
    return [(random()%(2**width)).to_bytes(4, byteorder='little') for i in range(height)]

def to_bmp(image, height = 16,width = 16):
    return (b"BM" +
            (height*width+0x20).to_bytes(4, byteorder='little')+
            b"\x00\x00\x00\x00\x20\x00\x00\x00\x0C\x00\x00\x00" +
            width.to_bytes(2, byteorder='little') +
            height.to_bytes(2, byteorder='little') +
            b"\x01\x00\x01\x00\xff\xff\xff\x00\x00\x00" +
            b"".join(image))


with open('benzaiten.bmp', 'wb') as f:
    image = gerate_image()
    f.write(to_bmp(image))
    music = []
    for i in image:
        notes = int.from_bytes(i, byteorder='little')
        music.append(notes & 0xf)
        music.append((notes >> 4) & 0xf)
        music.append((notes >> 8) & 0xf)
    xmfile = xm_maker.XMCreator("benzaiten.xm")
    pattern = xmfile.XMpattern(len(music),8)
    pattern.transform(music)
    xmfile.add_pattern(pattern)
    xmfile.write()