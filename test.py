import xmind
from pathlib import Path

path = Path.cwd().joinpath("assets").joinpath('input')


def test_xmind_file(name):
    # Load .xmind file
    file_path = path.joinpath(name + '.xmind') 
    print(file_path)
    w = xmind.load(file_path)
    # Load firt (primary sheet)
    sheet=w.getPrimarySheet()
    # Get root topic
    root = sheet.getRootTopic()
    print(root.getTitle())


test_xmind_file("srs")