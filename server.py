import socket
from _thread import *
import sys
from datetime import datetime, timedelta
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8888

try:
    s.bind(('', port))
except Exception as e:
    print(str(e))
    sys.exit()

s.listen(5)
print("Server started.")

messages = []
connections = []
sync_table = []


def show_messages():
    for message in messages:
        print(f"{message[0]} {message[1]} {message[2]} {message[3]}")
        print("-----")


def get_new_messages(last_sync_time):
    for message in messages:
        if message[3] > last_sync_time:
            yield message

# receive client message
def threaded_client(conn, addr):
    conn.send(str.encode("0"))

    while True:
        try:
            print("new iteration")
            print(threading.currentThread().getName())
            #show_messages()

            message_received = conn.recv(2048).decode('utf-8')
            print("message: " + message_received)
            if len(message_received) == 0:
                continue

            print(message_received)

            is_sync_exist = False
            if message_received == "get.new":
                print("update request")
                last_sync_time = None
                for sync in sync_table:
                    if sync[0] == conn:
                        last_sync_time = sync[1]
                        is_sync_exist = True
                        break

                if len(messages) > 0:
                    print("there are messages")
                    for message in messages:
                        if last_sync_time is None or message[3] > last_sync_time:
                            client_message = f"{message[3]} {message[1]}: {message[2]}"
                            #print("before message send")
                            conn.send(str.encode(client_message))
                            #print("after message send")

                    if is_sync_exist:
                        #print("before remove sync")
                        sync_table.remove((conn, last_sync_time))

                    last_sync_time = datetime.now()
                    sync_table.append((conn, last_sync_time))
                    #print("after sync insert")
                else:
                    conn.send(str.encode("none"))
                continue



            name, message = message_received.split("|")
            message_time = datetime.now()
            #print(f"{addr} {name} {message} {message_time}")

            messages.append((addr, name, message, message_time))

            #conn.sendall(str.encode(reply))
        except Exception as e:
            print(str(e))


print(threading.currentThread().getName())

# handle new client connection
while True:
    try:
        conn, addr = s.accept()
        print(conn)
        # if (conn, addr) not in connections:
        #     connections.append((conn, addr))

    except Exception as e:
        print(str(e))

    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,addr,))
