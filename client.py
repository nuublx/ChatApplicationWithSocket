import socket
import threading

HOST = '127.0.0.1'
PORT = 1234


def receive_messages(client, username):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message:
            user, content = message.split('~')
            if user != username:
                print(f'\n{message}')


def chat(client):
    while True:
        message = input()
        if message:
            client.sendall(message.encode())


def send_username(client):
    username = input("Enter username: ")
    while username == "":
        print("Username cannot be empty, try again!")
        username = input("Enter username: ")
    client.sendall(username.encode())
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
    client = connect_to_server()
    if client is not None:
        username = send_username(client)

        threading.Thread(target=receive_messages, args=(client, username)).start()

        chat(client)


if __name__ == "__main__":
    main()
