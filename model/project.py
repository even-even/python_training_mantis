from sys import maxsize


class Project:

    def __init__(self, id=None, name=None, status=None, view_state=None, description=None):
        self.id = id
        self.name = name
        self.status = status
        self.view_state = view_state
        self.description = description

    def __repr__(self):
        return "%s;%s;%s;%s;%s" % (self.id, self.name, self.status, self.view_state, self.description)

    def __eq__(self, other):
        return (self.id == other.id or self.id is None or other.id is None) and self.name == other.name

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
