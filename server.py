import socket, threading


server = socket.socket()
server.bind(("127.0.0.1", 65432))
server.listen()

clients = []
nicknames = []


def broadcast(msg, exclusion=None):
    """
    Рассылка сообщений всем пользователям, кроме отправителя
    """
    for client in clients:
        if client != exclusion:
            client.send(msg)


def drop_client(client):
    """
    Закрыть соединение с клиентом и удалить его в случае ошибки или получения "exit"
    """
    nickname = nicknames[clients.index(client)]
    nicknames.remove(nickname)
    clients.remove(client)
    client.close()
    print(f"{nickname} left")
    broadcast(f"*** Пользователь {nickname} покинул чат ***".encode("utf-8"))


def initialize():
    """
    Инициализация клиента, старт его потока
    """
    while True:
        # Сервер принимает соединение
        client, address = server.accept()
        print(f"Client with ip {address} has connected")
        # Запрос ника у пользователя и его сохранение
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)
        print(f"Client's nickname is {nickname}")
        broadcast(f"*** Пользователь {nickname} подключился к чату ***".encode("utf-8"), client)
        client.send("*** Вы подключились к чату ***".encode("utf-8"))
        # Старт потока для текущего пользователя
        thread = threading.Thread(target=receive, args=(client,))
        thread.start()
        
        
def receive(client):
    """
    Получение и обработка входящих сообщений
    """
    while True:
        try:
            message = client.recv(1024)
            if message.decode("utf-8").lower().split(":")[1].strip() == "exit":
                drop_client(client)
                break
            broadcast(message, client)
        except:
            drop_client(client)
            break


print("Сервер начал работу")
initialize()