from _obj.tex.format.DDS import *
from _obj.tex.format.ASTC import *

format_dict = {
0x1c:R8G8B8A8_UNORM(),
0x47:BC1_UNORM(),
0x4a:BC2_UNORM(),
0x4d:BC3_UNORM(),
0x50:BC4_UNORM(),
0x53:BC5_UNORM(),
0x5f:BC6H_UF16(),
0x62:BC7_UNORM(),
0x040e:ASTC_6x6_UNORM()
}

'''
All possible formats? Credits: https://github.com/AsteriskAmpersand/MHR_Tex_Chopper
'''
format_dict_completed = {
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
0x1b:"R8G8B8A8_TYPELESS",
0x1c:"R8G8B8A8_UNORM",
0x1d:"R8G8B8A8_UNORM_SRGB",
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
0x3c:"R8_TYPELESS",
0x3d:"R8_UNORM",
0x3e:"R8_UINT",
0x3f:"R8_SNORM",
0x40:"R8_SINT",
0x41:"A8_UNORM",
0x42:"R1_UNORM",
0x43:"R9G9B9E5_SHAREDEXP",
0x44:"R8G8B8G8_UNORM",
0x45:"G8R8G8B8_UNORM",
0x46:"BC1_TYPELESS",
0x47:"BC1_UNORM",
0x48:"BC1_UNORM_SRGB",
0x49:"BC2_TYPELESS",
0x4a:"BC2_UNORM",
0x4b:"BC2_UNORM_SRGB",
0x4c:"BC3_TYPELESS",
0x4d:"BC3_UNORM",
0x4e:"BC3_UNORM_SRGB",
0x4f:"BC4_TYPELESS",
0x50:"BC4_UNORM",
0x51:"BC4_SNORM",
0x52:"BC5_TYPELESS",
0x53:"BC5_UNORM",
0x54:"BC5_SNORM",
0x55:"B5G6R5_UNORM",
0x56:"B5G5R5A1_UNORM",
0x57:"B8G8R8A8_UNORM",
0x58:"B8G8R8X8_UNORM",
0x59:"R10G10B10_XRBIASA2_UNORM",
0x5a:"B8G8R8A8_TYPELESS",
0x5b:"B8G8R8A8_UNORM_SRGB",
0x5c:"B8G8R8X8_TYPELESS",
0x5d:"B8G8R8X8_UNORM_SRGB",
0x5e:"BC6H_TYPELESS",
0x5f:"BC6H_UF16",
0x60:"BC6H_SF16",
0x61:"BC7_TYPELESS",
0x62:"BC7_UNORM",
0x63:"BC7_UNORM_SRGB",
0x0400:"VIAEXTENSION",
0x0401:"ASTC_4x4_TYPELESS",
0x0402:"ASTC_4x4_UNORM",
0x0403:"ASTC_4x4_UNORM_SRGB",
0x0404:"ASTC_5x4_TYPELESS",
0x0405:"ASTC_5x4_UNORM",
0x0406:"ASTC_5x4_UNORM_SRGB",
0x0407:"ASTC_5x5_TYPELESS",
0x0408:"ASTC_5x5_UNORM",
0x0409:"ASTC_5x5_UNORM_SRGB",
0x040a:"ASTC_6x5_TYPELESS",
0x040b:"ASTC_6x5_UNORM",
0x040c:"ASTC_6x5_UNORM_SRGB",
0x040d:"ASTC_6x6_TYPELESS",
0x040e:"ASTC_6x6_UNORM",
0x040f:"ASTC_6x6_UNORM_SRGB",
0x0410:"ASTC_8x5_TYPELESS",
0x0411:"ASTC_8x5_UNORM",
0x0412:"ASTC_8x5_UNORM_SRGB",
0x0413:"ASTC_8x6_TYPELESS",
0x0414:"ASTC_8x6_UNORM",
0x0415:"ASTC_8x6_UNORM_SRGB",
0x0416:"ASTC_8x8_TYPELESS",
0x0417:"ASTC_8x8_UNORM",
0x0418:"ASTC_8x8_UNORM_SRGB",
0x0419:"ASTC_10x5_TYPELESS",
0x041a:"ASTC_10x5_UNORM",
0x041b:"ASTC_10x5_UNORM_SRGB",
0x041c:"ASTC_10x6_TYPELESS",
0x041d:"ASTC_10x6_UNORM",
0x041e:"ASTC_10x6_UNORM_SRGB",
0x041f:"ASTC_10x8_TYPELESS",
0x0420:"ASTC_10x8_UNORM",
0x0421:"ASTC_10x8_UNORM_SRGB",
0x0422:"ASTC_10x10_TYPELESS",
0x0423:"ASTC_10x10_UNORM",
0x0424:"ASTC_10x10_UNORM_SRGB",
0x0425:"ASTC_12x10_TYPELESS",
0x0426:"ASTC_12x10_UNORM",
0x0427:"ASTC_12x10_UNORM_SRGB",
0x0428:"ASTC_12x12_TYPELESS",
0x0429:"ASTC_12x12_UNORM",
0x042a:"ASTC_12x12_UNORM_SRGB",
0x7fffffff:"FORCE_UINT"
}