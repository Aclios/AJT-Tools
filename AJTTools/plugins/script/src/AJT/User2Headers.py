from .....io import LittleEndianBinaryFileReader

class USRHeader:
    def __init__(self,f : LittleEndianBinaryFileReader):
        self.magic = f.read(4)
        if self.magic != b'USR\x00':
            raise IncorrectMagicError(f'Expected "USR\\x00", read {self.magic}')
        f.readint32()
        self.entry_count = f.readint64()
        self.size = f.readint64()
        self.size2 = f.readint64()
        self.rsz_offset = f.readint64()
        f.readint64()

class RSZHeader:
    def __init__(self,f : LittleEndianBinaryFileReader):
        self.magic = f.read(4)
        if self.magic != b'RSZ\x00':
            raise IncorrectMagicError(f'Expected "RSZ\\x00", read {self.magic}')
        self.unk1 = f.readint32() #0x10
        self.unk2 = f.readint32() #0x01
        self.entry_count = f.readint32() - 2
        f.readint64()
        self.unk3 = f.readint64() #0x34
        self.size = f.readint64()
        self.size2 = f.readint64()
        self.extdata_count = f.readint64()
        f.readint32()
        f.read(8 * self.extdata_count)
        f.align(16)

class IncorrectMagicError(Exception):
    pass