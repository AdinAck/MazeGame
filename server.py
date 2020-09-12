import socket
import threading

class Player:
    def __init__(self, sock, addr, name="UNKNOWN"):
        self.sock, self.addr, self.name = sock, addr, name
        self.x, self.y = 0, 0
        self.dx, self.dy = 0, 0

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 8082))
        self.s.listen(5)
        self.s.setblocking(False)

        self.players = []

        t1 = threading.Thread(target=self.waitForConnection)
        t1.start()

        while True:
            self.distribute()

    def waitForConnection(self):
        while True:
            try:
                # now our endpoint knows about the OTHER endpoint.
                clientsocket, address = self.s.accept()
                print(f"[INFO] Connection from {address} has been established.")
                self.players.append(Player(clientsocket, address))
            except ConnectionResetError:
                print(f"[INFO] {address} has left.")
                for player in self.players:
                    if player.addr == address:
                        self.players.remove(player)
            except BlockingIOError:
                pass

    def distribute(self):
        for player in self.players:
            try:
                command = int.from_bytes(player.sock.recv(1), "little")
                if command == 0:
                    for p in [i for i in self.players if i != player and i.name != "UNKNOWN"]:
                        msg = str(p.name)+","+str(p.x)+","+str(p.y)+","+str(p.dx)+","+str(p.dy)
                        player.sock.send(bytearray([2, len(msg)]))
                        player.sock.send(msg.encode())
                        # print(f"sent {msg.encode()} to {player.name}")
                    continue
                header = int.from_bytes(player.sock.recv(1), "little")
                data = player.sock.recv(header).decode()
                if command == 4:
                    if player.name == "UNKNOWN":
                        stuff = data.split(",")
                        print(stuff)
                        # if stuff[0] in [i.name for i in self.players]:
                        #     print(f"[WARN] {player.addr} username already taken.")
                        #     player.sock.send(bytearray([6]))
                        #     continue
                        player.name = stuff[0]
                        player.color = int(stuff[1]),int(stuff[2]),int(stuff[3])
                        for _ in range(20):
                            player.sock.send(bytearray([4]))
                        print(f"[INFO] {player.addr} initialized. Name is {player.name}, color is {player.color}")
                        for p in [i for i in self.players if i != player]:
                            msg = player.name+","+str(player.color[0])+","+str(player.color[1])+","+str(player.color[2])
                            p.sock.send(bytearray([1, len(msg)]))
                            p.sock.send(msg.encode())
                            msg = p.name+","+str(p.color[0])+","+str(p.color[1])+","+str(p.color[2])
                            player.sock.send(bytearray([1, len(msg)]))
                            player.sock.send(msg.encode())

                elif command == 2: # player sends coordinates
                    stuff = data.split(",")
                    player.x, player.y = stuff[1], stuff[2]
                    player.dx, player.dy = stuff[3], stuff[4]
            except ConnectionResetError:
                self.inform(player)
            except IndexError:
                print(f"[WARN] Received bad packets from {player.name}.")
            except BlockingIOError:
                pass
            except Exception as e:
                print(f"[ERR] [{player.addr}] {e}")
                self.players.remove(player)

    def inform(self, player):
        print(f"[INFO] {player.name} has left.")
        self.players.remove(player)
        for p in [i for i in self.players if i != player]:
            try:
                p.sock.send(bytearray([3, len(player.name)]))
                p.sock.send(player.name.encode())
            except ConnectionResetError:
                self.inform(p)


if __name__ == '__main__':
    Server()
