# AJT-Tools

RE Engine modding tools. Developed specifically for Apollo Justice Trilogy and Ghost Trick. 
Other RE Engine games could be partially supported.

### Supported formats:

Import and export for the following formats are supported:

- Main archive (.pak)
- Textures (.tex)
- Message data (.msg)
- ASRC audio (.asrc)
- Font (.oft)
- Apollo Justice Trilogy script files (.user.2) - AA4, AA5 & AA6

### Supported platforms

The following platforms are supported:

- Android
- Steam
- Nintendo Switch
- PS4

This is only relevant for .tex files, it shouldn't matter for others. Other platforms that don't swizzle textures could be supported.

# Get Started

- Python 3.11 or superior is required.

- Install the required packages by running `python -m pip install -r requirements.txt` in a terminal.

- Fill the path_init.txt with the relevant information. Examples for Apollo Justice Steam are already there.
    - **pak_path** is the path of the main archive of the game, which should be named re_chunk_000.pak
    - **release_list_path** is the path of the release list of the game and platform, which is required to extract files with their real name. You can find release lists of all RE Engine games here: https://github.com/Ekey/REE.PAK.Tool/tree/main/Projects.
    - **extracted_dir** is the path of the folder where all the files of the .pak will be extracted.
    - **mod_dir** is the path of the folder where the modded files will be written. 
    - **patch_pak_path** is the path where the patch pak file will be written. For Steam games, it should be the game folder, for Switch games it can be the mods/contents/<game_id>/romfs of an emulator. This file should be named "re_chunk_000.pak.patch_001.pak". If such files already exist and you want to keep the game updates, name it with the higher id + 1 (If the last update is "re_chunk_000.pak.patch_005.pak", name it "re_chunk_000.pak.patch_006.pak").
    - **language** can be set to a specific language if you don't want to extract files specific to the other languages. By default everything will be extracted ("all").

# How to use

- Run EXPORT.bat to unpack the .pak file and extract all supported assets to their respective folders.

- Sort the files by removing the files you won't have to modify.

- Modify the files and run IMPORT.bat. It will copy the concerned files from the extraction folder to the mod folder, import your modify files, and build the .pak.patch file from them. From now, the files will stay in the mod folder, so if you are satisfied you can remove the assets from their folder to speed up the process.

- If you modified a file that isn't supported by AJT Tools (using a 3rd party tool) and want to add it in your mod, you can just simply put it in the mod folder with its correct path. BUILD PAK ONLY.pak can be used to directly build the .patch.pak file for this case of use case.

# As a python module

AJT Tools can also be used as a Python module.
## Pak files

```python
from AJTTools import REPAk, build_pak_from_dir

#extract a pak file

pak = REPak("path_to_pak")
pak.unpack("output_dir", "release_list_path")

#build a .pak file from a folder

build_pak_from_dir("mod_dir",".pak.patch_file_path")
```

## Font files

```python
from AJTTools.plugins.font import REFont

font = REFont("font.oft.1") # read the file

font.export_file("font.otf") # export

font.import_file("newfont.otf") # import
font.save("font.oft.1") # save
```

## Tex files

```python
from AJTTools.plugins.tex import Tex

tex = Tex("image.tex.35") # read the file

tex.export_file("image.png") # export

tex.import_file("newimage.png") # import
tex.save("image.tex.35") # save
```

## MSG files

```python
from AJTTools.plugins.msg import MSGPlugin

## work with csv files

plugin = MSGPlugin("csv")
plugin.export_file("message.msg.22","message.csv") # export
plugin.import_file("message.msg.22","newmessage.csv") # import/save

## work with json files

plugin = MSGPlugin("json")
plugin.export_file("message.msg.22","message.json") # export
plugin.import_file("message.msg.22","newmessage.json") # import/save

## work with txt files (single language)

plugin = MSGPlugin("txt","en") #init and chose english as export/import language
plugin.export_file("message.msg.22","message.txt") # export
plugin.import_file("message.msg.22","newmessage.txt") # import/save
```

## Audio files (asrc)

```python
from AJTTools.plugins.sound import ASRC

asrc = ASRC("se.asrc.31") # read the file

asrc.export_file("se") # export, extension is added automatically depending on the format

asrc.import_file("newse.wav") # import
asrc.save("se.asrc.31") # save
```

## AJT Script files

```python
from AJTTools.plugins.script import AA4Script, AA56Script

## user.2 to txt

script = AA4Script("script.user.2") #aa4 script
script.write_txt("script.txt") #export

script = AA56Script("script.user.2") #aa5 and aa6 script
script.write_txt("script.txt") #export

## txt to user.2

script = AA4Script("script.txt") #aa4
script.write_user2("script.user.2")

script = AA56Script("script.txt") #aa5 & 6
script.write_user2("script.user.2")
```

# Credits

[REE.PAK.Tool](https://github.com/Ekey/REE.PAK.Tool/tree/main) by Ekey and [retool](https://www.patreon.com/FluffyQuack) by FluffyQuack for file format.

Modules and packages used:

| Package   | Author   | License |
|---      |---    |---   |
| [etcpack](https://github.com/K0lb3/etcpak) | K0lb3 | MIT
| [texture2ddecoder](https://github.com/K0lb3/texture2ddecoder) | K0lb3 | MIT
| [astc-encoder-py](https://github.com/K0lb3/astc-encoder-py) | K0lb3 | MIT
| [REMSG_Converter](https://github.com/dtlnor/REMSG_Converter) | dtlnor | MIT
| [chardet](https://github.com/chardet/chardet) | dan-blanchard | LGPL-2.1
| [mmh3](https://github.com/hajimes/mmh3) | hajimes | MIT
| [Pillow](https://github.com/python-pillow/Pillow) | Jeffrey A. Clark | MIT-CMU
| [soundfile](https://github.com/bastibe/python-soundfile) | bastibe | BSD-3-Clause
| [zstd](https://github.com/sergey-dryabzhinsky/python-zstd) | Sergey Dryabzhinsky, Anton Stuk | BSD-2-Clause