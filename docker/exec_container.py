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
import re


class ExecContainer:
    @classmethod
    def exec_container(cls):
        command = 'docker ps --format "{{.Names}}"'
        exclude_prefix_list = ['k8s.*', 'pycharm.*']
        exclude_pattern = re.compile(rf'{"|".join(exclude_prefix_list)}')
        container_list = list()
        for container in os.popen(command).readlines():
            if exclude_pattern.search(container):
                continue
            container_list.append(container.strip())
        container_list = sorted(container_list)
        menu_str = '\n'.join([f'【{index + 1}.】 {container}' for index, container in enumerate(container_list)])
        input_index = input(f'ENTER CONTAINER NUM:\n'
                            f'========================================\n'
                            f'{menu_str}\n'
                            f'========================================\n')
        selected_container = container_list[int(input_index) - 1]
        print(f'EXEC DOCKER CONTAINER {selected_container}')
        os.system(f'docker exec -it {selected_container} bash')


if __name__ == '__main__':
    ExecContainer.exec_container()
