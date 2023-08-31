from sys import platform

from pyvirtualdisplay import Display

from .snapchat import SnapChat
from .cli import CLI


# TODO: make an "API" for adding own commands / features
# TODO: check command check is some object exists before saying that it is logged in because if your internet is to slow it might not be redirected fast enough
# TODO: run command add something to skip the account validation process / create a method to save the status and the unix when tested to only run if age is higher then x
# TODO: add a mechanism to check if window is out of focus and if true do something to regain focus
# TODO: add debugging features

# TODO: cli parsing arguments make arg_bool=True possible


class SnapChatBot:
    def __init__(self):
        self.snapchat = SnapChat()

        self.cli = CLI(self.snapchat)

        # create virtual display  # TODO: make it runnable on docker container with a virtual display
        if platform == "linux":
            self.__display__ = Display(visible=False, size=(1920, 1080))
            self.__display__.start()
