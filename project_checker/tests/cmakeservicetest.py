from unittest import TestCase
from unittest.mock import MagicMock

from project_checker.checker.buildservice import CMakeService
from project_checker.checker.buildservice import Target


class CMakeServiceTest(TestCase):
    def test_filtering_targets_of_lab1_does_skip_lab11_targets(self):
        service = CMakeService()
        service.list_all_targets = lambda: self.target_set('lab1', 'lab11_tests', 'lab1_tests', 'lab1_all_tests')
        output = service.test_targets_without_compound_all_of_lab('lab1')
        self.assertSetEqual(self.target_set('lab1_tests'), output)

    def target(self, name):
        return Target(name, MagicMock())

    def target_set(self, *args):
        return set(map(self.target, args))
