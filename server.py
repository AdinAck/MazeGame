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

        self.players = []

        while True:
            clientsocket, address = self.s.accept()
            print(f"[INFO] Connection from {address} has been established.")
            self.players.append(Player(clientsocket, address))
            threading.Thread(target=self.client, args=[self.players[-1]]).start()

    def sendCoords(self, player):
        for p in [i for i in self.players if i != player and i.name != "UNKNOWN"]:
            msg = str(p.name)+","+str(p.x)+","+str(p.y)+","+str(p.dx)+","+str(p.dy)
            player.sock.send(bytearray([2, len(msg)]))
            player.sock.send(msg.encode())
            # print(f"sent {msg.encode()} to {player.name}")

    def recvCoords(self, player, data):
        stuff = data.split(",")
        player.x, player.y = stuff[1], stuff[2]
        player.dx, player.dy = stuff[3], stuff[4]

    def initialize(self, player, data):
        if player.name == "UNKNOWN":
            stuff = data.split(",")
            # if stuff[0] in [i.name for i in self.players]:
            #     print(f"[WARN] {player.addr} username already taken.")
            #     player.sock.send(bytearray([6]))
            #     continue
            player.name = stuff[0]
            player.color = int(stuff[1]),int(stuff[2]),int(stuff[3])
            print(f"[INFO] {player.addr} initialized. Name is {player.name}, color is {player.color}")
            for p in [i for i in self.players if i != player]:
                msg = p.name+","+str(p.color[0])+","+str(p.color[1])+","+str(p.color[2])
                player.sock.send(bytearray([1, len(msg)]))
                player.sock.send(msg.encode())
                # print(f"told {player.name} that {p.name} exists")
                msg = player.name+","+str(player.color[0])+","+str(player.color[1])+","+str(player.color[2])
                p.sock.send(bytearray([1, len(msg)]))
                p.sock.send(msg.encode())
                # print(f"told {p.name} that {player.name} exists")

    def client(self, player):
        while True:
            try:
                command = int.from_bytes(player.sock.recv(1), "little")
                if command == 0:
                    threading.Thread(target=self.sendCoords, args=[player]).start()
                    continue
                header = int.from_bytes(player.sock.recv(1), "little")
                data = player.sock.recv(header).decode()
                if command == 4:
                    threading.Thread(target=self.initialize, args=[player, data]).start()
                elif command == 2: # player sends coordinates
                    threading.Thread(target=self.recvCoords, args=[player, data]).start()
            except ConnectionResetError:
                threading.Thread(target=self.inform, args=[player]).start()
                return
            except IndexError:
                print(f"[WARN] Received bad packets from {player.name}.")
            except Exception as e:
                print(f"[ERR] [{player.addr}] {e}")
                self.players.remove(player)
                return

    def inform(self, player):
        try:
            self.players.remove(player)
            print(f"[INFO] {player.name} has left.")
            player.sock.close()
            for p in [i for i in self.players if i != player]:
                try:
                    p.sock.send(bytearray([3, len(player.name)]))
                    p.sock.send(player.name.encode())
                except ConnectionResetError:
                    self.inform(p)
        except ValueError:
            return

if __name__ == "__main__":
    Server()
