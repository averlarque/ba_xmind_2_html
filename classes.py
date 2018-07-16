
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
            result += "<tr>\n<td>N.{0}-FR-{1}</td>\n<td class='FR-{1}'>{2}</td>\n<td><ol class='FR-{1}'>\n{3}</ol></td>\n</tr>\n".format(fe_index, fu_index, 
            fu_title, fu_des_items)

        return result

    def create_layout(self):
        table_open = "\n<table class='wrapped'><colgroup><col /><col /><col /></colgroup>\n<tbody class='func'>\n"
        header_row = '<tr>\n<th>ID</th>\n<th>Название</th>\n<th>Описание</th>\n</tr>\n'
        freqs = self._iterate_funcs()
        table_close = '</tbody></table>\n'
        result = table_open + header_row + freqs + table_close
        return result