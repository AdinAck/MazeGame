from __future__ import annotations
import sys
import threading
import socket
from dataclasses import dataclass
from commandDict import commandDict
from typing import *


def intToShort(x: int) -> bytes:
    return int.to_bytes(x, 2, 'big')


def shortToInt(x: bytes) -> int:
    return int.from_bytes(x, 'big')


@dataclass
class Player:
    x = 0
    y = 0
    name = "unknown"
    color: Tuple[int, int, int] = (0, 0, 0)


class ClientHandle:
    def __init__(self, server: Server, sock: socket.socket, addr: Tuple[str, int]):
        self.server = server
        self.sock, self.addr = sock, addr
        self.sock.settimeout(10)

        self.lock = threading.Lock()

        self.player = Player()

    def __readExactly(self, size: int) -> bytearray | None:
        buf = bytearray()
        while (l := len(buf)) < size:
            buf += self.sock.recv(size - l)
            return buf

    def main(self):
        try:
            while True:
                # Receive command
                command = shortToInt(self.sock.recv(2))

                if command == commandDict['no-op']:
                    continue

                elif command == commandDict['update-coords']:
                    self.player.x = shortToInt(self.sock.recv(2))
                    self.player.y = shortToInt(self.sock.recv(2))
                    for client in (client for client in self.server.clients.values() if client != self):
                        client.send('update-coords',
                                    data=self.player.name.encode())
                        client.send(data=intToShort(
                            self.player.x), header=False)
                        client.send(data=intToShort(
                            self.player.y), header=False)

                elif command == commandDict['remove-player']:

                    continue
                elif command == commandDict['new-player']:
                    header = shortToInt(self.sock.recv(2))
                    self.player.name = self.__readExactly(header).decode()
                    self.player.x = shortToInt(self.sock.recv(2))
                    self.player.y = shortToInt(self.sock.recv(2))
                    self.player.color = (shortToInt(self.sock.recv(1)),
                                         shortToInt(self.sock.recv(1)),
                                         shortToInt(self.sock.recv(1))
                                         )
                    print(self.server.clients.values())
                    for client in (client for client in self.server.clients.values() if client != self):
                        client.send(
                            'new-player', data=self.player.name.encode())

                        client.send(data=intToShort(
                            self.player.x), header=False)
                        client.send(data=intToShort(
                            self.player.y), header=False)
                        client.send(data=bytearray(
                            self.player.color), header=False)

                        self.send(
                            'new-player', data=client.player.name.encode())
                        self.send(data=intToShort(
                            client.player.x), header=False)
                        self.send(data=intToShort(
                            client.player.y), header=False)
                        self.send(data=bytearray(
                            client.player.color), header=False)

                elif command == commandDict['send-grid']:

                    continue
        except:
            pass

    def send(self, command='', data: Optional[Union[bytes, bytearray]] = None, header=True) -> None:
        if command != '':
            self.sock.send(intToShort(commandDict[command]))
        if data is not None:
            if header:
                self.sock.send(intToShort(len(data)))
            self.sock.send(data)


class Server:
    def __init__(self, PORT: int):
        print("Server starting...")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', PORT))
        self.s.listen()
        self.futureIDs: List[int] = []
        print(f'Listenning on port {PORT}.')

        self.gameState: Dict[str, Any] = {
            'player-coords': {},
            'grid': None
        }

        self.clients: Dict[Tuple[str, int], ClientHandle] = {}

    def main(self):
        while True:
            cs, addr = self.s.accept()
            print(f'[INFO] Connection from {addr} has been established.')
            self.clients[addr] = ClientHandle(self, cs, addr)
            threading.Thread(
                target=self.clients[addr].main,

            ).start()

    def removeClient(self, client: ClientHandle):
        sys.stdout.flush()
        # Terminate client thread
        client.sock.close()
        del self.clients[client.addr]
