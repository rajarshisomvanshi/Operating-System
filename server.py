import socket
import threading
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy

class ChatServer:
    def __init__(self, host="127.0.0.1", port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        
    def broadcast(self, message, _client=None):
        """Send a message to all clients except the sender"""
        for client in self.clients:
            if client != _client:
                client.send(message)

    def handle_client(self, client):
        """Handle communication with a single client"""
        while True:
            try:
                message = client.recv(1024)
                if message:
                    print(f"Broadcasting message: {message.decode()}")
                    self.broadcast(message, client)
            except:
                index = self.clients.index(client)
                nickname = self.nicknames[index]
                self.broadcast(f"{nickname} has left the chat.".encode())
                self.clients.remove(client)
                self.nicknames.pop(index)
                client.close()
                break

    def receive_clients(self):
        """Accept and handle new clients"""
        print("Server is running and waiting for connections...")
        while True:
            client, address = self.server.accept()
            print(f"Connection from {address} established.")
            client.send("NICK".encode())
            nickname = client.recv(1024).decode()
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f"Nickname of the client is {nickname}")
            self.broadcast(f"{nickname} joined the chat.".encode())
            client.send("Connected to the server.".encode())

            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

if __name__ == "__main__":
    chat_server = ChatServer()
    threading.Thread(target=chat_server.receive_clients).start()
    
    # Setting up XML-RPC server for external status check or management
    with SimpleXMLRPCServer(("127.0.0.1", 9000)) as rpc_server:
        rpc_server.register_instance(chat_server)
        print("XML-RPC Server running on port 9000...")
        rpc_server.serve_forever()
