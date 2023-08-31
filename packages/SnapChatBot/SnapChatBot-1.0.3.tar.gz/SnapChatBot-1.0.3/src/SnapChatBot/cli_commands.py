import os
from sys import platform

from .exceptions import ExitException


class CLICommands:
    def __init__(self, _self):
        self.self = _self

    def help(self):
        print("")
        for command in self.self.__commands__:
            print(f"{self.self.__commands__[command].get('command')} - {self.self.__commands__[command].get('description')}")
        print("")

    @staticmethod
    def clear():
        if platform == "win32":
            os.system("cls")
        else:
            os.system("clear")

    def exit(self):
        raise ExitException
