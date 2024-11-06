from .plugins.font import FontPlugin
from .plugins.msg import MSGPlugin
from .plugins.script import ScriptPlugin
from .plugins.sound import SoundPlugin
from .plugins.tex import TexPlugin
from .plugins.pak import REPak, build_pak_from_dir
from .plugins.plugin import Plugin

plugins : dict[str : Plugin] = {
    "-font" : FontPlugin(),
    "-msg" : MSGPlugin('txt','fr'),
    "-script" : ScriptPlugin('aa4'),
    "-sound" : SoundPlugin(),
    "-tex" : TexPlugin()
}