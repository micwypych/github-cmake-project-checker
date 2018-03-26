import re
from project_checker.checker.project import StudentProject


def matches_one_of(key, list_of_patterns):
    for pattern in list_of_patterns:
        if re.search(pattern, key) is not None:
            return True
    return False


class ProjectOwners:
    def __init__(self, parent_directory, file_name):
        self.parent_directory = parent_directory
        self.file_name = file_name
        self.__projects = dict()
        self.__declared_order = []
        self.listed = False

    def list_student_projects(self):
        if not self.listed:
            for n_line,line in enumerate(self.parent_directory.open(self.file_name, 'r')):
                if ';' not in line:
                  print("{0} skpping invalid line({1}): {2}".format(self.file_name, n_line, line))
                  continue
                project, owner1, owner2 = line.split(';')
                project_name = project.strip(' \t\n\r\f')
                owner1_name = owner1.strip(' \t\n\r\f')
                owner2_name = owner2.strip(' \t\n\r\f')
                p = StudentProject(project_name, self.parent_directory)
                if owner1_name != 'none':
                    p.add_owner(owner1_name)
                if owner2_name != 'none':
                    p.add_owner(owner2_name)

                self.__declared_order.append(project_name)
                self.__projects[project_name] = p
            self.listed = True
        return list(map(lambda name: self[name], self.__declared_order))

    def exclude_other_projects_than(self, list_of_patterns):
        self.list_student_projects()
        after_exclusion = {}
        for k, v in self.__projects.items():
            if matches_one_of(k, list_of_patterns):
                after_exclusion[k] = v
            else:
                self.__declared_order.remove(k)
        self.__projects = after_exclusion

    def __getitem__(self, item):
        return self.__projects[item]


class Groups:
    def __init__(self, parent_directory, file_name):
        self.parent_directory = parent_directory
        self.file_name = file_name
        self.students = dict()

    def list_students(self):
        for line in self.parent_directory.open(self.file_name, 'r'):
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
        for line in self.parent_directory.open(self.file_name, 'r'):
            lab, due = line.split('\t')
            lab_name = lab.strip(' \t\n\r\f')
            due_date = due.strip(' \t\n\r\f')
            self.deadlines[lab_name] = due_date

        return self.deadlines

    def __getitem__(self, item):
        return self.deadlines[item]


class Homeworks:
    def __init__(self, parent_directory, file_name):
        self.parent_directory = parent_directory
        self.file_name = file_name
        self.tasks = []
        self.listed = False

    def list(self):
        if self.listed:
            return self.tasks
        for line in self.parent_directory.open(self.file_name, 'r'):
            self.tasks.append(line.strip(' \t\n\r\f'))
        self.listed = True
        return self.tasks

    def exclude_other_homework_than(self, homeworks):
        self.list()
        filtered = []
        for t in self.tasks:
            if matches_one_of(t, homeworks):
                filtered.append(t)
        self.tasks = filtered



class Config:
    def __init__(self, parent_directory):
        self.parent_directory = parent_directory
        self.deadline_pattern = re.compile('deadline_(\d[ab])')
        self.deadline_filenames = self.parent_directory.all_deadlines_by_pattern(self.deadline_pattern)
        print("loading deadlines files: {0}".format(self.deadline_filenames))
        self.deadline3b_name = 'deadline_3b'
        self.deadline4a_name = 'deadline_4a'
        self.deadline4b_name = 'deadline_4b'
        self.deadline5a_name = 'deadline_5a'
        self.groups_name = 'groups'
        self.repository_owners_name = 'repository_owners'
        self.homework_name = 'homework'

        self.deadlines = dict()
        for filename in self.deadline_filenames:
          group_name = str(self.deadline_pattern.match(filename).group(1))
          deadline = Deadlines(self.parent_directory, filename)
          self.deadlines[group_name] = deadline
        self.groups = Groups(self.parent_directory, self.groups_name)
        self.repository_owners = ProjectOwners(self.parent_directory, self.repository_owners_name)
        self.homework = Homeworks(self.parent_directory, self.homework_name)

    def load(self):
        self.groups.list_students()
        self.repository_owners.list_student_projects()
        for deadline in self.deadlines.values():
            deadline.list_deadlines()
        self.homework.list()

    def student_projects(self):
        return self.repository_owners.list_student_projects()

    def deadlines_for_owners(self, owners):
        if len(owners) == 0:
            raise IndexError('no owners specified')
        group1 = self.groups[owners[0]]
        group = group1
        if len(owners) == 2:
            group2 = self.groups[owners[1]]
            if (group1 != group2):
                raise Exception('different groups')
        return self.deadlines[group]

    def homework(self):
        return self.homework.list()

    def save_homework_results_ranking(self, ranking):
        f = self.parent_directory.open('results-ranking', 'w')
        for line in ranking:
            f.write(line)
            f.write('\n')
        f.flush()
        f.close()
