import os


def run_client(url):
    print('Вы клиент. Введите какой-нить URL и вытащим из его HTML 10 самых частых слов')
    command = f'./client.sh {url}'
    os.system(command)


if __name__ == '__main__':
    while True:
        print('Вы клиент. Введите какой-нить URL и вытащим из его HTML 10 самых частых слов')
        url1 = input()
        com = f'./client.sh {url1}'
        os.system(com)
        print('')