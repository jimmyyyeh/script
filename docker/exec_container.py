import sys
import os
import subprocess


class ExecContainer:
    @classmethod
    def exec_container(cls):
        args = sys.argv
        if len(args) < 2:
            sys.exit()
        name_filter = args[1]
        command = f'docker ps -f name={name_filter} --format "{{{{.Names}}}}"'
        command_list = command.split()
        container_list = subprocess.run(command_list, stdout=subprocess.PIPE).stdout.decode('utf-8')
        container_list = container_list.split('\n')[:-1]
        if not container_list:
            sys.exit('CONTAINER NOT FOUND')
        else:
            container = container_list[0]
            print(f'CONTAINER {container} FOUND')
            command = f'docker exec -it {container} bash'
            os.system(command)


if __name__ == '__main__':
    ExecContainer.exec_container()
