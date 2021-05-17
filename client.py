from threading import Thread, Lock, Condition
import socket
from queue import Queue
from commandDict import commandDict
from render import Player, win, world
from typing import *


def intToShort(x: int) -> Union[bytes, bytearray]:
    return int.to_bytes(x, 2, 'big')


def shortToInt(x: Union[bytes, bytearray]) -> int:
    return int.from_bytes(x, 'big')


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.lock = Lock()
        self.condition = Condition()

        self.lastPlayerCoords = []

        self.toSend = Queue()

    def connect(self, ip, port, players: Dict[str, Player]):
        self.players = players
        try:
            self.s.connect((ip, port))
            Thread(
                target=self.recvForever,
                daemon=True
            ).start()

            Thread(
                target=self.sendCommandQueue,
                daemon=True
            ).start()
        except TimeoutError as e:
            del self
            return

        self.running = True

    def initialize(self, x: int, y: int, name: str, color: Tuple[int, int, int]):
        self.send('new-player', data=name.encode())
        self.send(intToShort(x)+intToShort(y), header=False)
        self.send(data=bytearray(color), header=False)

    def __readExactly(self, size: int) -> bytearray:
        buf = bytearray()
        while (l := len(buf)) < size:
            buf += self.s.recv(size - l)

        return buf

    @property
    def playerCoords(self) -> list:

        return self.lastPlayerCoords

    def recvForever(self) -> None:
        try:
            while True:
                # Receive command
                command = shortToInt(self.s.recv(2))

                if command == commandDict['no-op']:
                    continue

                elif command == commandDict['update-coords']:
                    # sent by server
                    header = header = shortToInt(self.s.recv(2))
                    name = self.__readExactly(header).decode()
                    x = shortToInt(self.s.recv(2))
                    y = shortToInt(self.s.recv(2))
                    self.players[name].x = x
                    self.players[name].y = y

                    continue
                elif command == commandDict['remove-player']:
                    # sent by server
                    continue
                elif command == commandDict['new-player']:
                    # sent by server
                    header = shortToInt(self.s.recv(2))
                    name = self.__readExactly(header).decode()
                    x = shortToInt(self.s.recv(2))
                    y = shortToInt(self.s.recv(2))
                    color = (shortToInt(self.s.recv(1)),
                             shortToInt(self.s.recv(1)),
                             shortToInt(self.s.recv(1))
                             )

                    self.players[name] = Player(win, x, y, world, name, color)

                    continue
                elif command == commandDict['send-grid']:
                    # sent by server
                    continue
        except:
            pass

    def sendCommandQueue(self) -> NoReturn:
        while True:
            with self.condition:
                self.condition.wait()

            while not self.toSend.empty():
                self.send(*self.toSend.get())

    def send(self, command='', data: Optional[Union[bytes, bytearray]] = None, header=True) -> None:
        if command != '':
            self.s.send(intToShort(commandDict[command]))
        if data is not None:
            if header:
                self.s.send(intToShort(len(data)))
            self.s.send(data)
