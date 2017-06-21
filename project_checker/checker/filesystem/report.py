import re


class Report:
    def __init__(self, report_dir, name):
        self.report_dir = report_dir
        self.name = name
        self.report = {}

    def store(self):
        f = self.report_dir.open(self.name, 'w')
        for key in sorted(self.report.keys()):
            f.write("%s=%s\n" % (key, self.report[key]))
        f.flush()
        f.close()

    def load(self):
        f = self.report_dir.open(self.name, 'r')
        for line in f:
            matcher = re.match('(\w+)\s*=\s*(\d+)', line)
            if matcher != None:
                self.report[matcher.group(1)] = int(matcher.group(2))
            else:
                'skipping line'
        f.close()

    def merge(self, other_report):
        common_keys = set(self.report.keys()).intersection(set(other_report.report.keys()))
        merged = dict(self.report)
        merged.update(other_report.report)
        for key in common_keys:
            merged[key] = min(self[key], other_report[key])
        self.report = merged

    def only_passed_tests(self, new_report_name):
        passed = {k: 'ok' for k, v in self.report.items() if v == 0}
        new_report = Report(self.report_dir, new_report_name)
        new_report.report = passed
        return new_report

    def to_result_ranking(self, labs, sep='\t'):
        mapped = map(lambda l: self[l], labs)
        results = map(lambda result: 'ok' if result == 0 else '0', mapped)
        return sep.join(results)

    def __getitem__(self, item):
        return self.report.get(item, 40)

    def __setitem__(self, key, value):
        self.report[key] = value

    def __str__(self):
        return 'Report(\'' + str(self.report_dir) +'/'+ str(self.name) + '\')'

    __repr__ = __str__

    def __eq__(self, other):
        return self.report_dir == other.report_dir and self.name == other.name

    def __hash__(self):
        return hash(self.working_dir, self.name)
