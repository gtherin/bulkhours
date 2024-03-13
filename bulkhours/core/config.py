from collections import OrderedDict


# class Config(OrderedDict):
class Config:
    def __init__(self, config={}):
        # Convert from Namespace
        self.data = vars(config) if type(config) != dict else config
        if "global" not in self.data:
            self.data["global"] = {}
        if "language" in self.data["global"] and self.data["global"]["language"] != "fr":
            self.data["isfr"] = False
        else:
            self.data["isfr"] = True

    @property
    def show_help(self):
        return "help" in self.data and self.data["help"]

    def __getattr__(self, k):
        if k in ["g", "global"]:
            return self.data["global"]
        if k in ["n"]:
            return self.data[self.data["notebook_id"]]

        if k in self.data:
            return self.data[k]

        if "global" in self.data and k in self.data["global"]:
            return self.data["global"][k]

        return None

    def __setitem__(self, key, item):
        self.data[key] = item

    def __getitem__(self, key):
        if self.has_key(key):
            return self.data[key]
        else:
            return None

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return len(self.data)

    def __delitem__(self, key):
        del self.data[key]

    def clear(self):
        return self.data.clear()

    def copy(self):
        return self.data.copy()

    def has_key(self, k):
        return k in self.data

    def update(self, *args, **kwargs):
        return self.data.update(*args, **kwargs)

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()

    def pop(self, *args):
        return self.data.pop(*args)

    def __cmp__(self, dict_):
        return self.data(self.data, dict_)

    def __contains__(self, item):
        return item in self.data

    def __iter__(self):
        return iter(self.data)
