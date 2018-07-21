from bs4 import BeautifulSoup
import re

class UserStory:
    """Class for storing and transforming user stories"""
    def __init__(self, object):
        self.feature_index = object["feature_index"] + 1
        self.story_index = object["story_index"] + 1
        self.title = object["title"]
        self.description = object["description"]
        self.criteria = object["criteria"]

    def create_layout(self):
        # h2 = '<h2 class="auto-cursor-target">Пользовательские истории</h2> \n'
        h3 = "\n<h3 class='US-{1}'>!N.{0}-US-{1}. {2}</h3>\n".format(self.feature_index, self.story_index, self.title)
        table_open = '<table><colgroup><col /><col /></colgroup> \n <tbody> \n'
        description_row = "<tr> \n <th>Описание</th> \n <td class='US-{1}'>{0}</td></tr> \n".format(self.description, self.story_index)
        criteria = self._iterate_criteria()
        criteria_row = "<tr>\n<th>Критерии приемки</th>\n<td><ol class='US-{1}'>\n{0}</ol></td></tr>".format(criteria, self.story_index)
        uc_row = '\n<tr>\n <th>UC</th>\n<td></td></tr>'
        fc_row = '\n<tr>\n<th>FR</th>\n<td></td></tr>'
        table_close = '\n</tbody></table>\n'

        result = h3 + table_open + description_row + criteria_row + uc_row + fc_row + table_close

        return result
    
    def _iterate_criteria(self):
        result = ''
        for item in self.criteria:
            result += '<li>{}</li>\n'.format(item)
        return result

class FuncRequirements:
    """Class for storing and transforming functional requirements """
    def __init__(self, object):
        self.func_reqs = object

    def _iterate_funcs(self):
        result = ''
        for f in self.func_reqs:
            fe_index = f['feature_index'] + 1
            fu_index = f['func_index'] + 1
            fu_title = f['func_title']
            fu_des = f['description']
            fu_des_items = ''
            for f in fu_des:
                fu_des_items += '<li>{}</li>\n'.format(f)
            result += "<tr>\n<td>!N.{0}-FR-{1}</td>\n<td class='FR-{1}'>{2}</td>\n<td><ol class='FR-{1}'>\n{3}</ol></td>\n</tr>\n".format(fe_index, fu_index, 
            fu_title, fu_des_items)

        return result

    def create_layout(self):
        table_open = "\n<table class='wrapped'><colgroup><col /><col /><col /></colgroup>\n<tbody class='func'>\n"
        header_row = '<tr>\n<th>ID</th>\n<th>Название</th>\n<th>Описание</th>\n</tr>\n'
        freqs = self._iterate_funcs()
        table_close = '</tbody></table>\n'
        result = table_open + header_row + freqs + table_close
        return result

class Parser:
    def __init__(self, xmind_obj, html_content):
        self.xmind_obj = xmind_obj
        self.html_content = html_content

    def html_to_xmind(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        Parser.get_user_stories(self.xmind_obj, soup)
        Parser.get_functional_reqs(self.xmind_obj, soup)

    @staticmethod
    def get_user_stories(xmind_obj, soup):
        # Set a chapter for feature's stories
        feature_stories = xmind_obj.addSubTopic()
        feature_stories.setTitle('Истории')
        # Find all h3 tags for stories
        stories = soup.find_all('h3', class_=re.compile('US-\d'))
        for n in range(len(stories)):
            # Extract particular story title by number
            story_name = soup.find('h3', class_='US-'+ str(n+1))
            if story_name:
                # Set a story title in map
                story_name_map = feature_stories.addSubTopic()
                story_name_map.setTitle(story_name.string)
            # Extract particular story description by number
            story_description = soup.find('td', class_='US-'+ str(n+1))
            if story_description:
                # Set a story description in map
                story_description_map = story_name_map.addSubTopic()
                story_description_map.setTitle(story_description.string)
            # Extract user story criteria
            criteria = soup.find('ol', class_='US-'+ str(n+1))
            if criteria:
                for li in criteria.contents:
                    if li != '\n':
                        criteria_map = story_description_map.addSubTopic()
                        criteria_map.setTitle(li.string)
    @staticmethod
    def get_functional_reqs(xmind_obj, soup):
        # Set a chapter for feature's functional requirements
        feature_functionals = xmind_obj.addSubTopic()
        feature_functionals.setTitle('Функциональные')
        # Find table with functional requirements
        func_table = soup.find(class_='func')
        if func_table:
            # Get all <tr> within that table
            trs = func_table.find_all('tr')
            # Remove header row
            del trs[0]
            # Iterate through the number of rows
            for n in range(len(trs)):

                f_name = soup.find('td', class_='FR-' + str(n+1))
                if f_name:
                    f_name_map = feature_functionals.addSubTopic()
                    f_name_map.setTitle(f_name.string)

                f_body = soup.find('ol', class_='FR-'+ str(n+1))
                if f_body:
                    for li in f_body.contents:
                        if li != '\n':
                            f_li_map = f_name_map.addSubTopic()
                            f_li_map.setTitle(li.string)