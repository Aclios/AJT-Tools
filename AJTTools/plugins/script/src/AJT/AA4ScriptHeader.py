class AA4ScriptHeader:
    def __init__(self,f):
        self.datasize = f.readint32() #those 4 bytes are not included in the size
        self.base_offset = f.tell()
        self.entry_count = f.readint32()
        self.abs_offsets = [f.readint32() + self.base_offset for _ in range(self.entry_count)]
