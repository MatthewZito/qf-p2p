class Vault(object):
    def __init__(self):
        self.__vault = {}

    def get(self, key):
        return self.__vault.get(key)

    def set(self, key, value):
        self.__vault[key] = value
        return 1

    def delete(self, key):
        if key in self.__vault:
            del self.__vault[key]
            return 1
        return 0

    def flush(self):
        kvlen = len(self.__vault)
        self.__vault.clear()
        return kvlen

    def mget(self, *keys):
        return [self.__vault.get(key) for key in keys]

    def mset(self, *items):
        data = zip(items[::2], items[1::2])
        for key, value in data:
            self.__vault[key] = value
        return len(data)