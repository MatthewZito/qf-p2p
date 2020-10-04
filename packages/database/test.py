from src.client.client import Client

if __name__ == "__main__":
    client = Client()
    client.mset('n_1', 'var_1', 'n_2', ['var_2-0', 9, 'var_2-2'], 'n_3', 'var_3')
    client.get('n_2')
    client.delete('n_1')
