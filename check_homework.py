import sys
from project_checker.checker import pull_all_links


if __name__ == "__main__":
    pull_all_links.new_main(sys.argv[1:])