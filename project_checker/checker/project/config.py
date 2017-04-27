from project_checker.checker.project import StudentProject


class ProjectOwners:
    def __init__(self, parent_directory, file_name):
        self.parent_directory = parent_directory
        self.file_name = file_name
        self.projects = dict()

    def list_student_projects(self):
        for line in self.parent_directory.open(self.file_name):
            project, owner1, owner2 = line.split(';')
            project_name = project.strip(' \t\n\r\f')
            p = StudentProject(project_name, self.parent_directory)
            p.add_owner(owner1)
            if owner2 != 'none':
                p.add_owner(owner2)

            self.projects[project_name] = p
        return self.projects

    def __getitem__(self, item):
        return self.projects[item]


class Groups:
    def __init__(self, parent_directory, file_name):
        self.parent_directory = parent_directory
        self.file_name = file_name
        self.students = dict()

    def list_students(self):
        for line in self.parent_directory.open(self.file_name):
            owner, g = line.split('\t')
            owner_id = owner.strip(' \t\n\r\f')
            g = g.strip(' \t\n\r\f')
            self.students[owner_id] = g

        return self.students

    def __getitem__(self, item):
        return self.students[item]


class Deadlines:
    def __init__(self, parent_directory, file_name):
        self.parent_directory = parent_directory
        self.file_name = file_name
        self.deadlines = dict()

    def list_deadlines(self):
        for line in self.parent_directory.open(self.file_name):
            lab, due = line.split('\t')
            lab_name = lab.strip(' \t\n\r\f')
            due_date = due.strip(' \t\n\r\f')
            self.deadlines[lab_name] = due_date

        return self.deadlines

    def __getitem__(self, item):
        return self.deadlines[item]


class Config:
    def __init__(self, parent_directory):
        self.parent_directory = parent_directory
        self.deadline3b_name = 'deadline_3b'
        self.deadline4a_name = 'deadline_4a'
        self.deadline4b_name = 'deadline_4b'
        self.deadline5a_name = 'deadline_5a'
        self.groups_name = 'groups'
        self.repository_owners_name = 'repository_owners'

        self.deadlines = map()
        self.deadlines['3b'] = Deadlines(self.parent_directory, self.deadline3b_name)
        self.deadlines['4a'] = Deadlines(self.parent_directory, self.deadline4a_name)
        self.deadlines['4b'] = Deadlines(self.parent_directory, self.deadline4b_name)
        self.deadlines['5a'] = Deadlines(self.parent_directory, self.deadline5a_name)
        self.groups = Groups(self.parent_directory, self.groups_name)
        self.repository_owners = ProjectOwners(self.parent_directory, self.repository_owners_name)



