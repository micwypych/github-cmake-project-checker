from unittest import TestCase
from project_checker.checker.gitservice import Branches
from project_checker.checker.gitservice import RemoteBranch
from project_checker.checker.gitservice import LocalBranch


class ServiceStub:
    pass


class BranchTest(TestCase):
    def test_branches_creation_no_branches(self):
        servicestub = ServiceStub()
        branches = Branches(servicestub)
        self.assertEquals(self.empty_set(), branches.remotes_without_local())

    def test_branches_creation_single_master_branch(self):
        servicestub = ServiceStub()
        branches = Branches(servicestub, local=['master'], remote=['master'])
        self.assertEquals(self.empty_set(), branches.remotes_without_local())

    def test_branches_creation_single_master_remote_branch_no_local(self):
        servicestub = ServiceStub()
        branches = Branches(servicestub, remote=['master'])
        self.assertEquals(self.remotes(servicestub, names=['master']), branches.remotes_without_local())

    def test_branches_creation_several_partially_matching_branches(self):
        servicestub = ServiceStub()
        branches = Branches(servicestub,
                            local=['master', 'lab1', 'lab3'],
                            remote=['master', 'lab1', 'lab2', 'lab5', 'lab4', 'lab9'])
        self.assertEquals(self.remotes(servicestub, names=['lab2', 'lab5', 'lab4', 'lab9']),
                          branches.remotes_without_local())

    def test_branches_creation_single_master_local_branch(self):
        servicestub = ServiceStub()
        branches = Branches(servicestub, local=['master'])
        self.assertEquals(self.locals(servicestub, ['master']), branches.local)

    def empty_set(self):
        return set([])

    def locals(self, servicestub, names=[]):
        return set(map(lambda n: LocalBranch(n, servicestub), names))

    def remotes(self, servicestub, names=[]):
        return set(map(lambda n: RemoteBranch(n, servicestub), names))
