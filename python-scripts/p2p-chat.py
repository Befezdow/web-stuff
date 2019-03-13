import socket
import threading
import select
import time


class Chat_Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = None
        self.conn = None
        self.addr = None

    def run(self):
        HOST = ''
        PORT = 1776
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))
        s.listen(1)
        self.conn, self.addr = s.accept()
        # Select loop for listen
        self.running = True
        while self.running == True:
            inputready,outputready,exceptready = select.select ([self.conn],[self.conn],[])
            for input_item in inputready:
                # Handle sockets
                data = self.conn.recv(1024)
                if data:
                    print("Them: " + data.decode())
                else:
                    break
            time.sleep(0)

    def kill(self):
        self.running = False


class Chat_Client(threading.Thread):
    def __init__(self, host_to_connect):
        threading.Thread.__init__(self)
        self.sock = None
        self.running = None
        self.host = host_to_connect
        self.messages_to_send = []

    def run(self):
        PORT = 1776
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, PORT))
        # Select loop for listen
        self.running = True
        while self.running == True:
            for msg in self.messages_to_send:
                self.sock.sendall(msg.encode())
            self.messages_to_send = []
            time.sleep(0)

    def kill(self):
        self.running = False

    def send_message(self, msg):
        self.messages_to_send.append(msg)


def main():
    app_type = input('Are you server?\n').lower()

    if app_type in ['y', 'yes', 'д', 'да']:
        print('Listening...\n')
        chat_server = Chat_Server()
        chat_server.start()

        while(True):
            s = input()
            if s == 'exit':
                exit(0)
    else:
        ip = input('Server IP: ')
        chat_client = Chat_Client(ip)
        chat_client.start()

        while(True):
            s = input()
            if s == 'exit':
                exit(0)
            else:
                chat_client.send_message(s)

if __name__ == "__main__":
    main()

