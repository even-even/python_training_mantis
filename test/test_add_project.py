from model.project import Project
import data.projects
import pytest


@pytest.mark.parametrize("project", data.projects.testdata, ids=[repr(y) for y in data.projects.testdata])
def test_add_project(app, project):
    app.session.login("administrator", "root")
    old_projects = app.soap.get_project_list("administrator", "root")
    app.project.create_project(project)
    new_projects = app.soap.get_project_list("administrator", "root")
    assert len(old_projects) + 1 == len(new_projects)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
