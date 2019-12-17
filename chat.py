import network
import time


network = network.Network()
network.client.setblocking(0)
#print(network.client)

while True:
    try:
        time.sleep(0.1)
        network.send(f"get.new")
        message_received = network.client.recv(2048).decode('utf-8')
        if message_received != "none":
            print(message_received)
    except Exception as E:
        pass
        #print(str(E))
