import threading
import socket
import select

class Player:
    def __init__(self, sock, addr, name="UNKNOWN"):
        self.sock, self.addr, self.name = sock, addr, name
        self.x, self.y = 0, 0
        self.dx, self.dy = 0, 0

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 8082))
        self.s.listen()

        self.client_threads = []
        self.players = []

        while True:
            clientsocket, address = self.s.accept()
            print(f"[INFO] Connection from {address} has been established.")
            self.players.append(Player(clientsocket, address))
            self.client_threads.append(threading.Thread(target=self.client, args=[self.players[-1]]))
            self.client_threads[-1].start()

    def client(self, player):
        while True:
            try:
                data = player.sock.recv(1024)
            except ConnectionResetError:
                print(f"[INFO] {player.addr} disconnected.")
                return

if __name__ == "__main__":
    Server()
