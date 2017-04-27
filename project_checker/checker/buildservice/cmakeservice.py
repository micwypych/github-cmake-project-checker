from project_checker.checker.abstractservice import Service
from project_checker.checker.buildservice.makeservice import MakeService


class Target:
    def __init__(self, name, make_service):
        self.name = name
        self.make_service = make_service

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def report_result(self):
        return self.make_service.run(self.name)

    def __str__(self):
        return 'Target('+self.name+')'

    __repr__ = __str__


class CMakeService(Service):
    def __init__(self, verbose=False):
        super(CMakeService, self).__init__('cmake', verbose=verbose)
        self.make_service = MakeService(verbose=verbose)

    def build(self):
        return self.call('..')

    def list_all_targets(self):
        output = self.command('--build', '.', '--target', 'help')
        lines = output.split('\n')
        return set(map(lambda s: Target(s.strip(' \t\n\r')[4:], self.make_service), lines[2:]))

    def test_targets_without_compound_all(self):
        all_targets = self.list_all_targets()
        test_targets = filter(lambda t: t.name.endswith('tests') and not t.name.endswith('all_tests'), all_targets)
        return set(test_targets)

    def test_targets_without_compound_all_of_lab(self, lab):
        all_targets = self.list_all_targets()
        test_targets = filter(lambda t: t.name.endswith('tests') and t.name.startswith(lab+'_') and not t.name.endswith('all_tests'), all_targets)
        return set(test_targets)
