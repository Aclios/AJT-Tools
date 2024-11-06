from pathlib import Path

from ...utils import try_create_dir
from ..plugin import Plugin
from .src import AA4Script, AA56Script

class ScriptPlugin(Plugin):
    help = "AJT script files"
    def __init__(self, script_code : str):
        super().__init__("ScriptPlugin",".user","script")
        assert script_code in ["aa4","aa56"], "Unknown script code"
        self.script_code = script_code

    def export_aa4_file(self, input_filepath : Path, output_filepath : Path):
        script = AA4Script(input_filepath)
        try_create_dir(str(output_filepath))
        script.write_txt(str(output_filepath) + '.txt')

    def export_aa56_file(self, input_filepath : Path, output_filepath : Path):
        script = AA56Script(input_filepath)
        try_create_dir(str(output_filepath))
        script.write_txt(str(output_filepath) + '.txt')

    def export_file(self, input_filepath : Path, output_filepath : Path):
        if self.script_code == 'aa4':
            self.export_aa4_file(input_filepath, output_filepath)
        elif self.script_code == 'aa56':
            self.export_aa56_file(input_filepath, output_filepath)

    def import_aa4_file(self, input_filepath : Path, file_to_import : Path):
        script = AA4Script(file_to_import)
        script.write_user2(input_filepath)

    def import_aa56_file(self, input_filepath : Path, file_to_import : Path):
        script = AA56Script(file_to_import)
        script.write_user2(input_filepath)

    def import_file(self, input_filepath : Path, file_to_import : Path):
        if self.script_code == 'aa4':
            self.import_aa4_file(input_filepath, file_to_import)
        elif self.script_code == 'aa56':
            self.import_aa56_file(input_filepath, file_to_import)

