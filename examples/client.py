import socket


def client_program():
    host = "localhost"
    port = 5002  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server


    while True:
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal
        if data.lower == "terminate":
            break

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
