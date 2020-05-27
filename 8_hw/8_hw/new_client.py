import socket
import random
from queue import Queue
import threading

hostname, sld, tld, port = 'www', 'integralist', 'co.uk', 80
target = '{}.{}.{}'.format(hostname, sld, tld)

API_WG = 'https://api.worldoftanks.ru/wot/account/achievements/'
URLS_AMOUNT = 103
APP_ID = 'application_id=e7c327f37d873eaf7895b497a5e260ae'

urls = Queue()


def get_urls(urls, start):
    for idx in range(start, start + URLS_AMOUNT):
        urls.put(f'{API_WG}?{APP_ID}&account_id={idx}')
    return urls


def send_request_full():
    global urls
    while not urls.empty():
        send_request()


threads = [threading.Thread(target=send_request_full) for i in range(5)]


def send_request():
    global urls
    if not urls.empty():
        # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect the client
        # client.connect((target, port))
        client.connect(('0.0.0.0', 9999))
        client.send(urls.get().encode('utf-8'))
        response = client.recv(40960)
        print(response[:70])
    elif urls.empty():
        print('ОЧЕРЕДЬ ПУСТАЯ')


st = random.randint(1, 100000000)
urls = get_urls(urls, st)

for thread in threads:
    thread.start()

while not urls.empty():
    pass

for thread in threads:
    thread.join()
