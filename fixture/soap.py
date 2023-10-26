from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client(self.app.config['app_link']['baseUrl'] + "/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects(self):
        username = self.app.config['app_creds']['username']
        password = self.app.config['app_creds']['password']
        client = Client(self.app.config['app_link']['baseUrl'] + "/api/soap/mantisconnect.php?wsdl")
        try:
            list_of_projects = []
            projects_user_accessible = client.service.mc_projects_get_user_accessible(username, password)
            for project in projects_user_accessible:
                list_of_projects.append(Project(project_name=project.name, description=project.description,
                                                status=project.status, view_status=project.view_state))
            return list_of_projects
        except WebFault:
            return None
