import os
from report import Report


class Directory:
    def __init__(self, path=os.getcwd()):
        self.working_dir = os.path.abspath(path)

    def create_dir(self, name):
        d = self.relative(name)
        if self.working_dir != d.working_dir:
            if not d.exists():
                print('creating directory ' + d.working_dir)
                os.mkdir(d.working_dir)
        return d

    def change_dir(self, name):
        d = self.relative(name)
        d.restore()
        print('changed directory to: ' + os.getcwd())
        return d

    def exists(self):
        return os.path.isdir(self.working_dir)

    def restore(self):
        if self.exists():
            os.chdir(self.working_dir)

    def relative(self, name):
        if os.path.isabs(name):
            return Directory(name)
        else:
            p = os.path.join(self.working_dir, name)
            return Directory(p)

    def open(self, name, options):
        if os.path.isabs(name):
            return open(name, options)
        else:
            p = os.path.join(self.working_dir, name)
            return open(p, options)

    def all_partial_reports(self):
        reports = os.listdir(self.working_dir)
        filtered = filter(lambda s: s.startswith('report-'), reports)
        mapped = map(lambda s: Report(self, s), filtered)
        return list(mapped)

    def __str__(self):
        return self.working_dir

    def __eq__(self, other):
        return self.working_dir == other.working_dir

    def __hash__(self):
        return hash(self.working_dir)
