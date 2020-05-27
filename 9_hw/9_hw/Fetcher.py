import asyncio
import aiohttp
import sys

class WargamingParser:
    class Config:
        SEMAPHORE_LIMIT = 10 if len(sys.argv) == 1 else int(sys.argv[1])
        API_WG = 'https://api.worldoftanks.ru/wot/account/achievements/'
        URLS_AMOUNT = 100
        APP_ID = 'application_id=e7c327f37d873eaf7895b497a5e260ae'

    def get_urls(self):
        urls = []

        for idx in range(self.Config.URLS_AMOUNT):
            urls.append(
                f'{self.Config.API_WG}?{self.Config.APP_ID}&account_id={idx}'
            )

        return urls

    async def fetch_url(self, url, session):
        async with session.get(url, verify_ssl=False) as resp:
            data = await resp.json()
            print(str(resp.url).split('=')[-1])

    async def bound_fetch(self, semaphore, url, session):
        async with semaphore:
            print(f"#2: {str(url).split('=')[-1]}")
            await self.fetch_url(url, session)

    async def load_links(self, urls):
        tasks = []
        semaphore = asyncio.Semaphore(self.Config.SEMAPHORE_LIMIT)
	# семафор на одновременное количество коннектов
        async with aiohttp.ClientSession() as session:
            for url in urls: # для каждого урла создаем задачу
                task = asyncio.ensure_future(
                    self.bound_fetch(
                        semaphore, url, session
                    )
                )
                tasks.append(task) # и пополняем список задач

            await asyncio.gather(*tasks) # запуск задач

    def run(self):
        urls = self.get_urls() # формируется список урлов (для моей задачи)
        loop = asyncio.get_event_loop() # event-loop из asyncio
        future = asyncio.ensure_future(self.load_links(urls)) # инициализируем
# футур из результата "будущего" fetch'а
        loop.run_until_complete(future) # выполняем


if __name__ == '__main__':
    print(f'Аргументы командной строки {sys.argv}')
    parser = WargamingParser()
    parser.run()
