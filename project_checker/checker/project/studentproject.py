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
            self.__report_all_tasks_from_single_branch(branch, report)
            report.store()

    def report_lab_tasks(self, report_dir, lab, date):
        for branch in self.branches.local:
            report = Report(report_dir, 'report-' + lab + '-' + branch.name)
            self.__report_lab_tasks_from_single_branch(branch, report, lab, date)
            report.store()

    def __report_all_tasks_from_single_branch(self, branch, report):
        self.project_dir.restore()
        branch.checkout()
        self.__build_branch(branch)
        test_targets = self.cmake.test_targets_without_compound_all()
        self.report_targets(report, test_targets)

    def __report_lab_tasks_from_single_branch(self, branch, report, lab, date):
        self.project_dir.restore()
        commit = branch.find_commit_before(date)
        branch.checkout(commit)
        self.__build_branch(branch)
        test_targets = self.cmake.test_targets_without_compound_all_of_lab(lab)
        self.report_targets(report, test_targets)

    def __build_branch(self, branch):
        build_dir = self.project_dir.create_dir(self.branch_build_dir_name(branch))
        build_dir.restore()
        self.cmake.build()

    @staticmethod
    def report_targets(report, test_targets):
        for target in test_targets:
            report[target.name] = target.report_result()

    @staticmethod
    def branch_build_dir_name(branch):
        return 'build-' + branch.name


class StudentProject:
    def __init__(self, repository, parent_dir):
        match = re.search('/([-\w]+)/([-\w]+)', repository)
        if match is None:
            print(repository + ' does not match')
            raise RuntimeError('invalid repository: ' + repository + ' does not match')
        user_dir_name = match.group(1)
        print('PROJECT: '+user_dir_name)
        self.working_dir = parent_dir
        self.user_dir = self.working_dir.create_dir(user_dir_name)
        project_dir_name = match.group(2)
        self.project_dir = self.user_dir.relative(project_dir_name)
        self.git = GitProject(self.project_dir, verbose=True)
        self.report_dir = self.project_dir.create_dir('report')
        self.git.synchronize(self.user_dir, repository)

    def check_lab_to_date(self, labs, due_date):
        for lab, date in zip(labs, due_date):
            self.git.report_lab_tasks(self.report_dir, lab, date)

    def compile_final_report(self, name):
        final_report = Report(self.report_dir, 'final-'+name)
        all_reports = self.report_dir.all_partial_reports()
        self.merge_reports(all_reports, final_report)
        final_report.store()
        print(final_report.report)
        final_report.only_passed_tests('final-passed-'+name).store()

        final_lab_report = Report(self.report_dir, 'final-lab' + name)
        lab_reports = filter(lambda r: r.name.startswith('report-lab'), all_reports)
        self.merge_reports(lab_reports, final_lab_report)
        final_lab_report.store()
        print(final_lab_report.report)
        final_lab_report.only_passed_tests('final-lab-passed-' + name).store()

    def merge_reports(self, all_reports, final_report):
        for report in all_reports:
            report.load()
            final_report.merge(report)
