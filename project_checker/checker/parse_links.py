import sys, getopt
import re

my_repos = ['/micwypych-testy2016','/javakisagh','/pfultz2','/mslazynski']

def is_my_repo(link):
  for left in my_repos:
      if link.startswith(left):
        return True
  return False

def find_urls(lines):
  for line in lines:
    match = re.search('<a href="([^"]+)"',line)
    if match == None:
      continue
    link = match.group(1)
    if is_my_repo(link):
      continue
    print('https://github.com'+match.group(1)+'.git')

def main(args):
  find_urls(open(args[0]))


if __name__ == "__main__":
    main(sys.argv[1:])
