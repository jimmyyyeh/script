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
from getopt import getopt, GetoptError


class KubeLog:
    """
        【USAGE】
            python3 kube_log.py -p [pods name pattern]
                                -n [tail lines want to print]
                                -f follow
                                -a all
        【EXAMPLE】
            python3 kube_log.py -p demo -n 5

            It will show tail 5 lines of logs which name with [.*demo.*] pattern
            by paragraph, you need to press enter to show next pod log.
    """

    def __init__(self):
        self.required_arg = {'-p'}
        self.opts = self._set_opts()

    def _set_opts(self):
        try:
            opts, argv = getopt(sys.argv[1:], 'p:n:fa', ['pod=', 'num=', 'follow=', 'all='])
        except GetoptError:
            sys.exit(self.__doc__)
        opts = dict((opt[0], opt[1]) for opt in opts)
        return opts

    def _check_argument(self):
        if set(self.opts) - self.required_arg:
            sys.exit(self.__doc__)

    @staticmethod
    def _get_pod_logs(pod, nums, follow):
        if follow is None:
            log_str = f'kubectl logs {pod}'
            pod_log = os.popen(log_str).read().strip()
            pod_log = pod_log.split('\n')
            print('\n'.join(pod_log[-nums:]))
            input()
        else:
            log_str = f'kubectl logs {pod} -f'
            os.system(log_str)

    def main(self):
        pod_pattern = self.opts['-p']
        follow = self.opts.get('-f')
        all_ = self.opts.get('-a')
        try:
            nums = self.opts.get('-n', 100)
            nums = int(nums)
        except ValueError:
            sys.exit(self.__doc__)
        if all_:
            command = f'kubectl get pods -o=name --all-namespaces | grep {pod_pattern}'
        else:
            command = f'kubectl get pods -o=name | grep {pod_pattern}'
        pod_list = os.popen(command).readlines()
        pod_list = [pod.strip() for pod in pod_list]

        for pod in pod_list:
            print(f'{"=" * 50} {pod} log {"=" * 50}')
            self._get_pod_logs(pod=pod, nums=nums, follow=follow)


if __name__ == '__main__':
    KubeLog().main()
