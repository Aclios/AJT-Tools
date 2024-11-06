from ....io import LittleEndianBinaryFileReader, LittleEndianBinaryFileWriter
from .TexHeader import TexHeader
from .TexMipmap import TexMipmap, SteamMipmap, SwitchMipmap, PS4Mipmap
from PIL import Image
from pathlib import Path

mipmap_table = {
    "stm" : SteamMipmap,
    "nsw" : SwitchMipmap,
    "ps4" : PS4Mipmap
}

class Tex:
    def __init__(self,filepath : Path):
        with LittleEndianBinaryFileReader(filepath) as f:
            self.filepath = filepath
            self.header = TexHeader(f)
            Mipmap = mipmap_table[self.header.platform]
            self.mipmaps : list[TexMipmap] = [Mipmap(f, self.header, idx) for idx in range(self.header.mipmap_count)]
                        
            if self.header.platform in ["stm","ps4"]:
                self.header.width = self.mipmaps[0].get_real_width_from_pitch(self.header.tex_format)

            self.image = self.load_pil_image(0)

    def load_pil_image(self, mipmap_idx : int) -> Image.Image:
        return self.mipmaps[mipmap_idx].decode(self.header.width, self.header.height)

    def to_png(self,png_filepath : Path):
        self.image.save(png_filepath)

    def import_file(self, im_filepath : Path):
        self.image : Image.Image = Image.open(im_filepath)
        self.image = self.image.convert(mode='RGBA')
        self.header.width, self.header.height = self.image.size

    def encode_mipmaps(self):
        offset : int = 0x28 + 0x10 * self.header.mipmap_count
        for idx, mipmap in enumerate(self.mipmaps):
            mipmap_im = self.image.reduce(2**idx)
            mipmap.abs_offset = offset
            mipmap.encode(mipmap_im)
            offset += mipmap.data_size
            
    def save(self,tex_filepath : Path):
        self.encode_mipmaps()
        with LittleEndianBinaryFileWriter(tex_filepath) as f:
            self.header.write(f)
            for mipmap in self.mipmaps:
                mipmap.write(f)
            for mipmap in self.mipmaps:
                f.write(mipmap.data)

    def show(self):
        self.image.show()