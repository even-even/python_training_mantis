from selenium.webdriver.support.ui import Select
from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_manage_projects_page(self):
        wd = self.app.wd
        wd.get("http://localhost/mantisbt-1.2.20/manage_proj_page.php")

    def open_add_project_page(self):
        wd = self.app.wd
        self.open_manage_projects_page()
        if not wd.current_url.endswith("/manage_proj_create_page.php"):
            wd.find_element_by_xpath("//input[@value='Create New Project']").click()
            self.implicitly_wait(3)

    def create_project(self, project):
        wd = self.app.wd
        self.open_add_project_page()
        self.fill_project_form(project)
        # submit project creation
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.implicitly_wait(5)

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        self.select_dropdown_value("status", project.status)
        self.select_dropdown_value("view_state", project.view_state)
        self.change_field_value("description", project.description)
        self.implicitly_wait(1)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def select_dropdown_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            Select(wd.find_element_by_name(field_name)).select_by_visible_text(text)
            # wd.find_element_by_link_text(text).click()

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_manage_projects_page()
        self.select_project_by_id(id)
        self.implicitly_wait(1)
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        self.project_cache = None
        self.implicitly_wait(2)

    def select_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[@href='manage_proj_edit_page.php?project_id=%s']" % id).click()

    project_cache = None

    def get_project_list(self):
        wd = self.app.wd
        self.open_manage_projects_page()
        self.project_cache = []
        all_tables = wd.find_elements_by_xpath("//table[@class='width100']")
        table = all_tables[1]
        rows = table.find_elements_by_xpath(".//tr[contains(@class, 'row')]")
        del rows[0]
        for element in rows:
            cells = element.find_elements_by_tag_name("td")
            name = cells[0].text
            description_text = cells[4].text
            id_link = wd.find_element_by_link_text(name).get_attribute("href")
            id_index = id_link.index('=') + 1
            id = id_link[id_index:]
            self.project_cache.append(Project(id=id, name=name, description=description_text))
        return list(self.project_cache)

    def implicitly_wait(self, param):
        pass
