import re
from project_checker.checker.filesystem import Report
from project_checker.checker.gitservice import GitService
from project_checker.checker.buildservice import CMakeService


class GitProject:
    def __init__(self, project_dir, verbose=False):
        self.verbose = verbose
        self.git = GitService(verbose=self.verbose)
        self.project_dir = project_dir
        self.branches = set()
        self.cmake = CMakeService(verbose=self.verbose)

    def synchronize(self, user_dir, repository):
        self.project_dir.restore()
        if not self.git.exists():
            user_dir.restore()
            self.git.clone(repository)
            self.project_dir.restore()
        self.git.pull()
        self.branches = self.git.list_branches()
        for branch in self.branches.remotes_without_local():
            branch.checkout()
        self.branches = self.git.list_branches()

    def report_all_tasks(self, report_dir):
        for branch in self.branches.local:
            report = Report(report_dir, 'report-' + branch.name)
            self.report_all_tasks_from_single_branch(branch, report)

    def report_all_tasks_from_single_branch(self, branch, report):
        self.project_dir.restore()
        branch.checkout()
        build_dir = self.project_dir.create_dir(self.branch_build_dir_name(branch))
        build_dir.restore()
        self.cmake.build()
        test_targets = self.cmake.test_targets_without_compound_all()
        for target in test_targets:
            report[target.name] = target.report_result()
        report.store()

    @staticmethod
    def branch_build_dir_name(branch):
        return 'build-' + branch.name


class StudentProject:
    def __init__(self, repository, parent_dir):
        match = re.search('/([-\w]+)/([-\w]+)', repository)
        if match is None:
            print (repository + ' does not match')
            raise RuntimeError('invalid repository: ' + repository + ' does not match')
        user_dir_name = match.group(1)
        self.working_dir = parent_dir
        self.user_dir = self.working_dir.create_dir(user_dir_name)
        project_dir_name = match.group(2)
        self.project_dir = self.user_dir.relative(project_dir_name)
        self.git = GitProject(self.project_dir, verbose=True)
        self.report_dir = self.project_dir.create_dir('report')
        self.git.synchronize()

    def build(self):
        pass
