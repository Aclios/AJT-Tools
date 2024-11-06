from ....io import LittleEndianBinaryFileReader, LittleEndianBinaryFileWriter
from PIL import Image
from .Formats import TexFormat
from .TexHeader import TexHeader
from pyswizzle import nsw_swizzle, ps4_swizzle, nsw_deswizzle, ps4_deswizzle

class TexMipmap:
    abs_offset : int
    padding : int
    pitch : int
    tex_data_size : int
    data_size : int
    data : bytes
    header : TexHeader

    def get_real_width_from_pitch(self, tex_format : TexFormat) -> int:
        if tex_format.pitch_type == 1: #BC textures
            return (4 * self.pitch) // tex_format.bytes_per_block
        elif tex_format.pitch_type == 2: #R8G8_B8G8, G8R8_G8B8, legacy UYVY-packed, and legacy YUY2-packed formats
            return self.pitch // 4
        elif tex_format.pitch_type == 3:#other formats
            return (self.pitch * 8) // tex_format.bits_per_pixel

    def get_new_pitch_from_width(self, width : int, tex_format : TexFormat) -> int:
        if tex_format.pitch_type == 1:
            return (width * tex_format.bytes_per_block) // 4
        elif tex_format.pitch_type == 2:
            return width * 4
        else:
            return (tex_format.bits_per_pixel * width) // 8
        
class SteamMipmap(TexMipmap):
    def __init__(self, f : LittleEndianBinaryFileReader, header : TexHeader, idx : int):
        self.abs_offset = f.readint32()
        self.padding = f.readint32()
        self.pitch = f.readint32()
        self.data_size = f.readint32()
        pos = f.tell()
        f.seek(self.abs_offset)
        self.data = f.read(self.data_size)
        f.seek(pos)
        self.header = header
        self.idx = idx

    def encode(self, image : Image.Image):
        rgba_data : bytes = image.tobytes()
        encoded_data : bytes = self.header.tex_format.encode(rgba_data,image.width,image.height)
        self.update(encoded_data, image.width)

    def decode(self, width : int, height : int) -> Image.Image:
        decoded_data, pix_order  = self.header.tex_format.decode(self.data, width, height)
        return Image.frombytes('RGBA',(width, height), decoded_data, 'raw', (pix_order))

    def update(self, newdata : bytes, width : int):
        self.data = newdata
        self.data_size = len(newdata)
        self.pitch = self.get_new_pitch_from_width(width, self.header.tex_format)

    def write(self,f : LittleEndianBinaryFileWriter):
        f.writeint32(self.abs_offset)
        f.writeint32(self.padding)
        f.writeint32(self.pitch)
        f.writeint32(self.data_size)

