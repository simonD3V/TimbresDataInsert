import os
import functools

class Config(dict):
    def __init__(self, filename):
        self.filename = filename
        if os.path.isfile(filename):
            with open(filename) as f:
                # use super here to avoid unnecessary write
                super(Config, self).update(yaml.load(f) or {})

    def __setitem__(self, key, value):
        super(Config, self).__setitem__(key, value)
        with open(self.filename, "w") as f:
            yaml.dump(self, f)

    def __delitem__(self, key):
        super(Config, self).__delitem__(key)
        with open(self.filename, "w") as f:
            yaml.dump(self, f)

    def update(self, kwargs):
        super(Config, self).update(kwargs)
        with open(self.filename, "w") as f:
            yaml.dump(self, f)

def dumps(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)
        with open(self.filename, "w") as f:
            yaml.dump(self, f)
        return ret
    return wrapper

class Config(dict):
    def __init__(self, filename):
        self.filename = filename
        if os.path.isfile(filename):
            with open(filename) as f:
                # use super here to avoid unnecessary write
                super(Config, self).update(yaml.load(f) or {})

    __setitem__ = dumps(dict.__setitem__)
    __delitem__ = dumps(dict.__delitem__)
    update = dumps(dict.update)