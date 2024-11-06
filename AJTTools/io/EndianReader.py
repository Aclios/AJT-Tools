import struct
from io import BytesIO

class LittleEndianBinaryFileReader:
    def __init__(self,filepath : str):
        self.filepath = filepath

    def __enter__(self):
        self.file = open(self.filepath,mode='rb')
        self.read = self.file.read
        self.tell = self.file.tell
        self.seek = self.file.seek
        return self

    def __exit__(self,exc_type, exc_val, exc_tb):
        self.file.close()

    def readint8(self) -> int:
        return struct.unpack(f'<b',self.read(1))[0]

    def readuint8(self) -> int:
        return struct.unpack('<B',self.read(1))[0]

    def readint16(self) -> int:
        return struct.unpack('<h',self.read(2))[0]
    
    def readuint16(self) -> int:
        return struct.unpack('<H',self.read(2))[0]

    def readint32(self) -> int:
        return struct.unpack('<i',self.read(4))[0]
    
    def readuint32(self) -> int:
        return struct.unpack('<I',self.read(4))[0]

    def readint64(self) -> int:
        return struct.unpack('<q',self.read(8))[0]

    def readstring(self,encoding,size) -> str:
        return self.read(size).decode(encoding)

    def align(self,alignment):
        mod = self.tell() % alignment
        if mod != 0:
            self.read(alignment - mod)



class LittleEndianBinaryStreamReader:
    def __init__(self,stream : bytes):
        self.stream = BytesIO(stream)
        self.read = self.stream.read
        self.tell = self.stream.tell
        self.seek = self.stream.seek
        self.getvalue = self.stream.getvalue

    def readint8(self) -> int:
        return struct.unpack(f'<b',self.read(1))[0]

    def readuint8(self) -> int:
        return struct.unpack('<B',self.read(1))[0]

    def readint16(self) -> int:
        return struct.unpack('<h',self.read(2))[0]
    
    def readuint16(self) -> int:
        return struct.unpack('<H',self.read(2))[0]

    def readint32(self) -> int:
        return struct.unpack('<i',self.read(4))[0]