from unittest import TestCase
from unittest.mock import MagicMock

from project_checker.checker.pull_all_links import check_homework_from_config
import project_checker.checker.project as prj


class StubConfig(prj.Config):
    def __init__(self, lines):
        self.load = lambda *args: None
        self.student_projects = lambda *args: {'https://github.com/USER/project.git': MagicMock(owners=['200100'],to_result_raniking_lines=lambda *args: 'ok;ok;0;0;ok')}
        self.groups = {'200100': '1c'}
        self.deadlines = {'1c': ['2000-01-01 12:34']}
        self.homework = MagicMock(list=lambda *args: ['lab1_ex1', 'lab1_ex2'])

        file_stub = MagicMock(write=lambda txt: lines.append(txt))
        self.parent_directory = MagicMock(open=lambda *args: file_stub)


class CMakeServiceTest(TestCase):
    def test_single_project_with_one_owner_five_ranking_tasks(self):
        lines = []
        prj.Config.__init__ = lambda s, *directory: StubConfig.__init__(s, lines)
        check_homework_from_config()
        self.assertIn('200100;ok;ok;0;0;ok', lines)
