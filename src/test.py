from client.client import Client

if __name__ == "__main__":
    client = Client()
    client.mset('k1', 'v1', 'k2', ['v2-0', 1, 'v2-2'], 'k3', 'v3')