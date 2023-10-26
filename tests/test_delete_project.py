import random
from model.project import Project


def test_delete_project_by_name(app):
    projects_list_before = app.soap.get_projects()
    if len(projects_list_before) == 0:
        app.project.create_new_project(Project(project_name='pj_name'))
        projects_list_before = app.soap.get_projects()
    project = random.choice(projects_list_before)
    project_name = project.project_name
    app.project.delete_project_by_project_name(project_name)
    projects_list_after = app.soap.get_projects()
    assert len(projects_list_before) - 1 == len(projects_list_after)
    projects_list_before.remove(project)
    assert (sorted(projects_list_before, key=Project.is_project_name_empty) ==
            sorted(projects_list_after, key=Project.is_project_name_empty))
