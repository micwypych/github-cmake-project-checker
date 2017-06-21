from unittest import TestCase
from unittest.mock import MagicMock

from project_checker.checker.filesystem import Report


class ReportTest(TestCase):
    def test_result_ranking_of_two_labs(self):
        report = self.report_labs(['lab1_ex1=0', 'lab1_ex2=2'])
        self.assertEqual('ok;0', report.to_result_ranking(['lab1_ex1', 'lab1_ex2'], sep=';'))

    def test_result_ranking_of_partially_intersecting_labs(self):
        report = self.report_labs(['lab1_ex1=0', 'lab1_ex2=2', 'lab2_ex1=1', 'lab2_ex2=0'])
        self.assertEqual('0;ok', report.to_result_ranking(['lab1_ex2', 'lab2_ex2'], sep=';'))

    def test_result_ranking_of_partially_intersecting_labs_more_results(self):
        report = self.report_labs(['lab1_ex1=0', 'lab1_ex2=2', 'lab2_ex1=1', 'lab2_ex2=0'])
        self.assertEqual('ok;0;ok', report.to_result_ranking(['lab1_ex1', 'lab1_ex2', 'lab2_ex2'], sep=';'))

    def test_result_ranking_of_four_labs_absent_from_report(self):
        report = self.report_labs(['lab1_ex1=0', 'lab1_ex2=2'])
        self.assertEqual('ok;0;0;0', report.to_result_ranking(['lab1_ex1', 'lab1_ex2','lab2_ex1', 'lab2_ex2'], sep=';'))

    def test_merging_of_two_reports(self):
        report1 = self.report_labs(['lab1_ex1=0', 'lab1_ex2=2', 'lab2_ex1=1', 'lab2_ex2=0'])
        report2 = self.report_labs(['lab1_ex2=0', 'lab3_ex1=0'])
        report1.merge(report2)
        self.assertEquals('ok;ok;0;ok;ok',
            report1.to_result_ranking(['lab1_ex1', 'lab1_ex2', 'lab2_ex1', 'lab2_ex2', 'lab3_ex1'], sep=';'))

    def test_merging_of_two_reports_other_way_round(self):
        report1 = self.report_labs(['lab1_ex1=0', 'lab1_ex2=2', 'lab2_ex1=1', 'lab2_ex2=0'])
        report2 = self.report_labs(['lab1_ex2=0', 'lab3_ex1=0'])
        report2.merge(report1)
        self.assertEquals('ok;ok;0;ok;ok',
            report2.to_result_ranking(['lab1_ex1', 'lab1_ex2', 'lab2_ex1', 'lab2_ex2', 'lab3_ex1'], sep=';'))

    def test_merging_of_two_reports_other_way_round(self):
        report1 = self.report_labs(['lab1_ex1=0', 'lab1_ex2=2', 'lab2_ex1=1', 'lab2_ex2=0'])
        report2 = self.report_labs(['lab1_ex2=0', 'lab3_ex1=0'])
        report2.merge(report1)
        self.assertEquals('ok;ok;0;ok;ok',
            report2.to_result_ranking(['lab1_ex1', 'lab1_ex2', 'lab2_ex1', 'lab2_ex2', 'lab3_ex1'], sep=';'))

    def report_labs(self, labs):
        file = MagicMock(__iter__=lambda *args: iter(labs))
        directory = MagicMock(open=lambda *args: file)
        report = Report(directory, 'report')
        report.load()
        return report
