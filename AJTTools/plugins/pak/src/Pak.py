import mmh3
import zlib
from pathlib import Path

from .PakEntry import PakEntry
from .checksum import calculate_checksum
from ....io import LittleEndianBinaryFileReader, LittleEndianBinaryFileWriter

def readuint(f):
    return int.from_bytes(f.read(4),'little')

def readulong(f):
    return int.from_bytes(f.read(8),'little')

class REPak:
    def __init__(self,filepath : Path):
        with LittleEndianBinaryFileReader(filepath) as f:
            self.filepath = filepath
            self.magic = f.read(4)
            assert self.magic == b'KPKA', "Error: bad magic"
            self.version = f.readuint32()
            #assert self.version == 4, f"Error: unsupported version {self.version} - the only supported version right now is version 4"
            self.entry_count = f.readuint32()
            self.unknown = f.readuint32()
            self.entry_list = [PakEntry(f) for _ in range(self.entry_count)]

    def unpack(self, root_output_dir : Path, release_list_path : Path):
        filepaths = open(release_list_path, mode='r', encoding='utf-8').read().split('\n')
        filehashes = {}
        for filepath in filepaths:
            lowercase_hash, _ = get_mmh3_hashes(filepath)
            filehashes[lowercase_hash] = filepath.lower()
        with open(self.filepath,mode='rb') as f:
            for entry in self.entry_list:
                entry.export(f, root_output_dir, filehashes)


def build_pak_from_dir(dir_path : Path, pak_path : Path):
    files_info = []
    unknown_files_path = dir_path / 'unknown'
    if unknown_files_path.is_dir():
        for file in unknown_files_path.iterdir():
            if not file.is_dir():
                lowercase_path_hash, uppercase_path_hash = str(file).split('.')[0].split('-')
                files_info.append(str(unknown_files_path / file), int(lowercase_path_hash), int(uppercase_path_hash))
    named_files_root = dir_path / 'natives'
    if named_files_root.is_dir():
        for filepath in named_files_root.rglob('*'):
            if not filepath.is_dir():
                gamepath = str("natives" / filepath.relative_to(named_files_root)).replace('\\','/')
                lowercase_hash, uppercase_hash = get_mmh3_hashes(gamepath)
                files_info.append((filepath, lowercase_hash, uppercase_hash))

    with LittleEndianBinaryFileWriter(pak_path) as f:
        f.write(b'KPKA')
        f.writeint32(4)
        entry_count = len(files_info)
        f.writeint32(entry_count)
        f.write(b'FLAG')
        f.write(b'\x00' *(0x30 * entry_count))
        offset = 0x10 + 0x30 * entry_count
        for idx, file_info in enumerate(files_info):
            filepath, lowercase_path_hash, uppercase_path_hash = file_info
            data = open(filepath, 'rb').read()

            compression_name = "none"
            if len(data) >= 8:
                magic1 = int.from_bytes(data[0:4],'little')
                magic2 = int.from_bytes(data[4:8],'little')
                if not (magic1 in [0x75B22630, 0x564D4552, 0x44484B42, 0x4B504B41] or magic2 in [0x70797466]):
                    compression_name = "deflate"
            
            if compression_name == "none":
                compressed_data = data
                compression_flag = 0

            elif compression_name == "deflate":
                compressed_data = zlib.compress(data, wbits = -15)
                compression_flag = 1

            print(f"Adding {filepath} to the pak file (compression:{compression_name})")
            decompressed_size = len(data)
            compressed_size = len(compressed_data)
            #entry.checksum = calculate_checksum(data)
            checksum = 0
            f.seek(0x10 + 0x30*idx)
            f.writeuint32(lowercase_path_hash)
            f.writeuint32(uppercase_path_hash)
            f.writeint64(offset)
            f.writeint64(compressed_size)
            f.writeint64(decompressed_size)
            f.writeint64(compression_flag)
            f.writeint64(checksum)
            f.seek(offset)
            f.write(compressed_data)
            offset = f.tell()

def get_mmh3_hashes(filepath: str):
    lowercase_hash = mmh3.hash(filepath.lower().encode("utf-16-le"), seed = 0xffffffff, signed=False)
    uppercase_hash = mmh3.hash(filepath.upper().encode("utf-16-le"), seed = 0xffffffff, signed=False)
    return lowercase_hash, uppercase_hash
            