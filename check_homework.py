from argparse import ArgumentParser
from project_checker.checker.pull_all_links import make_default_config
from project_checker.checker.pull_all_links import check_homework_by_configuration

def make_program_arg_parser():
    parser = ArgumentParser(prog='check homework')
    parser.add_argument('-r', '--only-repositories', dest='repos', type=str, default='',
                        help='regex matchers separated with colon (:) of repositories to include')
    parser.add_argument('-t', '--only-homeworks', dest='homeworks', type=str, default='',
                        help='regex matchers separated with colon (:) of homeworks to include')
    parser.add_argument('-u', '--update-local-repositories', dest='pull',
                        help='pull updates from remote repositories',
                        action='store_true')
    return parser


def main_args(args):
    config = make_default_config()
    repos = args.repos.split(':')
    if len(args.repos) > 0 and len(repos) > 0:
        print('only projects: ' + str(repos))
        config.repository_owners.exclude_other_projects_than(repos)
    else:
        print('processing all projects')
    homework = args.homeworks.split(':')
    if len(args.homeworks) > 0 and len(homework) > 0:
        print('only homeworks: ' + str(homework))
        config.homework.exclude_other_homework_than(homework)
    else:
        print('processing all homeworks')
    if args.pull:
        print('update')
    else:
        print('old version of pull')
    check_homework_by_configuration(config, pull_new_version=args.pull)

def main():
    parser = make_program_arg_parser()
    args = parser.parse_args()
    main_args(args)


if __name__ == "__main__":
    main()
