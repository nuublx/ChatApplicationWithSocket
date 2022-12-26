import socket
import threading
import rsa

HOST = '127.0.0.1'
PORT = 1234
LISTENERS_LIMIT = 4
current_users = []

server_public_k, server_private_k = rsa.newkeys(1024)


def send_key(client):
    client.sendall(server_public_k.save_pkcs1("PEM"))


def send_message(client, message, key):
    message = rsa.encrypt(message.encode(), key)
    client.sendall(message)


def listen_for_messages(client, username):
    while True:
        message = client.recv(2048)
        print(message)
        message = rsa.decrypt(message, server_private_k)
        print(message)
        message = message.decode()
        if message:
            message = username + '~' + message
            send_messages_to_all(message)
        else:
            print(f'*Empty message* from {username}')


def send_messages_to_all(message):
    for user in current_users:
        send_message(user[1], message, user[2])


def client_handle(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username:
            pk = client.recv(1024)
            pk = rsa.PublicKey.load_pkcs1(pk)
            current_users.append((username, client, pk))
            send_key(client)
            break
        else:
            print("Client username is Empty!")
    threading.Thread(target=listen_for_messages, args=(client, username)).start()


def main():
    # AF_INET -> IPV4, SOCK_STREAM ->TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print("Server is up and Running")
    except:
        print(f'Binding failed to host {HOST} and port {PORT}')

    server.listen(LISTENERS_LIMIT)
    while True:
        client, address = server.accept()
        print(f'connected Successfully to {address[0]} {address[1]}')

        threading.Thread(target=client_handle, args=(client,)).start()


if __name__ == '__main__':
    main()
