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
from docopt import docopt


class EnterScreen:
    """
    Enter Screen

    Usage:
        enter_screen.py [<screen_name>]
        enter_screen.py -h | --help

    Options:
        -h --help   Show Usage.
    """

    @classmethod
    def _enter_screen_by_list(cls):
        screen_name_list = os.popen('screen -r |'
                                    ' awk \'/[At|De]tached/ {print $1}\' |'
                                    ' awk \'BEGIN {FS="."} {print $2}\'').readlines()
        screen_name_list = [screen_name.strip() for screen_name in screen_name_list]
        screen_name_menu = '\n'.join([f'【{index}.】 {screen_name}'
                                      for index, screen_name in enumerate(screen_name_list)])
        index = input('ENTER SCREEN NUM:\n'
                      '====================\n'
                      f'{screen_name_menu}\n'
                      f'====================\n')
        index = int(index)
        if index > len(screen_name_list):
            sys.exit()
        else:
            screen_name = screen_name_list[index]
            cls._enter_screen(screen_name=screen_name)

    @classmethod
    def _enter_screen(cls, screen_name=None):
        if not screen_name:
            screen_name = os.popen('screen -r | grep ng | awk \'{print $1}\' |'
                                   ' awk \'BEGIN {FS="."} {print $2}\'').read().strip()
        os.system(f'screen -r {screen_name}')

    @classmethod
    def main(cls):
        opts_dict = docopt(cls.__doc__, version='Enter Screen 2.0')
        if not opts_dict.get('<screen_name>'):
            cls._enter_screen_by_list()
        else:
            cls._enter_screen()


if __name__ == '__main__':
    EnterScreen.main()
