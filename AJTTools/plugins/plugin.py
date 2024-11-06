from pathlib import Path
import traceback
import shutil

from ..utils import should_export, try_create_dir

class Plugin:
    def __init__(self, name: str, fileext : str, extract_dir_name : str):
        self.name = name
        self.fileext = fileext
        self.extract_dir_name = extract_dir_name

    def export_file(self, input_filepath : Path, output_filepath : Path):
        raise Exception("Unimplemented export function")

    def import_file(self, input_filepath : Path, file_to_import : Path):
        raise Exception("Unimplemented import function")

    def batch_export_file(self, root_dir : Path, output_dir : Path, langext : str):
        log = ""
        success = 0
        failure = 0
        try_create_dir(output_dir)
        for abs_path in root_dir.rglob("*"):
            if should_export(abs_path, self.fileext, langext):
                print(f"Exporting {abs_path}...")
                try:
                    export_path = output_dir / abs_path.relative_to(root_dir)
                    self.export_file(abs_path, export_path)
                    success += 1

                except KeyboardInterrupt:
                    raise KeyboardInterrupt("")
                
                except:
                    print(f"An error occured while trying to export {abs_path}")
                    log += f"Error for file {abs_path}\n\n"
                    log += traceback.format_exc()
                    log += ('-' * 140) + '\n\n'
                    failure += 1

        if log != "":
            with open('log.txt', mode='a',encoding='utf-8') as f:
                f.write(log)

        output_mes = f"{self.name}: {success + failure} files treated, with {success} successes and {failure} errors.\n"
        if failure != 0:
            output_mes += 'See the log.txt file for details about the errors.\n'
        return output_mes

    def batch_import_file(self, root_dir : Path, mod_dir : Path, files_dir : Path):
        log = ""
        success = 0
        failure = 0
        for abs_path in files_dir.rglob("*"):
            if not abs_path.is_dir():
                print(f"Importing {abs_path}...")
                root_dir_filepath = root_dir / abs_path.with_suffix('').relative_to(self.extract_dir_name)
                mod_dir_filepath = mod_dir / abs_path.with_suffix('').relative_to(self.extract_dir_name)
                try:
                    if not mod_dir_filepath.exists():
                        try_create_dir(mod_dir_filepath)
                        shutil.copy(root_dir_filepath, mod_dir_filepath)

                    self.import_file(mod_dir_filepath,abs_path)
                    success += 1

                except KeyboardInterrupt:
                    raise KeyboardInterrupt("")
                
                except:
                    print(f"An error occured while trying to import {abs_path}")
                    log += f"Error for file {abs_path}\n\n"
                    log += traceback.format_exc()
                    log += ('-' * 20) + '\n\n'
                    failure += 1

        if log != "":
            with open('log.txt', mode='a',encoding='utf-8') as f:
                f.write(log)

        output_mes = f"{self.name}: {success + failure} files treated, with {success} successes and {failure} errors.\n"
        if failure != 0:
            output_mes += 'See the log.txt file for details about the errors.\n'
        return output_mes



