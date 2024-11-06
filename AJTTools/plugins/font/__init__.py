from pathlib import Path

from ...utils import try_create_dir
from ..plugin import Plugin
from .src import REFont

class FontPlugin(Plugin):
    help = "Font (.oft) files"
    def __init__(self):
        super().__init__("FontPlugin",".oft","font")

    def export_file(self, input_filepath : Path, output_filepath : Path):
        font = REFont(input_filepath)
        try_create_dir(str(output_filepath))
        font.export_file(str(output_filepath) + '.otf')

    def import_file(self, input_filepath : Path, file_to_import : Path):
        font = REFont(input_filepath)
        font.import_file(file_to_import)
        font.save(input_filepath)