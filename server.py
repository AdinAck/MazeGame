from __future__ import annotations
import sys
import threading
import socket
from typing import *


class ClientHandle:
    def __init__(self, server: Server, sock: socket.socket, addr: Tuple[str, int], ID: int):
        self.server = server
        self.sock, self.addr = sock, addr
        self.sock.settimeout(10)

        self.lock = threading.Lock()
        self.frameReady = threading.Semaphore(0)

        self.ID = ID

    def main(self):
        try:
            while True:
                # Receive command
                command = int.from_bytes(self.sock.recv(2), 'big')

                self.frameReady.acquire(False)
                self.frameReady.acquire()

                if command == self.server.commandDict['no-op']:
                    continue

                elif command == self.server.commandDict['update-coords']:

                    continue
                elif command == self.server.commandDict['request-coords']:

                    continue
                elif command == self.server.commandDict['remove-player']:

                    continue
                elif command == self.server.commandDict['new-player']:

                    continue
                elif command == self.server.commandDict['send-grid']:

                    continue
        except:
            pass


class Server:
    def __init__(self, PORT: int):
        print("Server starting...")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', PORT))
        self.s.listen()
        self.futureIDs: List[int] = []
        print(f'Listenning on port {PORT}.')

        self.commandDict: Dict[str, int] = {
            'new-player': 0x10,
            'update-coords': 0x20,
            'request-coords': 0x21,
            'remove-player': 0x30,
            'send-grid': 0x40,
            'no-op': 0xFFFF
        }

        self.gameState: Dict[str, Any] = {
            'player-coords': {},
            'grid': None
        }

        self.clients: Dict[Tuple[str, int], ClientHandle] = {}

    def main(self):
        while True:
            cs, addr = self.s.accept()
            print(f'[INFO] Connection from {addr} has been established.')
            self.clients[addr] = ClientHandle(self, cs, addr, self.newID())
            threading.Thread(
                target=self.clients[addr].main,
                daemon=True
            ).start()

    def removeClient(self, client: ClientHandle):
        sys.stdout.flush()
        # Terminate client thread
        client.sock.close()
        del self.clients[client.addr]

    def newID(self):
        return len(self.clients) if not len(self.futureIDs) else self.futureIds.pop()
