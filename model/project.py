

class Project:

    def __init__(self, project_name, status, view_status, description):
        self.project_name = project_name
        self.description = description
        self.status = status
        self.view_status = view_status

    def __repr__(self):
        return "%s | %s | %s | %s" % (self.project_name, self.status, self.view_status, self.description)

    def __eq__(self, other):
        return self.project_name == other.project_name and self.description == other.description

    def is_project_name_empty(self):
        if self.project_name:
            return self.project_name
        else:
            return ""
