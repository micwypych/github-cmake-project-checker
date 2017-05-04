import re
from project_checker.checker.abstractservice import Service
from project_checker.checker.gitservice.branch import Branches


class GitService(Service):
    def __init__(self, verbose=False):
        super(GitService, self).__init__('git', verbose=verbose)
        self.verbose = verbose

    def status(self):
        return self.command('status')

    def pull(self):
        return self.command('pull')

    def checkout_branch(self, branch):
        return self.command('checkout', branch.name, '--')

    def checkout_commit(self, commit):
        return self.command('checkout', commit.id(), '--')

    def clone(self, repo_url):
        return self.command('clone', repo_url)

    def list_branches(self):
        def local_matcher(line):
            stripped = line.strip(' \t\n\r')
            return re.match(r'^(\*\s)?([^\*/\s]+)$', stripped)

        def remote_matcher(line):
            stripped = line.strip(' \t\n\r')
            return re.match(r'remotes/origin/([^\s]+)', stripped)

        def local_filter(line):
            match = local_matcher(line)
            if match == None:
                return False
            return True

        def remote_filter(line):
            match = remote_matcher(line)
            if match == None:
                return False
            if match.group(1) == 'HEAD':
                return False
            return True

        output = self.command('branch', '-a')
        lines = output.split('\n')
        local = filter(local_filter, lines)
        remote = filter(remote_filter, lines)
        local_names = map(lambda l: local_matcher(l).group(2), local)
        remote_names = map(lambda l: remote_matcher(l).group(1), remote)
        return Branches(self, local=local_names, remote=remote_names)

    def status(self):
        return self.command('status')

    def exists(self, project_directory):
        return self.call('status') == 0 or not project_directory.exists()
