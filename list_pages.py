#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging
import pathspec
import os
import io
import re

# constants
GITHUB_URL = r'https://github.com/'

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.DEBUG)
LOGGER = logging.getLogger('list-pages')


def read_ignorefile(filename):
    with open(filename) as f:
        return pathspec.PathSpec.from_lines('gitignore', f)


def create_child_list(path, files, repo, ignorespec):
    indent = path.count(os.sep)

    header = '%s- %s\n' % ('\t' * (indent - 1), os.path.basename(path)) if path != '' else ''

    child_list = []
    for f in files:
        if ignorespec.match_file(f):
            continue

        child_list.append('%s- [%s](%s/%s/wiki%s/%s)' % \
            ('\t' * indent, os.path.splitext(f)[0], GITHUB_URL, repo, path, f))

    return header + '\n'.join(child_list)


def list_pages(root, repo, ignorefile):
    ignorespec = read_ignorefile(ignorefile)

    result = []
    for path, dirs, files in os.walk(root):
        p = path.replace(root, '')

        LOGGER.debug('checking %s' % (p))

        if ignorespec.match_file(path):
            LOGGER.debug('ignoring %s' % (p))
            continue

        result.append(create_child_list(p, files, repo, ignorespec))

    print('\n'.join(result))


def main():
    parser = argparse.ArgumentParser(description='Update wiki pages with their child list')

    parser.add_argument('input', help='the folder of your github wiki')
    parser.add_argument('repo', help='the repository name of your github repo (e.g., username/repository)')
    parser.add_argument('-i', '--ignore', help='a file containing paths to be ignored', default='.pathignore')

    args = parser.parse_args()

    list_pages(args.input, args.repo, args.ignore)


if __name__ == '__main__':
    main()
