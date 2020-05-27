import time
import asyncio
import aiohttp
from aiofile import AIOFile
from multiprocessing import Process, Queue


queue = Queue()


def serve_forever():

    while True:
        write()

def write():
    global queue
    while not queue.empty():
        name, data = queue.get()
        print('Начал записывать в файл')
        with open(name, 'wb') as file:
            file.write(data)
        print('Закончил записывать в файл')


async def writing(data):
    """Запись в файл с использованием aiofile"""
    hash1 = int(time.time() * 1000)
    name = f'photo/photo_{hash1}'
    async with AIOFile(name, 'wb') as afp:
        await afp.write(data)


def write_file(data):
    """Несинхронная запись в файл БЕЗ использования aiofile"""
    hash1 = int(time.time() * 1000)
    name = f'photo/photo_{hash1}'
    global queue
    queue.put((name, data))


async def fetch(url, session):
    async with session.get(url, allow_redirects=True) as resp:
        print(f'Перед fetch {url}')
        data = await resp.read()
        print(f'После fetch {url}')
        #await writing(data)
        write_file(data)


async def main():
    url = 'https://loremflickr.com/320/240'
    tasks = []
    process = Process(target=serve_forever, daemon=True)
    process.start()

    async with aiohttp.ClientSession() as session:
        for i in range(10):
            tasks.append(asyncio.create_task(fetch(url, session)))

        await asyncio.gather(*tasks)
    flag = False
    process.join(0.1)


if __name__ == '__main__':
    t1 = time.time()
    asyncio.run(main())
    t2 = time.time()

    print('TT', t2 - t1)
