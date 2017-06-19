from unittest import TestCase
from unittest.mock import MagicMock

from project_checker.checker.project import Deadlines
from project_checker.checker.project import Groups
from project_checker.checker.project import ProjectOwners
from project_checker.checker.project import StudentProject
from project_checker.checker.filesystem import Directory


class DeadlinesTest(TestCase):
    def test_listing_deadlines(self):
        dir_service = Directory()
        dir_service.open = lambda *args: ['lab1\t2017-03-09 14:00', 'lab2\t2017-03-16 14:00', 'lab5\t2017-05-14 14:00']
        d = Deadlines(dir_service, 'whatever')

        self.assertEqual({'lab1': '2017-03-09 14:00', 'lab2': '2017-03-16 14:00', 'lab5': '2017-05-14 14:00'},
                         d.list_deadlines())


class GroupsTest(TestCase):
    def test_listing_groups(self):
        dir_service = Directory()
        dir_service.open = lambda *args: ['299111	4a', '281111	4a', '222222	3b']
        d = Groups(dir_service, 'whatever')

        self.assertEqual({'299111': '4a', '281111': '4a', '222222': '3b'},
                         d.list_students())


class ProjectOwnersTest(TestCase):
    def test_listing_groups(self):
        dir_service = MagicMock(open=lambda *args: ['https://github.com/owner/repo-2.git;111111;222222',
                                      'https://github.com/another-owner/repo-2.git;313131;111112',
                                      'https://github.com/owner2/repo-2.git;891929;none'])
        d = ProjectOwners(dir_service, 'whatever')

        self.assertEqual(self.projects(dir_service),
                         d.list_student_projects())

    @staticmethod
    def projects(d):
        r1 = 'https://github.com/owner/repo-2.git'
        p1 = StudentProject(r1, d)
        p1.add_owner('111111')
        p1.add_owner('222222')

        r2 = 'https://github.com/another-owner/repo-2.git'
        p2 = StudentProject(r2, d)
        p2.add_owner('313131')
        p2.add_owner('111112')
        r3 = 'https://github.com/owner2/repo-2.git'
        p3 = StudentProject(r3, d)
        p3.add_owner('891929')

        return [p1, p2, p3]
