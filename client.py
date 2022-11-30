import socket, threading


client = socket.socket()
client.connect(("127.0.0.1", 65432))

nickname = input("Выберите ник: ")

def receive():
    """
    Получение сообщений
    """
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "NICK": client.send(nickname.encode("utf-8"))
            else: print(message)
        except:
            print("Соединение с сервером прервано")
            client.close()
            break

def write():
    """
    Отправка сообщений
    """
    while True:
        message = f"{nickname}: {input()}"
        if message.lower().split(":")[1].strip() == "exit":
            client.close()
            break
        client.send(message.encode("utf-8"))

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()