import texture2ddecoder
import etcpak
from astc_encoder import (
 ASTCConfig,
 ASTCContext,
 ASTCImage,
 ASTCProfile,
 ASTCSwizzle,
 ASTCType,
)

class TexFormat:
    bits_per_pixel : int
    bytes_per_block : int
    pitch_type : int
    id : int
    block_size : int

    def encode(self, data : bytes, width :int, height : int) -> bytes:
        pass

    def decode(self, data : bytes, width : int, height : int) -> tuple[bytes,str]:
        pass

class R8G8B8A8_UNORM(TexFormat):
    bits_per_pixel = 32
    bytes_per_block = 4
    pitch_type = 2
    id = 0x1c
    block_size = (1,1)

    def encode(self, data : bytes, width :int, height : int) -> bytes:
        return data

    def decode(self, data : bytes, width : int, height : int) -> tuple[bytes,str]:
        return data, 'RGBA'
    
class R8_UNORM(TexFormat):
    bits_per_pixel = 8
    bytes_per_block = 1
    pitch_type = 3
    id = 0x3d
    block_size = (1,1)

    def encode(self, data : bytes, width : int, height : int) -> bytes:
        enc_data = b""
        for i in range(len(data) // 4):
            enc_data += data[4*i:4*i+1]
        return enc_data
    
    def decode(self, data : bytes, width : int, height : int) -> tuple[bytes,str]:
        dec_data = b""
        for r in data:
            dec_data += r.to_bytes(1,'little') + b'\x00\x00\xff'
        return dec_data, 'RGBA'

class BC1_UNORM(TexFormat):
    bits_per_pixel = 4
    bytes_per_block = 8
    pitch_type = 1
    id = 0x47
    block_size = (4,4)

    def encode(self, data : bytes, width :int, height : int) -> bytes:
        return etcpak.compress_bc1(data, width, height)

    def decode(self, data : bytes, width : int, height : int) -> tuple[bytes,str]:
        return texture2ddecoder.decode_bc1(data, width, height) , 'BGRA'
    
class BC3_UNORM(TexFormat):
    bits_per_pixel = 8
    bytes_per_block = 16
    pitch_type = 1
    id = 0x4d
    block_size = (4,4)

    def encode(self, data : bytes, width :int, height : int) -> bytes:
        return etcpak.compress_bc3(data, width, height)

    def decode(self, data : bytes, width : int, height : int) -> tuple[bytes,str]:
        return texture2ddecoder.decode_bc3(data, width, height) , 'BGRA'
    
class BC4_UNORM(TexFormat):
    bits_per_pixel = 4
    bytes_per_block = 8
    pitch_type = 1
    id = 0x50
    block_size = (4,4)

    def encode(self, data : bytes, width :int, height : int) -> bytes:
        return etcpak.compress_bc4(data, width, height)

    def decode(self, data : bytes, width : int, height : int) -> tuple[bytes,str]:
        return texture2ddecoder.decode_bc4(data, width, height) , 'BGRA'
    
class BC5_UNORM(TexFormat):
    bits_per_pixel = 8
    bytes_per_block = 16
    pitch_type = 1
    id = 0x53
    block_size = (4,4)

    def encode(self, data : bytes, width :int, height : int) -> bytes:
        return etcpak.compress_bc5(data, width, height)

    def decode(self, data : bytes, width : int, height : int) -> tuple[bytes,str]:
        return texture2ddecoder.decode_bc5(data, width, height) , 'BGRA'
    
class BC6H_UF16:
    bits_per_pixel = 8
    bytes_per_block = 16
    pitch_type = 1
    id = 0x5e
    block_size = (4,4)

    def encode(self, data : bytes, width :int, height : int) -> bytes:
        raise Exception("BC6 encode isn't implemented.")

    def decode(self, data : bytes, width : int, height : int) -> tuple[bytes,str]:
        return texture2ddecoder.decode_bc6(data, width, height) , 'BGRA'

class BC7_UNORM(TexFormat):
    bits_per_pixel = 8
    bytes_per_block = 16
    pitch_type = 1
    id = 0x62
    block_size = (4,4)

    def encode(self, data : bytes, width :int, height : int) -> bytes:
        return etcpak.compress_bc7(data, width, height)

    def decode(self, data : bytes, width : int, height : int) -> tuple[bytes,str]:
        return texture2ddecoder.decode_bc7(data, width, height) , 'BGRA'
    
class ASTC_UNORM(TexFormat):
    bytes_per_block = 16
    pitch_type = 1

    def __init__(self,block_width: int, block_height : int):
        self.block_size = (block_width,block_height)
        self.block_width = block_width
        self.block_height = block_height
        self.bits_per_pixel = (self.bytes_per_block * 8) / (self.block_width * self.block_height)
    
    def encode(self, data : bytes, width : int, height : int) -> bytes:
        config = ASTCConfig(ASTCProfile.LDR_SRGB, self.block_width, self.block_height)
        context = ASTCContext(config)
        image = ASTCImage(ASTCType.U8, dim_x = width, dim_y = height, data=data)
        swizzle = ASTCSwizzle()
        comp = context.compress(image, swizzle)
        return comp
    
    def decode(self, data : bytes, width : int, height : int) -> tuple[bytes,str]:
        return texture2ddecoder.decode_astc(data, width, height,self.block_width,self.block_height) , 'BGRA'
    
class ETC2_RGB(TexFormat):
    bytes_per_block = 8
    pitch_type = 1
    block_size = (4,4)
    bits_per_pixel = 4

    def encode(self, data : bytes, width : int, height : int) -> bytes:
        return etcpak.compress_etc2_rgb(data, width, height)

    def decode(self, data : bytes, width : int, height : int) -> tuple[bytes,str]:
        return texture2ddecoder.decode_etc2(data, width, height) , 'BGRA'


formats = {
0x1b:R8G8B8A8_UNORM(),
0x1c:R8G8B8A8_UNORM(),
0x1d:R8G8B8A8_UNORM(),
0x3c:R8_UNORM(),
0x3d:R8_UNORM(),
0x46:BC1_UNORM(),
0x47:BC1_UNORM(),
0x48:BC1_UNORM(),
#0x4a:BC2_UNORM(),
0x4c:BC3_UNORM(),
0x4d:BC3_UNORM(),
0x4e:BC3_UNORM(),
0x4f:BC4_UNORM(),
0x50:BC4_UNORM(),
0x51:BC4_UNORM(),
0x52:BC5_UNORM(),
0x53:BC5_UNORM(),
0x54:BC5_UNORM(),
0x5e:BC6H_UF16(),
0x5f:BC6H_UF16(),
0x61:BC7_UNORM(),
0x62:BC7_UNORM(),
0x63:BC7_UNORM(),
0x0401:ASTC_UNORM(4,4),
0x0402:ASTC_UNORM(4,4),
0x0403:ASTC_UNORM(4,4),
0x0404:ASTC_UNORM(5,4),
0x0405:ASTC_UNORM(5,4),
0x0406:ASTC_UNORM(5,4),
0x0407:ASTC_UNORM(5,5),
0x0408:ASTC_UNORM(5,5),
0x0409:ASTC_UNORM(5,5),
0x040a:ASTC_UNORM(6,5),
0x040b:ASTC_UNORM(6,5),
0x040c:ASTC_UNORM(6,5),
0x040d:ASTC_UNORM(6,6),
0x040e:ASTC_UNORM(6,6),
0x040f:ASTC_UNORM(6,6),
0x0410:ASTC_UNORM(8,5),
0x0411:ASTC_UNORM(8,5),
0x0412:ASTC_UNORM(8,5),
0x0413:ASTC_UNORM(8,6),
0x0414:ASTC_UNORM(8,6),
0x0415:ASTC_UNORM(8,6),
0x0416:ASTC_UNORM(8,8),
0x0417:ASTC_UNORM(8,8),
0x0418:ASTC_UNORM(8,8),
0x0419:ASTC_UNORM(10,5),
0x041a:ASTC_UNORM(10,5),
0x041b:ASTC_UNORM(10,5),
0x041c:ASTC_UNORM(10,6),
0x041d:ASTC_UNORM(10,6),
0x041e:ASTC_UNORM(10,6),
0x041f:ASTC_UNORM(10,8),
0x0420:ASTC_UNORM(10,8),
0x0421:ASTC_UNORM(10,8),
0x0422:ASTC_UNORM(10,10),
0x0423:ASTC_UNORM(10,10),
0x0424:ASTC_UNORM(10,10),
0x0425:ASTC_UNORM(12,10),
0x0426:ASTC_UNORM(12,10),
0x0427:ASTC_UNORM(12,10),
0x0428:ASTC_UNORM(12,12),
0x0429:ASTC_UNORM(12,12),
0x042a:ASTC_UNORM(12,12),
0x043e:ETC2_RGB(),
}

def getformat(id : int) -> TexFormat:
    try:
        return formats[id]
    except KeyError:
        raise Exception(f"Unsupported_format: {unsupported_formats[id]}")

unsupported_formats = {
0x01:"R32G32B32A32_TYPELESS",
0x02:"R32G32B32A32_FLOAT",
0x03:"R32G32B32A32_UINT",
0x04:"R32G32B32A32_SINT",
0x05:"R32G32B32_TYPELESS",
0x06:"R32G32B32_FLOAT",
0x07:"R32G32B32_UINT",
0x08:"R32G32B32_SINT",
0x09:"R16G16B16A16_TYPELESS",
0x0a:"R16G16B16A16_FLOAT",
0x0b:"R16G16B16A16_UNORM",
0x0c:"R16G16B16A16_UINT",
0x0d:"R16G16B16A16_SNORM",
0x0e:"R16G16B16A16_SINT",
0x0f:"R32G32_TYPELESS",
0x10:"R32G32_FLOAT",
0x11:"R32G32_UINT",
0x12:"R32G32_SINT",
0x13:"R32G8X24_TYPELESS",
0x14:"D32_FLOAT_S8X24_UINT",
0x15:"R32_FLOAT_X8X24_TYPELESS",
0x16:"X32_TYPELESS_G8X24_UINT",
0x17:"R10G10B10A2_TYPELESS",
0x18:"R10G10B10A2_UNORM",
0x19:"R10G10B10A2_UINT",
0x1a:"R11G11B10_FLOAT",
0x1e:"R8G8B8A8_UINT",
0x1f:"R8G8B8A8_SNORM",
0x20:"R8G8B8A8_SINT",
0x21:"R16G16_TYPELESS",
0x22:"R16G16_FLOAT",
0x23:"R16G16_UNORM",
0x24:"R16G16_UINT",
0x25:"R16G16_SNORM",
0x26:"R16G16_SINT",
0x27:"R32_TYPELESS",
0x28:"D32_FLOAT",
0x29:"R32_FLOAT",
0x2a:"R32_UINT",
0x2b:"R32_SINT",
0x2c:"R24G8_TYPELESS",
0x2d:"D24_UNORM_S8UINT",
0x2e:"R24_UNORM_X8_TYPELESS",
0x2f:"X24_TYPELESS_G8_UINT",
0x30:"R8G8_TYPELESS",
0x31:"R8G8_UNORM",
0x32:"R8G8_UINT",
0x33:"R8G8_SNORM",
0x34:"R8G8_SINT",
0x35:"R16_TYPELESS",
0x36:"R16_FLOAT",
0x37:"D16_UNORM",
0x38:"R16_UNORM",
0x39:"R16_UINT",
0x3a:"R16_SNORM",
0x3b:"R16_SINT",
0x3e:"R8_UINT",
0x3f:"R8_SNORM",
0x40:"R8_SINT",
0x41:"A8_UNORM",
0x42:"R1_UNORM",
0x43:"R9G9B9E5_SHAREDEXP",
0x44:"R8G8B8G8_UNORM",
0x45:"G8R8G8B8_UNORM",
0x49:"BC2_TYPELESS",
0x4a:"BC2_UNORM",
0x4b:"BC2_UNORM_SRGB",
0x55:"B5G6R5_UNORM",
0x56:"B5G5R5A1_UNORM",
0x57:"B8G8R8A8_UNORM",
0x58:"B8G8R8X8_UNORM",
0x59:"R10G10B10_XRBIASA2_UNORM",
0x5a:"B8G8R8A8_TYPELESS",
0x5b:"B8G8R8A8_UNORM_SRGB",
0x5c:"B8G8R8X8_TYPELESS",
0x5d:"B8G8R8X8_UNORM_SRGB",
0x60:"BC6H_SF16",
0x0400:"VIAEXTENSION",
0x7fffffff:"FORCE_UINT"
}