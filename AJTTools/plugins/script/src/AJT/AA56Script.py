from .....utils import align_size
from .....io import LittleEndianBinaryFileReader, TextFileReader, LittleEndianBinaryFileWriter
from .User2Headers import USRHeader, RSZHeader
from .AA56ScriptEntry import AA56ScriptEntry

from pathlib import Path

class AA56Script:
    def __init__(self,filepath : Path):
        if filepath.name.endswith('.txt'):
            self.read_txt(filepath)
        else:
            self.read_user2(filepath)

    def read_user2(self,filepath : Path):
        with LittleEndianBinaryFileReader(filepath) as f:
            self.usr_header = USRHeader(f)
            self.rsz_header = RSZHeader(f)
            self.entries = [AA56ScriptEntry('user2',f) for _ in range(self.rsz_header.entry_count)]
            self.entry_count = self.rsz_header.entry_count
            self.filename_size = f.readint32()
            self.filename = f.readstring('utf-16',self.filename_size * 2)[:-1]
            f.align(4)
            self.topic_id_count = f.readint32()
            self.topic_ids = [f.readint32() for _ in range(self.topic_id_count)]

    def read_txt(self,filepath : Path):
        with TextFileReader(filepath,'utf-8') as f:
            self.entries = []
            f.readUntilOccurrence("{")
            self.filename = f.readUntilOccurrence('}')
            try:
                f.readUntilOccurrence("{")
            except EOFError: #files with no topic
                self.entry_count = 0
                return
            flag = False
            while not flag:
                entry = AA56ScriptEntry('txt',f)
                flag = entry.last_entry_flag
                self.entries.append(entry)
            self.entry_count = len(self.entries)

    def write_txt(self,filepath : Path):
        with open(filepath,mode='w',encoding='utf-8') as f:
            f.write('{' + self.filename + '}\n\n')
            for entry in self.entries:
                entry.write_to_txt(f)

    def write_user2(self,filepath : Path):
        with LittleEndianBinaryFileWriter(filepath) as f:
            f.write(b'USR\x00')
            f.writeint32(0)
            f.writeint64(0)
            f.writeint64(0x30)
            f.writeint64(0x30)
            f.writeint64(0x30)
            f.writeint64(0)
            f.write(b'RSZ\x00')
            f.writeint32(0x10)
            f.writeint32(1)
            f.writeint32(len(self.entries) + 2)
            f.writeint64(0)
            f.writeint64(0x34)
            rsz_header_size = 0x3c + 8 * (self.entry_count + 1)
            rsz_header_size = align_size(rsz_header_size, 16)
            f.writeint64(rsz_header_size)
            f.writeint64(rsz_header_size)
            f.writeint64(self.entry_count + 1)
            f.writeint32(0)
            for _ in range(self.entry_count):
                f.write(b'\x42\xf0\xf3\x83\x56\x31\x26\x0b')
            f.write(b'\xa7\x3a\x93\xee\xac\xa4\xa1\x1a')
            f.pad(16)
            for entry in self.entries:
                entry.write_to_user2(f)
            self.filename_bytes = (self.filename + '\x00').encode('utf-16')[2:]
            self.filename_size = len(self.filename_bytes) // 2
            f.writeint32(self.filename_size)
            f.write(self.filename_bytes)
            f.pad(4)
            f.writeint32(self.entry_count)
            for idx in range(1,self.entry_count + 1):
                f.writeint32(idx)