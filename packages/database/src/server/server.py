from gevent import socket
from gevent.pool import Pool
from gevent.server import StreamServer

from socket import error as socket_error

from constants.errors import *
from constants.commands_enum import commands

from protocol_handler import ProtocolHandler
from store.vault import Vault

class Server(object):
    def __init__(self, host="127.0.0.1", port=31337, max_clients=64):
        self.pool = Pool(max_clients)
        self.server = StreamServer(
            (host, port),
            self.connection_handler,
            spawn=self.pool)

        self.protocol = ProtocolHandler()
        self.vault = Vault()
        
        self.commands = self.get_commands()

    def get_commands(self):
        return {
            commands["GET"]: self.vault.get,
            commands["SET"]: self.vault.set,
            commands["DEL"]: self.vault.delete,
            commands["FLUSH"]: self.vault.flush,
            commands["MG"]: self.vault.mget,
            commands["MS"]: self.vault.mset
        }

    # handle commands from client
    def get_response(self, data):
        if not isinstance(data, list):
            try:
                data = data.decode().split()
            except:
                raise CommandError("[-] Request must be list or simple string")
        
        if not data:
            raise CommandError("[-] A command is required")

        command = data[0].upper()
        if command not in self.commands:
            raise CommandError("[-] Unrecognized command %s" % command)    
        else:
            return self.commands[command](*data[1:])

    def connection_handler(self, conn, address):
        # Convert "conn" (a socket object) into a file-like object.
        file = conn.makefile("rwb")

        # Process client requests until client disconnects.
        while True:
            try:
                data = self.protocol.handle_request(file)
            except Disconnect:
                break

            try:
                response = self.get_response(data)
            except CommandError as exc:
                response = Error(exc.args[0])

            self.protocol.write_response(file, response)

    def run(self):
        self.server.serve_forever()