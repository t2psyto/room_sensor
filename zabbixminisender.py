import socket
import time
import json

class ZabbixMiniSender():
    log = True

    def __init__(self, host='127.0.0.1', port=10051):
        self.address = (host, port)
        self.data    = []

    def __log(self, log):
        if self.log: print(log)

    def __connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(self.address)
        except:
            raise Exception("Can't connect server.")

    def __close(self):
        self.sock.close()


    def add(self, host, key, value, clock=None):
        if clock is None: clock = int(time.time())
        self.data.append({"host":host, "key":key, "value":value, "clock":clock})

    def send(self):
        if not self.data:
            self.__log("Not found sender data, end without sending.")
            return False

        self.__active_checks()
        request  = {"request":"sender data", "data":self.data}
        response = self.__request(request)
        result   = True if response['response'] == 'success' else False

        if result:
            for d in self.data:
                self.__log("[send data] %s" % d)
            self.__log("[send result] %s" % response['info'])
        else:
            raise Exception("Failed send data.")

        return result
