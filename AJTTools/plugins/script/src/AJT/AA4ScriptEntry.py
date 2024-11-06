from .....utils import relative_path
from .....io import TextFileReader, TextStreamReader, LittleEndianBinaryFileWriter, LittleEndianBinaryStreamReader
import json
from typing import Union

with open(relative_path(__file__,'aa4_codes_info.json'),'r',encoding='utf-8') as f:
    CODE_DICT = json.load(f)

REVERSE_CODE_DICT = {v[0]:k for k,v in CODE_DICT.items()}

class AA4ScriptEntry:
    def __init__(self,stream : Union[LittleEndianBinaryStreamReader, TextStreamReader],type:str):
        if type == 'user2':
            self.read_user2(stream)
        elif type == 'txt':
            self.read_txt(stream)

    def read_user2(self,f : LittleEndianBinaryStreamReader):
        self.size = len(f.getvalue())
        self.code_35_diff = []
        self.code_35_values = []
        readbytes = f.read(2)
        self.data = ""
        while readbytes != b'':
            value = int.from_bytes(readbytes,'little')
            if value >= 0xe000 and value < 0xf900:
                newdata = self.parse_user2_code(value,f)
                self.data += newdata
            else:
                self.data += readbytes.decode('utf-16')
            readbytes = f.read(2)
        for value in self.code_35_values:
            self.code_35_diff.append(self.size - value)

    def parse_user2_code(self,value : int,f : LittleEndianBinaryStreamReader) -> str:
        name, arg_count = CODE_DICT[hex(value - 0xe000)]
        if arg_count == 0:
            if name in ["PAGE","b","NEXT","NEXT_AUTO"]: #formatting
                return f'<{name}>\n'
            return f'<{name}>'
        args = [str(f.readuint16()) for _ in range(arg_count)]
        if value == 0xe035: #JUMP using a constant byte pointer, must be updated
            self.code_35_values.append(int(args[1]))
        args_str = ','.join(args)
        if name in ["MSG","MSG_EXAM_PARTNER"]: #formatting
            return f'<{name},{args_str}>\n'
        return f'<{name},{args_str}>'
    
    def read_txt(self,f : TextStreamReader):
        label = f.readUntilOccurrence('}')
        self.code_35_diff = [int(val) for val in label.split('=')[1].split(',')]
        self.code_35_func_value_offsets = []
        end_flag = False
        self.byte_data = bytearray()
        text, end_flag = f.readUntilOccurrenceOrEOFSkipCR('<')
        while not end_flag:
            self.byte_data += text.encode('utf-16')[2:]
            self.byte_data += self.parse_txt_code(f)
            text, end_flag = f.readUntilOccurrenceOrEOFSkipCR('<')
        for idx, offset in enumerate(self.code_35_func_value_offsets):
            code_35_value = self.getsize() - self.code_35_diff[idx]
            self.byte_data = self.byte_data[0:offset] + code_35_value.to_bytes(2,'little') + self.byte_data[offset + 2:] #update the raw jump

    def parse_txt_code(self,f : TextStreamReader) -> bytes:
        code_data = f.readUntilOccurrence('>')
        parsing = code_data.split(',')
        code_value = int(REVERSE_CODE_DICT[parsing[0]],16) + 0xe000
        if len(parsing) == 1:
            return code_value.to_bytes(2,'little')
        else:
            output_data = code_value.to_bytes(2,'little')
            for arg in parsing[1:]:
                output_data += int(arg).to_bytes(2,'little')
            if code_value == 0xe035:
                self.code_35_func_value_offsets.append(self.getsize() + 4) #adding the offset of the values to update
            return output_data

    
    def write_to_txt(self,f,idx):
        if len(self.code_35_diff) == 0:
            offset_35 = 0
        else:
            offset_35 = ','.join(str(offset) for offset in self.code_35_diff)
        f.write("{" + f'{idx},35_offset={offset_35}' + "}\n\n")
        f.write(self.data + '\n\n')

    def getsize(self):
        return len(self.byte_data)