import socket
import threading
from queue import Queue
import requests
import signal
import atexit
import os

urls = Queue()

bind_ip = '0.0.0.0'
bind_port = 9999
workers_quantity = 5
urls_quantity = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections


# print('Listening on {}:{}'.format(bind_ip, bind_port))

def get_response():
    while True:
        get_response_zero()


def get_response_zero():
    global urls
    global urls_quantity
    if not urls.empty():
        elem = urls.get()
        url = elem[0]
        client_sock = elem[1]
        resp = requests.get(url).text
        client_sock.send(resp.encode('utf-8'))
        urls_quantity += 1
        client_sock.close()


workers = [threading.Thread(target=get_response) for i in range(workers_quantity)]
for worker in workers:
    worker.start()


def finish_work(*args):
    global workers
    global urls_quantity
    for worker in workers:
        worker.join(1)
    print(f"Всего за время работы было обработано {urls_quantity} URL'ов")
    os.kill(os.getpid(), signal.SIGKILL)


atexit.register(finish_work)
signal.signal(signal.SIGUSR1, finish_work)
signal.signal(signal.SIGTERM, finish_work)
signal.signal(signal.SIGINT, finish_work)


def handle_client_connection(client_socket):
    global urls
    request = client_socket.recv(1024)
    urls.put((request.decode('utf-8'), client_socket))


def serve_forever():
    while True:
        client_sock, address = server.accept()
        # print('Accepted connection from {}:{}'.format(address[0], address[1]))
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()


if __name__ == '__main__':
    serve_forever()
