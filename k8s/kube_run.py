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
from getopt import getopt, GetoptError


class KubeRun:
    """
        【USAGE】
            python3 kube_run.py -p [pods name pattern]
                                -a all
        【EXAMPLE】
            python3 kube_run.py -p demo -a

            It will run into pod which name with [.*demo.*] pattern.
    """
    def __init__(self):
        self.required_arg = {'-p'}
        self.opts = self._set_opts()

    def _set_opts(self):
        try:
            opts, argv = getopt(sys.argv[1:], 'p:a', ['pod=', 'all='])
        except GetoptError:
            sys.exit(self.__doc__)
        opts = dict((opt[0], opt[1]) for opt in opts)
        return opts

    def _check_argument(self):
        if set(self.opts) - self.required_arg:
            sys.exit(self.__doc__)

    @staticmethod
    def _get_pod(pod_list):
        if len(pod_list) == 1:
            pod = pod_list[0]
        else:
            menu = '\n'.join([f'【{index}】: {pod}' for index, pod in enumerate(pod_list)])
            index = input(f'{menu}\n')
            try:
                pod = pod_list[int(index)]
            except KeyError:
                sys.exit('POD INDEX ERROR')
        print(f'POD {pod} FOUND')
        return pod

    def main(self):
        pod_pattern = self.opts['-p']
        all_ = self.opts.get('-o')
        if all_:
            command = f'kubectl get pods -o=name --all-namespaces | grep {pod_pattern}'
        else:
            command = f'kubectl get pods -o=name | grep {pod_pattern}'

        pod_list = os.popen(command).readlines()
        pod_list = [pod.strip() for pod in pod_list]

        if not pod_list:
            sys.exit('POD NOT FOUND')
        else:
            pod = self._get_pod(pod_list=pod_list)
            command = f'kubectl exec -it {pod} -- bash'
            os.system(command)


if __name__ == '__main__':
    KubeRun().main()