class SwitchMipmap(TexMipmap):
    def __init__(self, f : LittleEndianBinaryFileReader, header : TexHeader, idx : int):
        self.abs_offset = f.readint32()
        self.padding = f.readint32()
        self.tex_data_size = f.readint32() #trailing zeroes are not in the tex file and are added in memory
        self.data_size = f.readint32() #padded (in memory) data size
        pos = f.tell()
        f.seek(self.abs_offset)
        self.data = f.read(self.tex_data_size) + (self.data_size - self.tex_data_size) * b'\x00'
        f.seek(pos)
        self.header = header
        self.idx = idx
        self.nsw_swizzle_mode = self.header.nsw_swizzle_mode - idx #shaky, but works
        
    def encode(self, image : Image.Image):
        width, height = image.size
        swizzle_width, swizzle_height = self.get_swizzle_size(width, height)
        padded_image = Image.new('RGBA',(swizzle_width,swizzle_height))
        padded_image.paste(image)
        rgba_data : bytes = padded_image.tobytes()
        encoded_data : bytes = self.header.tex_format.encode(rgba_data,padded_image.width, padded_image.height)
        swizzled_data = nsw_swizzle(encoded_data, padded_image.size, self.header.tex_format.block_size, self.header.tex_format.bytes_per_block, self.nsw_swizzle_mode)
        self.update(swizzled_data)

    def decode(self, width : int, height : int) -> Image.Image:
        swizzle_width, swizzle_height = self.get_swizzle_size(width, height)
        deswizzled_data = nsw_deswizzle(self.data, (swizzle_width, swizzle_height), self.header.tex_format.block_size, self.header.tex_format.bytes_per_block, self.nsw_swizzle_mode)
        decoded_data, pix_order  = self.header.tex_format.decode(deswizzled_data, swizzle_width, swizzle_height)
        return Image.frombytes('RGBA',(swizzle_width, swizzle_height), decoded_data, 'raw', (pix_order)).crop((0,0,width,height))

    def get_swizzle_size(self, width : int, height : int) ->  tuple[int, int]:  
        chunk_width = 16 // self.header.tex_format.bytes_per_block * self.header.tex_format.block_size[0] * 4
        chunk_height = 8 * self.header.tex_format.block_size[1] * (2 ** self.nsw_swizzle_mode)
        
        if width % chunk_width != 0:
            swizzle_width = ((width // chunk_width) + 1) * chunk_width
        else:
            swizzle_width = width

        if height % chunk_height != 0:    
            swizzle_height = ((height // chunk_height) + 1) * chunk_height
        else:
            swizzle_height = height
            
        return swizzle_width, swizzle_height

    def update(self, newdata : bytes):
        self.data = newdata
        self.data_size = len(newdata)
        self.tex_data_size = self.data_size #not bothering with that bs

    def write(self,f : LittleEndianBinaryFileWriter):
        f.writeint32(self.abs_offset)
        f.writeint32(self.padding)
        f.writeint32(self.tex_data_size)
        f.writeint32(self.data_size)

class PS4Mipmap(TexMipmap):
    def __init__(self,f : LittleEndianBinaryFileReader, header : TexHeader, idx : int):
        self.header = header
        self.abs_offset = f.readint32()
        self.padding = f.readint32()
        self.pitch = f.readint32()
        self.unpadded_data_size = f.readint32() #this datasize weirdly don't take swizzle padding into account... so it's quite useless
        swizzle_width, swizzle_height = self.get_swizzle_size(header.width, header.height) #can't really read lower mipmaps this way... need another solution
        self.data_size = (swizzle_width * swizzle_height // (header.tex_format.block_size[0] * header.tex_format.block_size[1])) * header.tex_format.bytes_per_block #we calculate the real data size
        pos = f.tell()
        f.seek(self.abs_offset)
        self.data = f.read(self.data_size)
        f.seek(pos)
        self.idx = idx

    def encode(self, image : Image.Image):
        width, height = image.size
        swizzle_width, swizzle_height = self.get_swizzle_size(width, height)
        padded_image = Image.new('RGBA',(swizzle_width,swizzle_height))
        padded_image.paste(image)
        rgba_data : bytes = padded_image.tobytes()
        encoded_data : bytes = self.header.tex_format.encode(rgba_data, padded_image.width, padded_image.height)  
        swizzled_data = ps4_swizzle(encoded_data, padded_image.size, self.header.tex_format.block_size, self.header.tex_format.bytes_per_block)
        self.update(swizzled_data, image.width)

    def decode(self, width : int, height : int) -> Image.Image:
        swizzle_width, swizzle_height = self.get_swizzle_size(width, height)
        deswizzled_data = ps4_deswizzle(self.data, (swizzle_width, swizzle_height), self.header.tex_format.block_size, self.header.tex_format.bytes_per_block)
        decoded_data, pix_order  = self.header.tex_format.decode(deswizzled_data, swizzle_width, swizzle_height)
        return Image.frombytes('RGBA',(swizzle_width, swizzle_height), decoded_data, 'raw', (pix_order)).crop((0,0,width,height))

    def get_swizzle_size(self, width : int, height : int) ->  tuple[int, int]: 
        chunk_width = 8 * self.header.tex_format.block_size[0]
        chunk_height = 8 * self.header.tex_format.block_size[1]
        
        if width % chunk_width != 0:
            swizzle_width = ((width // chunk_width) + 1) * chunk_width
        else:
            swizzle_width = width

        if height % chunk_height != 0:    
            swizzle_height = ((height // chunk_height) + 1) * chunk_height
        else:
            swizzle_height = height
            
        return swizzle_width, swizzle_height

    def update(self, newdata : bytes, width : int):
        self.data = newdata
        self.data_size = len(newdata) #Let's hope it'll work that way
        self.pitch = self.get_new_pitch_from_width(width, self.header.tex_format)

    def write(self,f : LittleEndianBinaryFileWriter): 
        f.writeint32(self.abs_offset)
        f.writeint32(self.padding)
        f.writeint32(self.pitch)
        f.writeint32(self.data_size)