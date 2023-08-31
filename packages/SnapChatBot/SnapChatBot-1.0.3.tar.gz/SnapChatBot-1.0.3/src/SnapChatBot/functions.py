import inspect


def get_funtion_arguments(func: object, remove_self: bool = True):
    argspec = inspect.getfullargspec(func)

    if remove_self:
        try:
            argspec.args.remove("self")
        except ValueError:
            pass

    arg_details = {}

    # Required arguments
    for arg_name in argspec.args:
        arg_details[arg_name] = {
            "required": True,
            "default": None,
            "annotation": argspec.annotations.get(arg_name)
        }

    # Arguments with default values
    if argspec.defaults:
        for arg_name, default_value in zip(argspec.args[-len(argspec.defaults):], argspec.defaults):
            arg_details[arg_name]["required"] = False
            arg_details[arg_name]["default"] = default_value

    # Keyword-only arguments
    for arg_name in argspec.kwonlyargs:
        arg_details[arg_name] = {
            "required": True,
            "default": argspec.kwonlydefaults.get(arg_name),
            "annotation": argspec.annotations.get(arg_name)
        }

    return arg_details
