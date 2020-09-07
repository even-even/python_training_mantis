from model.project import Project
import random


def test_delete_some_project(app):
    app.session.login("administrator", "root")
    if len(app.soap.get_project_list("administrator", "root")) == 0:
        app.contact.create_project(Project(name="new_project"))
    old_projects = app.soap.get_project_list("administrator", "root")
    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.id)
    new_projects = app.soap.get_project_list("administrator", "root")
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert sorted(new_projects, key=Project.id_or_max) == sorted(old_projects, key=Project.id_or_max)
