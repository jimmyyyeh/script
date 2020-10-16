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
from time import sleep
from pathlib import Path


class BuildScreen:
    _HOME_DIR = str(Path.home())
    _BUILD_DICT = {'project_name': {'title': 'entrypoint.py'}}
    _MENU_DICT = dict((index, project)
                      for index, project in enumerate(_BUILD_DICT))
    _OPTS = list()

    @classmethod
    def _valid_project(cls, project_str):
        pattern = re.compile(r'([\d]+,)*[\d]+')
        if not pattern.fullmatch(project_str):
            return None
        input_list = [int(num.strip()) for num in project_str.split(',')]
        project_list = list()
        for num in input_list:
            if num not in cls._MENU_DICT:
                return None
            project_list.append(cls._MENU_DICT.get(num))
        return project_list

    @classmethod
    def _select_project(cls):
        print('=' * 50)
        for index, project in sorted(cls._MENU_DICT.items(), key=lambda x: x[0]):
            print(index, project)
        print('=' * 50)

        project_str = input(
            'Please enter which project you want to build, (Use "," to split if you want to build multiple projects).\n'
            'If you want to build all above, please press ENTER directly:\n')
        if project_str == '':
            return list(cls._BUILD_DICT.keys())
        project_list = cls._valid_project(project_str)
        return project_list

    @classmethod
    def _init_screen(cls, project):
        # kill exists screen
        os.system(f'screen -X -S {project} quit')
        # create new screen
        os.system(f'screen -dmS {project}')
        # kill all containers
        os.system(
            f"docker ps -a -q --filter='name=.*{project}.*' | xargs docker rm -f")
        # run docker-compose
        if '-p' in cls._OPTS:
            cls._run_script_in_screen(
                screen_name=project, title=0, command=f'gitpullall')
            print('GIT PULL DONE')
        if '-d' in cls._OPTS:
            cls._run_script_in_screen(
                screen_name=project, title=0, command=f'docker-compose up -d')
            sleep(5)
        else:
            cls._run_script_in_screen(
                screen_name=project, title=0, command=f'docker-compose up')
            sleep(5)
        print('DOCKER COMPOSE UP DONE')

    @classmethod
    def _run_script_in_screen(cls, screen_name, title, command):
        os.system(
            f'screen -x -S {screen_name} -p {title} -X stuff "{command}"')
        os.system(f'screen -x -S {screen_name} -p {title} -X stuff "\n"')

    @classmethod
    def _build_project(cls, project):
        project_path = os.path.join(cls._HOME_DIR, project)
        project_setting = cls._BUILD_DICT.get(project)
        os.chdir(project_path)
        cls._init_screen(project=project)
        if not project_setting:
            return
        for title, entrypoint in project_setting.items():
            # create screen window with title
            os.system(f'screen -S {project} -X screen -t {title}')
            # run command in container
            cls._run_script_in_screen(
                screen_name=project, title=title, command=f'docker exec -it {project} sh')
            cls._run_script_in_screen(
                screen_name=project, title=title, command=f'python {entrypoint}')
            print(f'EXECUTE {entrypoint} FINISHED')

    @classmethod
    def run(cls):
        opts, args = getopt(sys.argv[1:], 'hpd', [
                            'help', 'gitpull', 'detached'])
        cls._OPTS = [opt[0] for opt in opts]

        project_list = cls._select_project()
        for project in project_list:
            for i in range(5):
                print(f'COUNTDOWN {5-i} SECONDS FOR BUILDING {project}')
                sleep(1)
            cls._build_project(project=project)


if __name__ == '__main__':
    BuildScreen.run()
