import os
from unittest import TestCase
from project_checker.checker.filesystem import Directory
from project_checker.checker.filesystem import Report


class DirectoryTest(TestCase):
    def __init__(self, test_case_name):
        super(DirectoryTest, self).__init__(test_case_name)
        self.listdir = os.listdir
        self.abspath = os.path.abspath
        self.mkdir = os.mkdir
        self.isdir = os.path.isdir

    def setUp(self):
        self.restore_os()

    def tearDown(self):
        self.restore_os()

    def restore_os(self):
        os.listdir = self.listdir
        os.path.abspath = self.abspath
        os.mkdir = self.mkdir
        os.path.isdir = self.isdir

    def test_finds_partial_report_declared_within_directory(self):
        os.listdir = lambda s: ['abc', 'efg', 'report-abc']
        os.path.abspath = lambda s: '/test'
        directory = Directory()
        self.assertEquals([Report(directory, 'report-abc')], directory.all_partial_reports())

    def test_child_directory_creation(self):
        self.restore_os()
        os.mkdir = lambda name: None
        os.isdir = lambda name: False
        directory = Directory('/absolute/path')
        tmp_directory = Directory('/another')
        tmp_directory.restore()
        subpath = directory.create_dir('subpath')
        self.assertEquals('/absolute/path/subpath', subpath.working_dir)
