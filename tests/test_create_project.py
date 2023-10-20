import random
import string
import pytest
from model.project import Project


def random_string(prefix, maxlen):
    if prefix == "status: ":
        status = ("development", "release", "stable", "obsolete")
        return "".join(str(random.choice(status)))
    elif prefix == "view_status: ":
        view_status = ("public", "private")
        return "".join(str(random.choice(view_status)))
    else:
        symbols = string.ascii_letters + string.digits + string.punctuation + " "*10
        return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


n = 1


testdata = [Project(project_name=random_string("project_name: ", 10), description=random_string("description: ", 20),
                    status=random_string("status: ", 2), view_status=random_string("view_status: ", 2))
    for i in range(n)
]


@pytest.mark.parametrize("project", testdata, ids=[repr(x) for x in testdata])
def test_create_project(app, project):
    projects_list_before = app.project.get_projects_list()
    app.project.create_new_project(project)
    projects_list_after = app.project.get_projects_list()
    assert len(projects_list_before) + 1 == len(projects_list_after)
    projects_list_before.append(project)
    assert (sorted(projects_list_before, key=Project.is_project_name_empty) ==
            sorted(projects_list_after, key=Project.is_project_name_empty))
