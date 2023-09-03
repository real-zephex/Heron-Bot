import time
import os
from termcolor import colored

def clear(arg):
    os.system("clear")
    for char in arg:
        print(colored(char, color="magenta", attrs=["bold"]), end="")
        time.sleep(0.03)