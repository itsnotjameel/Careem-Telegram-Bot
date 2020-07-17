import platform
def back_or_forward_slash(directory, filename):
    if platform.system() == "Windows":
        return r"{directory}\{filename}".format(directory=directory, filename=filename)
    elif platform.system() != "Windows":
        return r"{directory}/{filename}".format(directory=directory, filename=filename)