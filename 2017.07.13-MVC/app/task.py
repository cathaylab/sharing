import json

class Task(object):
    def __init__(self, tid, title, description, done):
        self.tid = tid
        self.title = title
        self.description = description
        self.done = done

    def to_json(self):
        return json.dumps({"tid": tid, "title": title, "description": description, "done": done})

class TaskDAO(object):
    def __init__(self):
        pass

    def update(self, task):
        pass

    def add(self, task):
        pass

    def delete(self, task):
        pass

    def find(self, task):
        pass
