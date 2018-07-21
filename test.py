import xmind
from pathlib import Path
import requests
from config import *
from classes import Parser


def test_xmind_file(name):
    # Load .xmind file
    file_path = Path.cwd().joinpath(name + '.xmind') 
    print(file_path)
    w = xmind.load(file_path)
    # Load firt (primary sheet)
    sheet=w.getPrimarySheet()
    # Get root topic
    root = sheet.getRootTopic()
    print(root.getTitle())

def parse_html():
    path = Path.cwd().joinpath("output")
    # Load xmind file to write
    w = xmind.load('test.xmind')
    s1 = w.createSheet()
    r1 = s1.getRootTopic()
    r1.setTitle('SRS')
    for s in path.iterdir():
        path_section = s
        # Set a section in map
        section = r1.addSubTopic()
        section.setTitle(s.name)
        for l in path_section.iterdir():
            # Set a feature in map
            feature = section.addSubTopic()
            feature.setTitle(l.stem)
            with l.open() as f:
                content = f.read()
            Parser(feature, content).html_to_xmind()
    xmind.save(w,"test.xmind") 
            

def get_wiki_page(url):
    r = requests.get(url, auth=(wiki_user, wiki_password))
    body = r.text
    w = xmind.load('test.xmind')
    s1 = w.getPrimarySheet()
    r1 = s1.getRootTopic()
    # r1.setTitle('SRS')
    feature = r1.addSubTopic()
    feature.setTitle('Some Feature')
    Parser(feature, body).html_to_xmind()
    xmind.save(w,"test.xmind") 

# test_xmind_file("srs")
# parse_html()
# get_wiki_page(test_url)