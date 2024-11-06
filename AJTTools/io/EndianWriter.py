import struct

class LittleEndianBinaryFileWriter:
    def __init__(self,filepath : str):
        self.filepath = filepath

    def __enter__(self):
        self.file = open(self.filepath,mode='wb')
        self.write = self.file.write
        self.tell = self.file.tell
        self.seek = self.file.seek
        return self

    def __exit__(self,exc_type, exc_val, exc_tb):
        self.file.close()

    def writeint8(self,value: int):
        self.file.write(struct.pack('<b',value))

    def writeuint8(self,value: int):
        self.file.write(struct.pack('<B',value))

    def writeint16(self,value: int):
        self.file.write(struct.pack('<h',value))
    
    def writeuint16(self,value: int):
        self.file.write(struct.pack('<H',value))

    def writeint32(self,value: int):
        self.file.write(struct.pack('<i',value))

    def writeuint32(self,value: int):
        self.file.write(struct.pack('<I',value))

    def writeint64(self,value: int):
        self.file.write(struct.pack('<q',value))

    def pad(self,alignment: int):
        mod = self.tell() % alignment
        if mod != 0:
            self.write(bytes(alignment - mod))