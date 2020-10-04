from gevent import socket

from constants.commands_enum import commands
from constants.errors import Error, CommandError

from server.protocol_handler import ProtocolHandler

class Client(object):
    def __init__(self, host="127.0.0.1", port=31337):
        self.protocol = ProtocolHandler()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))
        self.file = self.conn.makefile("rwb")

    def execute(self, *args):
        self.protocol.write_response(self.file, args)
        response = self.protocol.handle_request(self.file)

        if isinstance(response, Error):
            raise CommandError(response.message)
        print(response)
    
    def get(self, key):
        return self.execute(commands["GET"], key)

    def set(self, key, value):
        return self.execute(commands["SET"], key, value)

    def delete(self, key):
        return self.execute(commands["DEL"], key)

    def flush(self):
        return self.execute(commands["FLUSH"])

    def mget(self, *keys):
        return self.execute(commands["MG"], *keys)

    def mset(self, *items):
        return self.execute(commands["MS"], *items)