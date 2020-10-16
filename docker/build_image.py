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


class BuildImage:
    _REGISTRY_HOST = 'registry.feiwalk.com.tw'

    @classmethod
    def build(cls):
        project_path = os.getcwd()
        os.chdir(project_path)
        project_name = os.path.basename(project_path)
        tag = input("PLEASE INPUT YOUR TAG:")
        print(f'BUILDING DOCKER IMAGE : {project_name} WITH TAG {tag}')
        os.system(f'docker build -t {project_name} . --no-cache')
        os.system(f'docker tag {project_name} {cls._REGISTRY_HOST}/{project_name}:{tag}')
        os.system(f'docker push {cls._REGISTRY_HOST}/{project_name}:{tag}')
        os.system(f'docker tag {project_name} {cls._REGISTRY_HOST}/{project_name}:latest')
        os.system(f'docker push {cls._REGISTRY_HOST}/{project_name}:latest')


if __name__ == '__main__':
    BuildImage.build()
