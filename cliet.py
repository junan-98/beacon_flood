import socket

# 접속 정보 설정
SERVER_IP = '127.0.0.1'
SERVER_PORT = 1235
SIZE = 1024
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

# 클라이언트 소켓 설정
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(SERVER_ADDR)
    while True:
        ssid = input("Input SSID: ")
        client_socket.send(ssid.encode())