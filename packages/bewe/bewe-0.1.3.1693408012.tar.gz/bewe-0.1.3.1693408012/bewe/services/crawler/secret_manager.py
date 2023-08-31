import os


def get_secret_tokens(name):
    if name not in os.environ:
        raise KeyError(f'{name} is not registered in secret.')
    return os.environ[name]
