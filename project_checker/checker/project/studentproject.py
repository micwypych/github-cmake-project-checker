import re


class ProjectDirectories:
    pass


class StudentProject:
    def __init__(self, repository, parent_dir):
        match = re.search('/([-\w]+)/([-\w]+)', repository)
        if match is None:
            print (repository + ' does not match')
            raise RuntimeError('invalid repository: ' + repository + ' does not match')
        user_dir_name = match.group(1)
        self.working_dir = parent_dir
        self.user_dir = parent_dir.create_dir(user_dir_name)

    def build(self):
        pass
