import os
import sys
import re
from getopt import getopt


class GitPull:
    _OPTS_DICT = None
    _BRANCH = 'develop'
    _MODULE_PATH = os.getcwd()
    _SUBMODULE_PATH = None
    _SUBMODULE_PATTERH = re.compile(r'\[submodule "(.+)"\]')

    @classmethod
    def _get_submodule(cls):
        git_config_path = os.path.join(cls._MODULE_PATH, '.git/config')
        with open(git_config_path, 'r') as f:
            git_config = f.read()
        submodule = cls._SUBMODULE_PATTERH.search(git_config).group(1) \
            if cls._SUBMODULE_PATTERH.search(git_config) else None
        if submodule:
            cls._SUBMODULE_PATH = os.path.join(cls._MODULE_PATH, submodule)

    @classmethod
    def run(cls):
        opts, args = getopt(sys.argv[1:], 'sb:', ['pullsubmodule=', 'branch='])
        cls._OPTS_DICT = dict((opt) for opt in opts)
        if '-b' in cls._OPTS_DICT:
            cls._BRANCH = cls._OPTS_DICT.get('-b')

        cls._get_submodule()
        os.system(f'git checkout {cls._BRANCH}')
        os.system('git pull')
        print('【GIT PULL MODULE DONE.】')

        if '-s' not in cls._OPTS_DICT or not cls._SUBMODULE_PATH:
            return
        os.system(f'git checkout {cls._BRANCH}')
        os.chdir(cls._SUBMODULE_PATH)
        os.system('git pull')
        print('【GIT PULL SUBMODULE DONE.】')


if __name__ == '__main__':
    GitPull.run()
