from ....io import LittleEndianBinaryFileReader, LittleEndianBinaryFileWriter

import soundfile as sf
from pathlib import Path


depth_dict = {
    "PCM_16":16,
    "PCM_U8":8,
    "PCM_24":24,
    "PCM_32":32,
    }

sound_format_dict = {
    "WAV":b"wav ",
    "OGG":b"ogg ",
    "AT9":b"at9 "
    }

ext_dict={
    b"wav ":".wav",
    b"ogg ":".ogg",
    b"at9 ":".at9"
    }

class ASRC:
    def __init__(self,filepath : Path,version : int):
        self.version = version
        self.filepath = filepath
        with LittleEndianBinaryFileReader(filepath) as f:
            self.magic = f.read(4)
            if self.magic not in [b'srcd',b'srch']:
                raise Exception('Invalid asrc file (bad magic)')
            self.srch_flag = False
            if self.magic == b'srch':
                self.srch_flag = True
                return
            padding = f.read(4) # 00 00 00 00 ??
            self.audio_filesize = f.readuint32()
            self.format = f.read(4)
            if self.format not in ext_dict:
                raise Exception(f"Error: unsupported audio format: {self.format}")
            self.stream = f.readuint32()
            self.id = f.readuint32()
            if self.version == 31:
                self.unk = f.readuint32()
            self.channels = f.readuint32() #mono = 1, stereo = 2
            self.samples = f.readuint32()
            self.unk_rate = f.readuint32()
            if self.version == 31:
                self.samplerate = f.readuint32()
            self.depth = f.readuint32()
            self.unk1 = f.readuint32()
            self.loop_flag = f.readuint8()
            self.loop_start = f.readuint32()
            self.loop_end = f.readuint32()
            self.key_position_count = f.readuint32()
            self.key_positions = [[f.readuint32(),f.readuint32()] for _ in range(self.key_position_count)]
            padding = f.read(8)
            self.extended_flag = f.readuint8()
            if self.extended_flag:
                self.extended_data = [f.readuint32() for _ in range(5)]
            self.unk2 = f.readuint32()
            self.header_size = f.readuint32()
            self.data_offset = f.readuint32() #????
            f.seek(self.header_size)
            self.data = f.read(self.audio_filesize)
            assert self.data[0:4] in [b"RIFF", b"OggS"], "Error while reading {filepath} - corrupted data"

    def export_file(self,audio_filepath : Path):
        if not self.srch_flag:
            ext = ext_dict[self.format]
            with open(str(audio_filepath) + ext,mode='wb') as f:
                f.write(self.data)

    def import_file(self,audio_filepath : Path):
        format, channels, samplerate, subtype, data = get_audio_file_data(audio_filepath)
        if subtype in depth_dict:
            self.depth = depth_dict[subtype]
        else:
            self.depth = 16 #ogg and at9 seems to only use a 16 bits depth
        self.format = sound_format_dict[format]
        self.channels, self.samplerate, self.audio_filesize, self.data = channels, samplerate, len(data), data

    def save(self,output_filepath : Path):
        with LittleEndianBinaryFileWriter(output_filepath) as f:
            f.write(self.magic)
            f.writeuint32(0)
            f.writeuint32(self.audio_filesize)
            f.write(self.format)
            f.writeuint32(self.stream)
            f.writeuint32(self.id)
            if self.version == 31:
                f.writeuint32(self.unk)
            f.writeuint32(self.channels)
            f.writeuint32(self.samples)
            f.writeuint32(self.unk_rate)
            if self.version == 31:
                f.writeuint32(self.samplerate)
            f.writeuint32(self.depth)
            f.writeuint32(self.unk1)
            f.writeuint8(self.loop_flag)
            f.writeuint32(self.loop_start)
            f.writeuint32(self.loop_end)
            f.writeuint32(self.key_position_count)
            for key_position in self.key_positions:
                f.writeuint32(key_position[0])
                f.writeuint32(key_position[1])
            f.writeint64(0)
            f.writeuint8(self.extended_flag)
            if self.extended_flag:
                for unk in self.extended_data:
                    f.writeuint32(unk)
            f.writeuint32(self.unk2)
            f.writeuint32(self.header_size)
            f.writeuint32(self.data_offset)
            f.write(self.data)

def get_audio_file_data(audio_filepath : Path):
        data = open(audio_filepath,'rb').read()
        if audio_filepath.suffix == '.at9': #try to detect at9
            return "AT9", 2, 48000, "AT9", data
        else:
            with sf.SoundFile(audio_filepath,'r') as f:
                return f.format, f.channels, f.samplerate, f.subtype, data