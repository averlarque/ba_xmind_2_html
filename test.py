import xmind

def test_xmind_file(path):
    # Load .xmind file
    w = xmind.load(path)
    # Load firt (primary sheet)
    sheet=w.getPrimarySheet()
    # Get root topic
    root = sheet.getRootTopic()
    print(root.getTitle())

test_xmind_file("srs.xmind")