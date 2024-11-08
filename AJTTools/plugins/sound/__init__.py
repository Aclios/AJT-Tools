from pathlib import Path

from ...utils import try_create_dir
from ..plugin import Plugin
from .src import ASRC

class SoundPlugin(Plugin):
    help = "Sound clips (.asrc) files"
    def __init__(self):
        super().__init__("SoundPlugin",".asrc","sound")

    def export_file(self, input_filepath : Path, output_filepath : Path):
        version = int(input_filepath.name.split('.')[2])
        sound = ASRC(input_filepath, version)
        if not sound.srch_flag:
            try_create_dir(str(output_filepath))
            sound.export_file(output_filepath)

    def import_file(self, input_filepath : Path, file_to_import : Path):
        version = int(input_filepath.name.split('.')[2])
        sound = ASRC(input_filepath, version)
        if not sound.srch_flag:
            sound.import_file(file_to_import)
            sound.save(input_filepath)