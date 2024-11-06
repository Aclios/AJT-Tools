from pathlib import Path

from .src import Tex
from ..plugin import Plugin
from ...utils import try_create_dir

class TexPlugin(Plugin):
    help = "Texture (.tex) files"
    def __init__(self):
        super().__init__("TexPlugin",".tex","tex")

    def export_file(self, input_filepath : Path, output_filepath : Path):
        tex = Tex(input_filepath)
        try_create_dir(str(output_filepath))
        tex.to_png(str(output_filepath) + '.png')

    def import_file(self, input_filepath : Path, file_to_import : Path):
        tex = Tex(input_filepath)
        tex.import_file(file_to_import)
        tex.save(input_filepath)