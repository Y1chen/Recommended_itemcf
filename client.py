import socket
s = socket.socket()
host = socket.gethostname()
port = 8890
s.connect((host, port))
print('Linked')
info = ''
while True:
    send_mes = input("input your message\r\n")
    s.send(send_mes.encode())
    if send_mes =='exit':
        break
    info = s.recv(1024)
    print('receive:' + info.decode())
s.close()