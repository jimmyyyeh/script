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
    _MODULE_PATH = os.popen('git rev-parse --show-toplevel').read().strip()
    _SUBMODULE_PATH = list()

    @classmethod
    def _init_submodule(cls):
        git_config_path = os.path.join(cls._MODULE_PATH, '.git/config')
        if not os.popen(f'cat {git_config_path} | grep submodule').read():
            os.system('git submodule update --init --recursive')

    @classmethod
    def _get_submodule(cls):
        submodule_list = os.popen("git config --file .gitmodules --get-regexp path | awk '{ print $2 }'").readlines()
        cls._SUBMODULE_PATH = [os.path.join(cls._MODULE_PATH, submodule.strip()) for submodule in submodule_list]

    @classmethod
    def run(cls):
        opts, args = getopt(sys.argv[1:], 'sb:', ['pullsubmodule=', 'branch='])
        cls._OPTS_DICT = dict(opts)
        cls._BRANCH = cls._OPTS_DICT.get('-b', None)

        if cls._BRANCH:
            os.system(f'git checkout {cls._BRANCH}')
        os.system('git pull')
        print('【GIT PULL MODULE DONE.】')

        if '-s' not in cls._OPTS_DICT:
            return
        cls._init_submodule()
        cls._get_submodule()
        for submodule_path in cls._SUBMODULE_PATH:
            os.chdir(submodule_path)
            if cls._BRANCH:
                os.system(f'git checkout {cls._BRANCH}')
            os.system('git pull')
            print(f'【PULL SUBMODULE {submodule_path} DONE.】')


if __name__ == '__main__':
    GitPull.run()
