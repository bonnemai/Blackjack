import os
from sys import platform


def clear():
    # clear the output before
    if platform == 'darwin':
        os.system('clear')
    else:
        os.system('cls')