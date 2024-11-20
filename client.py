import socket
import threading
from xmlrpc.client import ServerProxy

class ChatClient:
    def __init__(self, nickname, host="127.0.0.1", port=12345):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.nickname = nickname
        
        # Sending the nickname to the server
        self.client.send(self.nickname.encode())

        # Start threads for receiving and sending messages
        threading.Thread(target=self.receive_messages).start()
        threading.Thread(target=self.send_messages).start()
        
    def receive_messages(self):
        """Continuously listen for messages from the server."""
        while True:
            try:
                message = self.client.recv(1024).decode()
                print(message)
            except:
                print("An error occurred!")
                self.client.close()
                break

    def send_messages(self):
        """Send messages to the server."""
        while True:
            message = f"{self.nickname}: {input('')}"
            self.client.send(message.encode())

if __name__ == "__main__":
    nickname = input("Choose your nickname: ")
    ChatClient(nickname)
