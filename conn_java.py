from itemcf import use
import socket
host = 'localhost'
port = 8890
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    sock, addr = s.accept()
    print('Connection built')
    info = sock.recv(1024)
    if info != None:
        result = use(str(info.decode()))
        sock.send(result.encode())
        sock.close()
    if info == 'exit':
        break




