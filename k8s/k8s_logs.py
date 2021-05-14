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


class GetLogs:
    """
        【USAGE】
            python3 k8s_logs.py -p [pods name pattern]
                                -n [tail lines want to print]
                                -f follow
        【EXAMPLE】
            python3 k8s_logs.py -p demo -n 5

            It will show tail 5 lines of logs with k8s pods match name pattern [.*demo.*]
            by paragraph, you need to press enter to show next pod log.
    """
    _OPTS = dict()

    @staticmethod
    def _get_pods_list(pod_pattern):
        grep_str = "kubectl get pods --template " \
                   "'{{{{range .items}}}}{{{{.metadata.name}}}}{{{{\"\\n\"}}}}{{{{end}}}}' |" \
                   " grep {pod_pattern}".format(pod_pattern=pod_pattern)
        pods_output = os.popen(grep_str).read()
        if not pods_output:
            sys.exit('pods not found')
        pods_list = pods_output.strip().split('\n')
        return pods_list

    @staticmethod
    def _get_pod_logs(pod, line_nums, follow):
        if follow is None:
            log_str = f'kubectl logs {pod}'
            pod_log = os.popen(log_str).read().strip()
            pod_log = pod_log.split('\n')
            print('\n'.join(pod_log[-line_nums:]))
            input()
        else:
            log_str = f'kubectl logs {pod} -f'
            os.system(log_str)

    @classmethod
    def run(cls):
        try:
            opts, argv = getopt(sys.argv[1:], 'p:n:f', ['pod=', 'num='])
        except GetoptError:
            sys.exit(cls.__doc__)
        cls._OPTS = dict((opt[0], opt[1]) for opt in opts)
        if not set(cls._OPTS).intersection({'-p'}):
            sys.exit(cls.__doc__)
        pod_pattern = cls._OPTS['-p']
        follow = cls._OPTS.get('-f')
        try:
            line_nums = cls._OPTS.get('-n', 100)
            line_nums = int(line_nums)
        except ValueError:
            sys.exit(cls.__doc__)
        pods_list = cls._get_pods_list(pod_pattern=pod_pattern)

        for pod in pods_list:
            print(f'{"="*50} {pod} log {"="*50}')
            cls._get_pod_logs(pod=pod, line_nums=line_nums, follow=follow)


if __name__ == '__main__':
    GetLogs.run()
