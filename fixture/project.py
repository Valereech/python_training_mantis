import time
from selenium.webdriver.support.select import Select
from model.project import Project

class ProjectsHelper:

    def __init__(self, app):
        self.app = app

    def open_projects_page(self):
        pass

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def status_fields(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            Select(wd.find_element_by_xpath("//select[@name='"+field_name+"']")).select_by_visible_text(text)
            wd.find_element_by_xpath("//*/text()[normalize-space(.)='"+text+"']/parent::*").click()

    def fill_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.project_name)
        self.status_fields("status", project.status)
        wd.find_element_by_name("inherit_global").click()
        self.status_fields("view_state", project.view_status)
        self.change_field_value("description", project.description)

    def create_new_project(self, project):
        wd = self.app.wd
        if not wd.current_url.endswith("/manage_proj_create_page.php"):
            self.go_to_manage_projects_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_form(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        time.sleep(3)
        self.projects_cache = None

    def go_to_manage_projects_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("/manage_proj_page.php"):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def delete_project_by_project_name(self, project_name):
        wd = self.app.wd
        self.go_to_manage_projects_page()
        wd.find_element_by_xpath("//a[contains(text(), "+project_name+")]").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        self.projects_cache = None

    projects_cache = None

    def get_projects_list(self):
        if self.projects_cache is None:
            wd = self.app.wd
            self.go_to_manage_projects_page()
            self.projects_cache = []
            for element in wd.find_elements_by_xpath("//table[3]/tbody/tr[contains(@class,'row')]")[1:]:
                project_name = element.find_element_by_css_selector("td:nth-child(1) a:nth-child(1)").text
                status = element.find_element_by_css_selector("td:nth-child(2)").text
                view_status = element.find_element_by_css_selector("td:nth-child(4)").text
                description = element.find_element_by_css_selector("td:nth-child(5)").text
                self.projects_cache.append(Project(project_name=project_name, description=description,
                                                   status=status, view_status=view_status))
        return list(self.projects_cache)
