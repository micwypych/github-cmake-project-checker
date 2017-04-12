from project_checker.checker.abstractservice import Service


class MakeService(Service):
    def __init__(self, verbose=False):
        super(MakeService, self).__init__('make', verbose=verbose)

    def run(self, task_name):
        return int(self.call(task_name))
