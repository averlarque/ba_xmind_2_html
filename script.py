import xmind
from classes import UserStory, FuncRequirements
from pathlib import Path


def get_user_stories(feature):
    """
    param: xmind.core.topic.TopicElement object
    return: list
    Supportive function to transform user stories from xmind to html layout
    """
    # Create list for output
    result = []
    # Get feature's index
    feature_index = feature.getIndex()
    # Get through label identifying user stories
    user_stories = feature.getSubTopicByIndex(0)
    # Check if not empty, else return empty list
    if user_stories:
        # Get list of stories' titles
        stories = user_stories.getSubTopics()
        # Itetare through each story and create data structure
        for story in stories:
            description = story.getSubTopicByIndex(0)
            user_story = {
                "feature_index": feature_index,
                "story_index": story.getIndex(),
                "title": story.getTitle(),
                "description": description.getTitle(),
                "criteria": [x.getTitle() for x in description.getSubTopics()]
            }
            # Call UserStory class, pass a story and transform it to layout
            result.append(UserStory(user_story).create_layout())
    return result
       
def get_func_reqs(feature):
    """
    param: xmind.core.topic.TopicElement object
    return: str
    Supportive function to transform functional requirements from xmind to html layout
    """
    # Create list for reqs
    reqs = []
    # Get feature's index
    feature_index = feature.getIndex()
    # Get through label identifying functional requirements
    functionals = feature.getSubTopicByIndex(1)
    # check in not empty, else return an empty list
    if functionals:
        # Get list of freqs' titles
        func_reqs = functionals.getSubTopics()
        # Itetare through each frequirement and create data structure
        for f in func_reqs:
            func_req = {
                "feature_index": feature_index,
                "func_index": f.getIndex(),
                "func_title": f.getTitle(),
                "description": [x.getTitle() for x in f.getSubTopics()]
            }
            reqs.append(func_req)
        # Call FuncRequirement class, pass a list of reqs and transform it to layout
        return FuncRequirements(reqs).create_layout()
    else:
        return reqs

def generate_features(name, section_index=0):
    # Load required Path
    path_output = Path.cwd().joinpath('output')
    Path(path_output).mkdir(exist_ok=True)
    file_path = Path.cwd().joinpath(name + '.xmind')
    # Load .xmind file
    w = xmind.load(file_path)
    # Load firt (primary sheet)
    sheet=w.getPrimarySheet()
    # Get root topic
    root = sheet.getRootTopic()
    # Get required section
    section = root.getSubTopicByIndex(section_index)
    # Create folder for a section to keep features
    section_name = section.getTitle()
    section_folder_path = path_output.joinpath(section_name)
    Path(section_folder_path).mkdir(exist_ok=True) 
    # Extract features and start iterating
    features = section.getSubTopics()

    for feature in features:
        feature_name = str(feature.getIndex() + 1) + '.' + feature.getTitle()
        output = '<h2>Пользовательские истории</h2>'
        stories = get_user_stories(feature)
        for story in stories:
            output += story
        output += '<h2>Функциональные требования</h2>'
        func_reqs = get_func_reqs(feature)
        output += str(func_reqs)
        # Write output in a file
        with open(section_folder_path.joinpath(feature_name + '.txt'), 'w') as f:
            f.write(output)
                  
generate_features("srs", section_index=1)