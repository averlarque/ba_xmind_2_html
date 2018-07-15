import xmind
from pathlib import Path
from bs4 import BeautifulSoup


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
            soup = BeautifulSoup(content, 'html.parser')
            # Set a chapter for feature's stories
            feature_stories = feature.addSubTopic()
            feature_stories.setTitle('Истории')
            # Find all h3 tags (we know that only h3 stands for a user story)
            stories = soup.find_all('h3')
            for n in range(len(stories)):
                # Extract particular story title by number
                story_name = soup.find('h3', id='US-'+ str(n+1)).string
                # Set a story title in map
                story_name_map = feature_stories.addSubTopic()
                story_name_map.setTitle(story_name)
                # Extract particular story description by number
                story_description = soup.find('td', id='US-'+ str(n+1)).string
                # Set a story description in map
                story_description_map = story_name_map.addSubTopic()
                story_description_map.setTitle(story_description)
                # Extract user story criteria
                criteria = soup.find('ol', id='US-'+ str(n+1)).contents
                # Iterate through criteria
                for li in criteria:
                    if li != '\n':
                        criteria_map = story_description_map.addSubTopic()
                        criteria_map.setTitle(li.string)
            
            # Set a chapter for feature's functional requirements
            feature_functionals = feature.addSubTopic()
            feature_functionals.setTitle('Функциональные')
            # Find table with functional requirements
            func_table = soup.find(id='func')
            # Get all <tr> within that table
            trs = func_table.find_all('tr')
            # Remove header row
            del trs[0]
            # Iterate through the number of rows
            for n in range(len(trs)):
                f_name = soup.find('td', id='FR-' + str(n+1)).string
                f_name_map = feature_functionals.addSubTopic()
                f_name_map.setTitle(f_name)
                f_body = soup.find('ol', id='FR-'+ str(n+1)).contents
                for li in f_body:
                    if li != '\n':
                        f_li_map = f_name_map.addSubTopic()
                        f_li_map.setTitle(li.string)
    xmind.save(w,"test.xmind") 
            
#test_xmind_file("srs")
parse_html()