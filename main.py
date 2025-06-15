from AJTTools import plugins, REPak, build_pak_from_dir
import argparse
from pathlib import Path
import sys

assert sys.version_info[0] >= 3 and sys.version_info[1] >= 11, f'Invalid Python version: 3.11 or superior is required, current version: {sys.version_info[0]}.{sys.version_info[1]}'

info = {}
lines = open("path_init.txt",'r',encoding='utf-8').readlines()
for line in lines:
    key, value = line.split('=')
    info[key] = value.replace('\n','')

def main():
    parser = argparse.ArgumentParser(
        prog = "AJT Tools",
        description = "REEngine modding tools",
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-e", "--exportf", action="store_true", help="Batch export files")
    mode.add_argument("-i", "--importf", action="store_true", help="Batch import files")

    for command, plugin in plugins.items():
        parser.add_argument(command, help=plugin.help, action='store_true')

    args = parser.parse_args()
    options = vars(args)

    if args.exportf:
        assert not Path(info["extracted_dir"]).exists(), "Delete the extraction folder before exporting files again. This is intended to be a security feature."
        pak = REPak(Path(info["pak_path"]))
        pak.unpack(Path(info["extracted_dir"]), Path(info["release_list_path"]))
        root_dir = list((Path(info["extracted_dir"]) / 'natives').iterdir())[0]
        output_mes = ""
        for name in options:
            if options[name] and name not in ['exportf','importf']:
                plugin = plugins[f"-{name}"]
                if name == 'script':
                    if (root_dir / 'gamedesign' / 'gs4' / 'scriptbinary').exists(): #AJT
                        output_mes += plugin.batch_export_file(root_dir / 'gamedesign' / 'gs4' / 'scriptbinary', Path(plugin.extract_dir_name) / 'gs4' / 'scriptbinary', info["language"])
                        plugin.script_code = "aa56"
                        output_mes += plugin.batch_export_file(root_dir / 'gamedesign' / 'gs5' / 'scriptdata', Path(plugin.extract_dir_name) / 'gs5' / 'scriptdata', info["language"])
                        output_mes += plugin.batch_export_file(root_dir / 'gamedesign' / 'gs6' / 'scriptdata', Path(plugin.extract_dir_name) / 'gs6' / 'scriptdata', info["language"])
                else:
                    output_mes += plugin.batch_export_file(root_dir, Path(plugin.extract_dir_name), info["language"])
        print(output_mes)

    elif args.importf:
        root_dir = list((Path(info["extracted_dir"]) / 'natives').iterdir())[0]
        plat_code = root_dir.name
        mod_dir = Path(info["mod_dir"])
        output_mes = ""
        for name in options:
            if options[name] and name not in ['exportf','importf']:
                plugin = plugins[f"-{name}"]
                if name == 'script':
                    if (root_dir / 'gamedesign' / 'gs4' / 'scriptbinary').exists(): #AJT
                        output_mes += plugin.batch_import_file(root_dir / 'gamedesign' , mod_dir / 'natives' / plat_code / 'gamedesign' , Path(plugin.extract_dir_name) / 'gs4' / 'scriptbinary')
                        plugin.script_code = "aa56"
                        output_mes += plugin.batch_import_file(root_dir / 'gamedesign' , mod_dir / 'natives' / plat_code / 'gamedesign' , Path(plugin.extract_dir_name) / 'gs5' / 'scriptdata')
                        output_mes += plugin.batch_import_file(root_dir / 'gamedesign' , mod_dir / 'natives' / plat_code / 'gamedesign' , Path(plugin.extract_dir_name) / 'gs6' / 'scriptdata')
                else:
                    output_mes += plugin.batch_import_file(root_dir, mod_dir / 'natives' / plat_code, Path(plugin.extract_dir_name))

        build_pak_from_dir(mod_dir, Path(info["patch_pak_path"]))
        print(output_mes)


if __name__ == '__main__':
    main()
