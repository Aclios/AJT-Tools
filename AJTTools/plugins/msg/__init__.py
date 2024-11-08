from pathlib import Path

from ...utils import try_create_dir
from ..plugin import Plugin
from .src import exportCSV, exportTXT, exportMSG, exportJson, importCSV, importTXT, importMSG, importJson
from .src.REMSGUtil import SHORT_LANG_LU

class MSGPlugin(Plugin):
    help = "Message data (.msg) files"
    def __init__(self, export_type : str, lang_code : str = None):
        super().__init__("MSGPlugin",".msg","msg")
        assert export_type in ["txt","csv","json"], "export_type should be either 'txt', 'csv', or 'json'"
        if export_type == 'txt':
            assert lang_code in SHORT_LANG_LU or lang_code == 'all', "Invalid language code"
        self.export_type = export_type
        self.lang_code = lang_code

    def export_file(self, input_filepath : Path, output_filepath : Path):
        msg = importMSG(input_filepath)
        try_create_dir(str(output_filepath))
        if self.export_type == 'csv':
            exportCSV(msg, str(output_filepath) + '.csv')
        elif self.export_type == 'txt':
            if self.lang_code != "all":
                exportTXT(msg, str(output_filepath) + '.txt', SHORT_LANG_LU[self.lang_code])
            else:
                raise Exception('txt mode requires a specific language')
        elif self.export_type == 'json':
            exportJson(msg, str(output_filepath) + '.json')

    def import_file(self, msg_filepath : Path, file_to_import : Path):
        msg = importMSG(msg_filepath)
        if self.export_type == 'csv':
            msg = importCSV(msg, file_to_import)
        elif self.export_type == 'txt':
            if self.lang_code != "all":
                msg = importTXT(msg, file_to_import, SHORT_LANG_LU[self.lang_code])
            else:
                raise Exception('txt mode requires a specific language')
        elif self.export_type == 'json':
            msg = importJson(msg, file_to_import)
        exportMSG(msg, msg_filepath)