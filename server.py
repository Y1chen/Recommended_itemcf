from itemcf import use
import socket
host = socket.gethostname()
port = 8890
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
sock, addr = s.accept()
print('Connection built')
while True:
    info = sock.recv(1024)
    if info != None:
        result = use(str(info.decode()))
        sock.send(result.encode())
    if info == 'exit':
        break
sock.close()



