from .....io import LittleEndianBinaryFileReader, LittleEndianBinaryStreamReader, TextFileReader, TextStreamReader, LittleEndianBinaryFileWriter
from .User2Headers import USRHeader, RSZHeader
from .AA4ScriptHeader import AA4ScriptHeader
from .AA4ScriptEntry import AA4ScriptEntry

from pathlib import Path

class AA4Script:
    def __init__(self,filepath : Path):
        if filepath.name.endswith('.txt'):
            self.read_txt(filepath)
        else:
            self.read_user2(filepath)
    
    def read_user2(self,filepath : Path):
        eof_offset = filepath.stat().st_size
        with LittleEndianBinaryFileReader(filepath) as f:
            self.usr_header = USRHeader(f)
            self.rsz_header = RSZHeader(f)
            self.header = AA4ScriptHeader(f)
            self.entries = []
            self.header.abs_offsets.append(eof_offset)
            for idx, offset in enumerate(self.header.abs_offsets[:-1]):
                f.seek(offset)
                data = f.read(self.header.abs_offsets[idx + 1] - offset)
                stream = LittleEndianBinaryStreamReader(data)
                self.entries.append(AA4ScriptEntry(stream,'user2'))

    def read_txt(self,filepath : Path):
        with TextFileReader(filepath,'utf-8') as f:
            end_flag = False
            self.entries : list[AA4ScriptEntry] = []
            _, empty_flag = f.readUntilOccurrenceOrEOF('{')
            if empty_flag:
                return
            while not end_flag:
                data, end_flag = f.readUntilOccurrenceOrEOF('{')
                stream = TextStreamReader(data)
                self.entries.append(AA4ScriptEntry(stream,'txt'))

    def write_txt(self,filepath : Path):
        with open(filepath,mode='w',encoding='utf-8') as f:
            for idx, entry in enumerate(self.entries):
                entry.write_to_txt(f,idx)

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
            f.writeint32(2)
            f.writeint64(0)
            f.writeint64(0x34)
            f.writeint64(0x50)
            f.writeint64(0x50)
            f.writeint64(1)
            f.writeint32(0)
            f.write(b'\x45\x84\xa4\xda\xa2\xda\x12\x52')
            f.pad(16)
            size_pos = f.tell()
            f.writeint32(0)
            f.writeint32(len(self.entries))
            entry_data_offset = 4 * (len(self.entries) + 1)
            for entry in self.entries:
                f.writeint32(entry_data_offset)
                entry_data_offset += entry.getsize()
            for entry in self.entries:
                f.write(entry.byte_data)
            eof_offset = f.tell()
            f.seek(size_pos)
            f.writeint32(eof_offset - size_pos - 4)