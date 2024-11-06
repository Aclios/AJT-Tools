import os
import re
from pathlib import Path

lang_exts = ['ja','en','de','fr','ko','it','es','zhcn','zhtw','ru','pl','nl','pt','ptbr','fi','sv','da','no','cs','hu','sk','ar','tr','bg','el','ro','th','ua','vi','id','cc','hi','es419']

def should_export(filepath : Path, fileext : str, langext : str) -> bool:
    filename = filepath.name
    if not fileext in filename:
        return False
    else:
        if filepath.name.endswith(f".{langext}") or langext == 'all':
            return True
        if filepath.with_name(f"{filename}.{langext}").exists():
            return False
        for ext in lang_exts:
            if filename.endswith(f".{ext}"):
                return False
        return True

def multiple_replace(string,rep):
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], string)

def relative_path(currentpath,relative_path):
    basepath = Path(currentpath).parent
    return (basepath / relative_path).resolve()

def align_size(value,alignment):
    mod = value % alignment
    if mod != 0:
        return value + (alignment - mod)
    return value

def try_create_dir(filepath : str):
    try:
        os.makedirs(os.path.dirname(filepath))
    except:
        pass
