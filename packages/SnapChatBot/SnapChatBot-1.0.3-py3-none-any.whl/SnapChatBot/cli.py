from .snapchat import SnapChat
from .cli_commands import CLICommands
from .exceptions import ExitException, ExitFunctionException
from .functions import get_funtion_arguments


class CLI:
    def __init__(self, snapchat: SnapChat):
        self.snapchat = snapchat

    def __call__(self, *args, **kwargs):
        self.__commands__ = {}
        self.__cli_commands__ = CLICommands(self)

        self.add_command("add", "add an account", self.snapchat.add_account)
        self.add_command("run", "run the bot", self.snapchat.run)
        self.add_command("check", "check accounts", self.snapchat.check_accounts)
        self.add_command("open", "opens web.snapchat.com with the selected account session to change settings, ...", self.snapchat.open)
        self.add_command("remove", "remove an account", self.snapchat.remove_account)
        self.add_command("list", "returns a list of all accounts", self.snapchat.list_accounts)
        self.add_command("clear", "clears the console", self.__cli_commands__.clear)
        self.add_command("exit", "exits the console", self.__cli_commands__.exit)
        self.add_command("help", "list of all commands", self.__cli_commands__.help)

        # TODO: add a alias list to add_command to add aliases for a command

        self.__cli_commands__.clear()

        while True:
            try:
                self._await_command()
            except KeyboardInterrupt:
                print("")
            except ExitException:
                break
            except ExitFunctionException:
                pass

        return self

    def add_command(self, command: str, description: str, action):
        if command in self.__commands__:
            raise ValueError(f"Command {command} already exists.")

        if not callable(action):
            raise ValueError("Action must be a callable function.")

        self.__commands__[command] = {"command": command, "description": description, "action": action}
        return True

    def _await_command(self):
        while True:
            cmd = input("SnapChatBot ~ % ").split()
            if not cmd:
                continue
            if cmd[0] in self.__commands__:
                command = self.__commands__.get(cmd[0])
                action = command.get("action")

                cmd.pop(0)

                arguments = get_funtion_arguments(action)
                # if the function takes arguments
                if len(arguments) > 0:
                    # if the function takes more arguments then given
                    if len(arguments) > len(cmd):
                        print("")
                        print(f"Required arguments: {list(arguments.keys())}")
                        print(f"   Given arguments: {cmd}")
                        print("")
                        continue

                    # if more arguments are given, then the function takes
                    elif len(arguments) < len(cmd):
                        print("")
                        print(f"Required arguments: {list(arguments.keys())}")
                        print(f"   Given arguments: {cmd}")
                        print("")
                        continue

                    # elif len(arguments) == len(cmd):
                    #     print("")

                continue_bool = False
                args = []

                for _ in range(len(cmd)):
                    command = list(arguments.keys())[_]
                    annotation = arguments.get(command).get("annotation")

                    try:
                        args.append(annotation(cmd[_]))
                    except ValueError:
                        print(f"Value \"{cmd[_]}\" must be a {annotation}")
                        continue_bool = True

                if continue_bool:
                    print("")
                    continue

                try:
                    action(*args)
                except ExitException:
                    self.__cli_commands__.exit()
                # except Exception as e:
                #     print(f"Exception: {e}\n")
