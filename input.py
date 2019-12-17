import network

network = network.Network()
name = input("Type your name: ")


while True:
    message = input("Your message: ")
    if not message.strip() == "":
        network.send(f"{name}|{message}")