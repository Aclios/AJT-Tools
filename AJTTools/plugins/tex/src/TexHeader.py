from ....io import LittleEndianBinaryFileReader, LittleEndianBinaryFileWriter
from .Formats import getformat

platforms = {
    -1  : 'stm',
    1   : 'nsw',
    0xd : 'ps4',
}

class TexHeader:
    def __init__(self,f : LittleEndianBinaryFileReader):
        self.magic : bytes = f.read(4)
        if self.magic != b'TEX\x00':
            raise Exception(f'Error: Invalid magic ; expected "TEX\x00", got {self.magic}')
        self.version = f.readint32()
        self.width = f.readuint16()
        self.height = f.readuint16()
        self.unk1 = f.readint16() #always 01 00 ?
        self.img_count = f.readuint8()
        assert self.img_count == 1, "Image Count > 1 isn't supported"
        chunk = f.readuint8()
        self.mipmap_count = chunk // 16
        self.unk2 = chunk % 16 # always 0 ?
        self.format_id = f.readint32()
        self.tex_format = getformat(self.format_id)
        self.platform_id = f.readint32()
        self.platform = platforms[self.platform_id]
        self.unk3 = f.readint32() # always 0 ?
        self.unk4 = f.readint32() #change depending on the textures ; truly unknown
        self.nsw_swizzle_mode = f.readint32()
        self.nsw_swizzle_flags = f.readint32() #no idea what those are

    def write(self,f : LittleEndianBinaryFileWriter):
        f.write(self.magic)
        f.writeint32(self.version)
        f.writeuint16(self.width)
        f.writeuint16(self.height)
        f.writeint16(self.unk1)
        f.writeuint8(self.img_count)
        f.writeuint8(self.mipmap_count * 16 + self.unk2)
        f.writeint32(self.format_id)
        f.writeint32(self.platform_id)
        f.writeint32(self.unk3)
        f.writeint32(self.unk4)
        f.writeint32(self.nsw_swizzle_mode)
        f.writeint32(self.nsw_swizzle_flags)