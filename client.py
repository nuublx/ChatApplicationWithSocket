import socket
import threading
import rsa

HOST = '127.0.0.1'
PORT = 1234


def receive_messages(client, username, private_key):
    while True:
        message = client.recv(2048)
        message = rsa.decrypt(message, private_key)
        if message:
            message=message.decode()
            user, content = message.split('~')
            if user != username:
                print(f'\n{message}')


def chat(client, server_key):
    while True:
        message = input()
        if message:
            message = rsa.encrypt(message.encode(), server_key)
            client.sendall(message)


def send_username(client, public_key):
    username = input("Enter username: ")
    while username == "":
        print("Username cannot be empty, try again!")
        username = input("Enter username: ")
    client.sendall(username.encode())
    client.sendall(public_key.save_pkcs1("PEM"))
    return username


def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print("Connected Successfully")
        return client
    except:
        print("Server is unavailable")
    return None


def main():
    public_key, private_key = rsa.newkeys(1024)
    client = connect_to_server()
    if client is not None:
        username = send_username(client, public_key)

        server_key = client.recv(1024)
        server_key = rsa.PublicKey.load_pkcs1(server_key)

        threading.Thread(target=receive_messages, args=(client, username, private_key)).start()

        chat(client, server_key)


if __name__ == "__main__":
    main()
