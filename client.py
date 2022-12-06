import socket

host = '127.0.0.1'
port = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    while True:
        message = input("введите email") + "|" + input("введите сообщение")
        s.sendall(message.encode())
        data = s.recv(1024).decode()
        if data == 'OK':
            print('урааа')
            break
        print(data)
        print("введите заново")
