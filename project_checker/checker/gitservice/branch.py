import re


class CommitId:
    def __init__(self, name):
        matches = re.match('[0-9a-fA-F]+', name)
        if not matches:
            raise RuntimeError('invalid commit id: '+name)
        self.name = name

    def id(self):
        return self.name


class Branch:
    def __init__(self, name, git_service):
        self.__name = name
        self.git_service = git_service

    def __hash__(self):
        return hash(self.__name)

    def __eq__(self, other):
        return self.__name == other.__name

    def escaped_name(self):
        return re.sub('/', '_', self.__name)

    def checkout_name(self):
        return self.__name


class LocalBranch(Branch):
    def checkout(self, commit=None):
        if commit is None:
            return self.git_service.checkout_branch(self)
        else:
            return self.git_service.checkout_commit(commit)

    def find_commit_before(self, date):
        matches = re.match('\d{4}-\d{2}-\d{2} \d{2}:\d{2}', date)
        if not matches:
            raise RuntimeError('invalid date format')
        return CommitId(
            self.git_service.command('rev-list', '-n', '1', '--before="' + date + '"', self.checkout_name(), '--').strip(
                ' \t\n\r'))

    def __str__(self):
        return 'local:' + self.checkout_name()

    __repr__ = __str__


class RemoteBranch(Branch):
    def checkout(self):
        return self.git_service.command('checkout', '-b', self.checkout_name(), 'origin/' + self.checkout_name())

    def __str__(self):
        return 'remote:' + self.checkout_name()

    __repr__ = __str__


class Branches:
    def __init__(self, git_service, local=set([]), remote=set([])):
        self.git_service = git_service
        self.local = set(map(lambda name: LocalBranch(name, self.git_service), set(local)))
        self.remote = set(map(lambda name: RemoteBranch(name, self.git_service), set(remote)))

    def remotes_without_local(self):
        return self.remote.difference(self.local)

    def __len__(self):
        return len(self.local)

    def first_branch(self):
        return list(self.local)[0]
