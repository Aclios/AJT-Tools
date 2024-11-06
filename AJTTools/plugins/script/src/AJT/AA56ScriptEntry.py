from .....utils import multiple_replace, relative_path
from .....io import LittleEndianBinaryFileReader, TextFileReader, LittleEndianBinaryFileWriter
import json

class AA56ScriptEntry:
    def __init__(self,type : str,f : LittleEndianBinaryFileReader | TextFileReader):
        if type == 'user2':
            self.read_user2(f)
        elif type == 'txt':
            self.read_txt(f)

    def read_user2(self,f : LittleEndianBinaryFileReader):
        self.label_size = f.readint32()
        self.label = f.readstring('utf-16',self.label_size * 2)[:-1]
        f.align(4)
        self.data_size = f.readint32()
        self.data = f.readstring('utf-16',self.data_size * 2)[:-1]
        f.align(4)

    def read_txt(self,f : TextFileReader):
        self.label = f.readUntilOccurrence('}')
        self.data, self.last_entry_flag  = f.readUntilOccurrenceOrEOF('{')
        self.data = self.normalize_data()

    def format_data(self) -> str:
        with open(relative_path(__file__,'aa56_codes_formatting.json'),'r',encoding='utf-8') as f:
            rep_base = json.load(f)
        rep = {}
        rep['<PAGE>'] = '<PAGE>\n' #formatting
        rep['\r\n'] = '<b>\n' #more convenient CR
        rep['<XXXX MSG,'] = '\n<MSG,' #formatting
        for k, v in rep_base.items():
            rep[f'<{k}>'] = f'<{v}>'
            rep[f'<{k},'] = f'<{v},'
        return multiple_replace(self.data,rep)
    
    def normalize_data(self) -> str:
        with open(relative_path(__file__,'aa56_codes_formatting.json'),'r',encoding='utf-8') as f:
            rep_base = json.load(f)
        rep_base = {k:v for v,k in rep_base.items()}
        rep = {}
        rep['\n'] = ''
        rep['\r'] = ''
        rep['<b>'] = '\r\n'
        for k, v in rep_base.items():
            rep[f'<{k}>'] = f'<{v}>'
            rep[f'<{k},'] = f'<{v},'
        rep['<MSG,'] = '<XXXX MSG,'
        return multiple_replace(self.data,rep)

    def write_to_txt(self,f):
        f.write("{" + self.label + "}\n\n")
        f.write(self.format_data() + '\n\n')

    def write_to_user2(self,f : LittleEndianBinaryFileWriter):
        label_bytes = (self.label + '\x00').encode('utf-16')[2:]
        self.label_size = len(label_bytes) // 2
        data_bytes = (self.data + '\x00').encode('utf-16')[2:]
        self.data_size = len(data_bytes) // 2
        f.writeint32(self.label_size)
        f.write(label_bytes)
        f.pad(4)
        f.writeint32(self.data_size)
        f.write(data_bytes)
        f.pad(4)