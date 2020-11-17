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

import sys
import os
import re
import subprocess


class ExecContainer:
    @classmethod
    def _exec_container_by_list(cls):
        command = 'docker ps --format "{{.Names}}"'
        exclude_prefix_list = ['k8s.*', 'pycharm.*']
        exclude_pattern = re.compile(rf'{"|".join(exclude_prefix_list)}')
        container_list = list()
        for container in os.popen(command).readlines():
            if exclude_pattern.search(container):
                continue
            container_list.append(container.strip())
        if not container_list:
            sys.exit('CONTAINER NOT FOUND')
        container_list = sorted(container_list)
        menu_str = '\n'.join([f'【{index}.】 {container}' for index, container in enumerate(container_list)])
        input_index = input(f'ENTER CONTAINER NUM:\n'
                            f'========================================\n'
                            f'{menu_str}\n'
                            f'========================================\n')
        input_index = int(input_index)
        if input_index > len(container_list):
            sys.exit('INDEX ERROR')
        container = container_list[input_index]
        print(f'CONTAINER {container} FOUND')
        os.system(f'docker exec -it {container} bash')

    @classmethod
    def _exec_container(cls, name_filter):
        command = f'docker ps -f name={name_filter} --format "{{{{.Names}}}}"'
        container = os.popen(command).readline().strip() if os.popen(command).readline() else None
        if not container:
            sys.exit('CONTAINER NOT FOUND')
        print(f'CONTAINER {container} FOUND')
        command = f'docker exec -it {container} bash'
        os.system(command)

    @classmethod
    def exec_container(cls):
        args = sys.argv
        if len(args) < 2:
            cls._exec_container_by_list()
        elif len(args) == 2:
            cls._exec_container(name_filter=args[1])


if __name__ == '__main__':
    ExecContainer.exec_container()
