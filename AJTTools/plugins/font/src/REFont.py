from pathlib import Path

class REFont:
    def __init__(self, filepath : Path):
        with open(filepath,'rb') as f:
            self.magic = f.read(4)
            self.data = f.read()
    
    def _crypt(self, data : bytes | bytearray) -> bytearray:
        newdata = bytearray()
        seed = 1
        delta = 0xAE6E39B58A355F45
        size = len(data) & 0x3F
        if size > 0:
            for _ in range(size):
                seed = 2 * seed + 1
        intkey = (delta >> size) | ((seed & delta) << (64 - size))
        if len(data) > 0:
            intkey = intkey & 0xffffffffffffffff
            key = intkey.to_bytes(8,'little')
            for idx in range(len(data)):
                value = key[idx % 8] ^ data[idx]
                newdata += value.to_bytes(1,'little')
        return newdata
    
    def export_file(self, output_filepath : Path):
        decrypted_data = self._crypt(self.data)
        open(output_filepath,'wb').write(decrypted_data)

    def import_file(self, font_filepath : Path):
        newdata = open(font_filepath,'rb').read()
        self.data = self._crypt(newdata)

    def save(self, filepath : Path):
        with open(filepath,'wb') as f:
            f.write(self.magic)
            f.write(self.data)

