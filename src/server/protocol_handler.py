from io import BytesIO

from constants.protocol_prefixes import prefixes
from constants.errors import *
from constants.char_enum import char

"""
Protocol definition
Allocates data per types system to dedicated handlers
"""
class ProtocolHandler(object):
    def __init__(self):
        self.handlers = {
            prefixes["ARRAY"]: self.handle_array,
            prefixes["DICT"]: self.handle_dict,
            prefixes["ERROR"]: self.handle_error,
            prefixes["INTEGER"]: self.handle_integer,
            prefixes["SIMPLE_STRING"]: self.handle_simple_string,
            prefixes["STRING"]:self.handle_string
        }
        
    def handle_request(self, file):
        # pull first byte to determine datatype
        prefix = file.read(1)
        if not prefix:
            raise Disconnect()

        try:
            return self.handlers[prefix](file)
        except KeyError:
            raise CommandError("invalid request")
    
    def handle_array(self, file):
        items = self.__parse_file(file)
        return [ self.handle_request(file) for _ in range(items) ]

    def handle_dict(self, file):
        items = self.__parse_file(file)
        elements = [ self.handle_request(file) for _ in range(items * 2) ]
        return dict(zip(elements[::2], elements[1::2]))

    def handle_error(self, file):
        return Error(file.readline().rstrip(char["RETURN"]))

    def handle_integer(self, file):
        return self.__parse_file(file)

    def handle_simple_string(self, file):
        return file.readline().rstrip(char["RETURN"])

    def handle_string(self, file):
        length = self.__parse_file(file)
        if length == -1:
            return None # NULL case
        length += 2
        return file.read(length)[:-2]

    def write_response(self, file, data):
        buffer = BytesIO()
        self.__write(buffer, data)
        buffer.seek(0)
        file.write(buffer.getvalue())
        file.flush()

    def __write(self, buffer, data):
        if isinstance(data, str):
            data = data.encode("utf-8")

        if isinstance(data, bytes):
            buffer.write(f"${len(data)}\r\n{data}\r\n")
        elif isinstance(data, int):
            buffer.write(f":{data}\r\n")
        elif isinstance(data, Error):
            buffer.write(f"-{error.message}\r\n")
        elif isinstance(data, (list, tuple)):
            print(data)
            buffer.write(f"*{len(data)}\r\n")
            for item in data:
                self.__write(buffer, item)
        elif isinstance(data, dict):
            buffer.write("%%%s\r\n" % len(data))
            for key in data:
                self.__write(buffer, key)
                self.__write(buffer, data[key])
        elif data is None:
            buffer.write("$-1\r\n")
        else:
            raise CommandError("[-] Unrecognized type: %s" % type(data))

    def __parse_file(file):
        return int(file.readline().rstrip(char["RETURN"]))
