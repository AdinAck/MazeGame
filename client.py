import threading
import socket
from typing import *


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Configurable constants
        self.BUF_SIZE = 2048
        self.lock = threading.Lock()

        self.commandDict: Dict[str, int] = {
            'new-player': 0x10,
            'update-coords': 0x20,
            'request-coords': 0x21,
            'remove-player': 0x30,
            'send-grid': 0x40,
            'no-op': 0xFFFF
        }

    def connect(self, ip, port=1234):
        try:
            self.s.connect((ip, port))
        except TimeoutError as e:
            del self
            return

        self.running = True

        threading.Thread(
            target=self._keepalive,
            daemon=True
        ).start()

    def transact(self, word, data=None):
        assert type(word) == str, "Word must be of type 'str'"
        assert data is None or type(
            data) == bytes, "Data must be of type 'None' or 'bytes'"
        try:
            with self.lock:
                # Transmit
                self.s.send(int.to_bytes(self.commandDict[word], 2, 'big'))

                if data != None:
                    # self.s.send(int.to_bytes(len(data), 2, 'big'))
                    self.s.send(data)

                # Receive
                result = int.from_bytes(self.s.recv(2), 'big')

            return result
        except Exception as e:
            return str(e)

    def _keepalive(self):
        try:
            while True:
                sleep(3)
                with self.lock:
                    if not self.running:
                        return
                    self.s.send(int.to_bytes(
                        self.commandDict['no-op'], 2, 'big'))
        except Exception as e:
            statusTextVar.set(str(e))
