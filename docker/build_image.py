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
from getopt import getopt


class BuildImage:

    _REGISTRY_HOST = 'registry.feiwalk.com.tw'

    @classmethod
    def build(cls):
        opts, args = getopt(sys.argv[1:], 'n:f:t:')
        opts_dict = dict(opts)
        if '-t' not in opts_dict:
            sys.exit('missing tag arguments')
        tag = opts_dict['-t']
        if '-n' and '-f' in opts_dict:
            project_name = opts_dict['-n']
            docker_file = opts_dict['-f']
        else:
            project_path = os.getcwd()
            os.chdir(project_path)
            project_name = os.path.basename(project_path)
            docker_file = None
        print(f'BUILDING PROJECT: {project_name} DOCKER IMAGE: {docker_file} WITH TAG {tag}')
        option = input('Y / N:')
        if option.lower() != 'y':
            sys.exit()
        if docker_file:
            os.system(f'docker build -t {project_name} -f {docker_file} . --no-cache')
        else:
            os.system(f'docker build -t {project_name} . --no-cache')
        os.system(f'docker tag {project_name} {cls._REGISTRY_HOST}/{project_name}:{tag}')
        os.system(f'docker push {cls._REGISTRY_HOST}/{project_name}:{tag}')
        os.system(f'docker tag {project_name} {cls._REGISTRY_HOST}/{project_name}:latest')
        os.system(f'docker push {cls._REGISTRY_HOST}/{project_name}:latest')


if __name__ == '__main__':
    BuildImage.build()
