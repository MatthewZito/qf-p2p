class Vault(object):
    def __init__(self):
        self.vault = {}

    def get(self, key):
        return self.vault.get(key)

    def set(self, key, value):
        self.vault[key] = value
        return 1

    def delete(self, key):
        if key in self.vault:
            del self.vault[key]
            return 1
        return 0

    def flush(self):
        vault_length = len(self.vault)
        self.vault.clear()
        return vault_length

    def mget(self, *keys):
        return [ self.vault.get(key) for key in keys ]

    def mset(self, *items):
        data = zip(items[::2], items[1::2])
        for key, value in data:
            self.vault[key] = value
        return len(data)