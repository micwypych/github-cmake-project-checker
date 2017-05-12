from unittest import TestCase
from unittest.mock import MagicMock

from project_checker.checker.project import StudentProject


class ReportTest(TestCase):
    def test_result_ranking_of_two_labs(self):
        r1 = MagicMock(report={'lab1_ex1': 0, 'lab1_ex2': 2, 'lab1_ex3': 0},
                       __getitem__=lambda s, index: s.report[index])
        r2 = MagicMock(report={'lab1_ex1': 2, 'lab1_ex2': 2, 'lab1_ex3': 2},
                       __getitem__=lambda s, index: s.report[index])
        r3 = MagicMock(report={'lab1_ex1': 0, 'lab1_ex2': 0, 'lab1_ex3': 0},
                       __getitem__=lambda s, index: s.report[index])

        written = []
        read = ['lab2_ex1: 0', 'lab2_ex2: 2']
        file = MagicMock(write=lambda line: written.append(line), __iter__=lambda *args: iter(read))
        directory = MagicMock(all_partial_reports=lambda *args: [r1, r2, r3], open=lambda name, opt: file)
        project = StudentProject('url.com/USER/REPO.git', directory)
        project.report_dir = directory
        project.compile_final_report('report')
        self.assertEquals(
            ['lab1_ex1=0\n', 'lab1_ex2=0\n', 'lab1_ex3=0\n', 'lab1_ex1=ok\n', 'lab1_ex2=ok\n', 'lab1_ex3=ok\n',
             'lab1_ex1=0\n', 'lab1_ex2=0\n', 'lab1_ex3=0\n', 'lab1_ex1=ok\n', 'lab1_ex2=ok\n', 'lab1_ex3=ok\n'],
            written)
        
    def test_changing_protocol_to_ssh(self):
        self.assertEquals('ssh://git@github.com/USER/REPO.git', StudentProject.to_ssh('https://github.com/USER/REPO.git'))


class StudentProjectTest(TestCase):
    def test_create_simple_project_name(self):
        project = StudentProject('https://github.com/USER/REPO.git', MagicMock())
        self.assertEquals('USER', project.user_dir_name)
        self.assertEquals('REPO', project.project_dir_name)

    def test_create_project_name_with_hyphens(self):
        project = StudentProject('https://github.com/USER--WITH-HYPHENS/REPO-WITH--HYPHENS--.git', MagicMock())
        self.assertEquals('USER--WITH-HYPHENS', project.user_dir_name)
        self.assertEquals('REPO-WITH--HYPHENS--', project.project_dir_name)

    def test_create_project_name_with_dots(self):
        project = StudentProject('https://github.com/USER..WITH.HYPHENS/REPO.WITH.DOTS...git', MagicMock())
        self.assertEquals('USER..WITH.HYPHENS', project.user_dir_name)
        self.assertEquals('REPO.WITH.DOTS..', project.project_dir_name)

    def test_create_project_without_git_extension(self):
        project = StudentProject('https://github.com/USER/REPO', MagicMock())
        self.assertEquals('USER', project.user_dir_name)
        self.assertEquals('REPO', project.project_dir_name)
