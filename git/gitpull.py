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
    _MODULE_PATH = os.getcwd()
    _SUBMODULE_PATH = list()

    @classmethod
    def _get_submodule(cls):
        command = "git config --file .gitmodules --get-regexp path | awk '{ print $2 }'"
        submodule_list = os.popen(command).readlines()
        cls._SUBMODULE_PATH = [os.path.join(cls._MODULE_PATH, submodule.strip()) for submodule in submodule_list]

    @classmethod
    def run(cls):
        opts, args = getopt(sys.argv[1:], 'sb:', ['pullsubmodule=', 'branch='])
        cls._OPTS_DICT = dict(opts)
        cls._BRANCH = cls._OPTS_DICT.get('-b', 'develop')

        os.system(f'git checkout {cls._BRANCH}')
        os.system('git pull')
        print('【GIT PULL MODULE DONE.】')

        if '-s' not in cls._OPTS_DICT:
            return
        cls._get_submodule()
        os.system(f'git checkout {cls._BRANCH}')
        for submodule_path in cls._SUBMODULE_PATH:
            os.chdir(submodule_path)
            os.system('git pull')
            print(f'【PULL SUBMODULE {submodule_path} DONE.】')


if __name__ == '__main__':
    GitPull.run()
