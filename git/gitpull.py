# -*- coding: utf-8 -*
"""
      ┏┓       ┏┓
    ┏━┛┻━━━━━━━┛┻━┓
    ┃      ☃      ┃
    ┃  ┳┛     ┗┳  ┃
    ┃      ┻      ┃
    ┗━┓         ┏━┛
      ┗┳        ┗━┓
       ┃          ┣┓
       ┃          ┏┛
       ┗┓┓┏━━━━┳┓┏┛
        ┃┫┫    ┃┫┫
        ┗┻┛    ┗┻┛
    God Bless,Never Bug
"""

import os
import sys
import re
from getopt import getopt


class GitPull:
    _OPTS_DICT = None
    _BRANCH = 'develop'
    _MODULE_PATH = os.getcwd()
    _SUBMODULE_PATH = list()
    _SUBMODULE_PATTERN = re.compile(r'\[submodule "(.+)"\]')

    @classmethod
    def _get_submodule(cls):
        git_config_path = os.path.join(cls._MODULE_PATH, '.git/config')
        if not os.path.isfile(git_config_path):
            sys.exit("【GIT MODULE NOT FOUND.】")
        with open(git_config_path, 'r') as f:
            git_config = f.read()
        if cls._SUBMODULE_PATTERN.search(git_config):
            cls._SUBMODULE_PATH = [os.path.join(cls._MODULE_PATH, submodule)
                                   for submodule in cls._SUBMODULE_PATTERN.findall(git_config)]

    @classmethod
    def run(cls):
        opts, args = getopt(sys.argv[1:], 'sb:', ['pullsubmodule=', 'branch='])
        cls._OPTS_DICT = dict(opts)
        if '-b' in cls._OPTS_DICT:
            cls._BRANCH = cls._OPTS_DICT.get('-b')

        cls._get_submodule()
        os.system(f'git checkout {cls._BRANCH}')
        os.system('git pull')
        print('【GIT PULL MODULE DONE.】')

        if '-s' not in cls._OPTS_DICT or not cls._SUBMODULE_PATH:
            return
        os.system(f'git checkout {cls._BRANCH}')
        for submodule_path in cls._SUBMODULE_PATH:
            os.chdir(submodule_path)
            os.system('git pull')
            print(f'【PULL SUBMODULE {submodule_path} DONE.】')


if __name__ == '__main__':
    GitPull.run()
