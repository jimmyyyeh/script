import os


class KillContainers:
    _SKIP_CONTAINERS = ['minikube']

    @classmethod
    def run(cls):
        container_list = os.popen(
            'docker ps --format "{{.Names}}:{{.ID}}"').readlines()
        container_dict = dict((container.strip().split(':'))
                              for container in container_list)
        killed_id = ' '.join(
            [id_ for name, id_ in container_dict.items() if name not in cls._SKIP_CONTAINERS])
        os.system(f'docker kill {killed_id}')


if __name__ == '__main__':
    KillContainers.run()
