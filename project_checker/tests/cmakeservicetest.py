from unittest import TestCase
from unittest.mock import MagicMock

from project_checker.checker.buildservice import CMakeService


class CMakeServiceTest(TestCase):
    def test_branches_creation_no_branches(self):
        service = CMakeService()
        service.list_all_targets = lambda: ['lab1', 'lab11', 'lab1_test', 'lab1_all_tests']
        output = service.test_targets_without_compound_all_of_lab('lab1')
        self.assertIn('lab1_test', output)
