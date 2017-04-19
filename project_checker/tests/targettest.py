from unittest import TestCase
from unittest.mock import MagicMock

from project_checker.checker.buildservice import Target


class ServiceStub:
    pass

class TargetTest(TestCase):
    def test_branches_creation_no_branches(self):
        service = MagicMock()
        target = Target('name', service)
        target.report_result()
        service.run.assert_called_with('name')
