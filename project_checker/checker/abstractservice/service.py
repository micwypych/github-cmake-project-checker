import subprocess


class Service:
    def __init__(self, service_name, verbose=False):
        self.service_name = service_name
        self.verbose = verbose

    def command(self, name, *args):
        cmd = self.create_cmd_args(args, name)
        output = subprocess.check_output(cmd).decode(encoding='UTF-8')
        self.message(name, output)
        return output

    def call(self, name, *args):
        cmd = self.create_cmd_args(args, name)
        output = subprocess.call(cmd)
        self.message(name, output)
        return output

    def message(self, name, output):
        if self.verbose:
            print(self.service_name + '-' + name + ': ' + str(output))

    def create_cmd_args(self, args, name):
        cmd = [self.service_name, name]
        for arg in args:
            cmd.append(arg)
        return cmd
