import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ""
        self.port = 8888
        self.address = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        response = ""
        try:
            self.client.connect(self.address)
            response = self.client.recv(2048).decode()

            #print(f"Connected. id is {id}")
            #return id
        except Exception as e:
            print(str(e))

        if response != "0":
            raise Exception("Failed to connect to server.")

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            #reply = self.client.recv(2048).decode()
            #return reply
        except Exception as e:
            print(str(e))