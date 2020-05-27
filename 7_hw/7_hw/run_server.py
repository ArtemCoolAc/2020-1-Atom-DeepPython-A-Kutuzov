import json
import socket
import sys
from email.parser import Parser
from functools import lru_cache
from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup
import logging
import requests
import re
from collections import Counter

logging.basicConfig(filename='log.txt', level=logging.DEBUG)

MAX_LINE = 64 * 1024
MAX_HEADERS = 100


class MyHTTPServer:
    def __init__(self, host, port, server_name):
        logging.debug(f"host is {host}, port is {port}, server_name is {server_name}")
        self._host = host
        self._port = port
        self._server_name = server_name
        self._users = {}

    def serve_forever(self):
        """Метод "вечной" жизни сервера"""
        serv_sock = socket.socket(  # инициализируем сокет
            socket.AF_INET,  # семейство адресов AF_INET
            socket.SOCK_STREAM,  # SOCK_STREAM - тип сокетов для TCP
            proto=0)

        try:
            serv_sock.bind((self._host, self._port))  # связываем хост и порт в сокете
            serv_sock.listen()  # прослушиваем

            while True:  # бесконечно
                conn, _ = serv_sock.accept()  # принимаем подключение и возвращаем инфу о нем
                logging.debug(f'Connected socket is {conn}')
                try:
                    self.serve_client(conn)  # принимаем что-то от клиента
                except Exception as e:
                    logging.error(f'Client serving failed, exception: {e}')
                    print('Client serving failed', e)  # в случае исключения выводим его
        finally:
            serv_sock.close()  # после всего закрываем сокет

    def serve_client(self, conn):
        """Метод описывает общий алгоритм работы с клиентом"""
        logging.debug('Начало работы с клиентом! Serve_client')
        try:
            req = self.parse_request(conn)  # сначала парсим запрос
            logging.debug(f'Распарсили запрос, вот он: {req}')
            resp = self.handle_request(req)  # затем формируем ответ
            logging.debug(f'Сформирован ответ, вот он: {resp}')
            self.send_response(conn, resp)  # после этого отправляем ответ
        except ConnectionResetError:
            conn = None
        except Exception as e:
            logging.error(f'Внезапная ошибка: {e}')
            self.send_error(conn, e)  # если ловим исключение, устанавливаем ошибку

        if conn:
            req.rfile.close()
            conn.close()
            logging.debug('СОКЕТ ЗАКРЫТ')

    def parse_request(self, conn):
        """В этом методе парсим запрос от пользователя"""
        logging.debug(f'Начинаем парсить запрос из сокета {conn}, начало метода parse_request')
        rfile = conn.makefile('rb')  # создаем file object ассоциированный с сокетом
        method, target, ver = self.parse_request_line(rfile)  # парсим строку запроса
        logging.debug(f'После парсинга строки запроса получаем следующее: \n \
        метод: {method}, цель: {target}, версия: {ver}')
        # и получаем метод, цель, версию
        headers = self.parse_headers(rfile)  # парсим заголовки
        logging.debug(f'После парсинга заголовков имеем: {headers}')
        host = headers.get('Host')  # получаем хоста
        logging.debug(f'Хост {host}')
        if not host:  # если его нет, кидаем исключение
            logging.debug(f'Нет хоста, HTTPError 400')
            raise HTTPError(400, 'Bad request',
                            'Host header is missing')
        if host not in (self._server_name,
                        f'{self._server_name}:{self._port}'):
            logging.error(f'Хост не найден')
            raise HTTPError(404, 'Not found')
        logging.debug(f'Конец parse_request')
        return Request(method, target, ver, headers, rfile)

    def parse_request_line(self, rfile):
        """В этом методе парсим строку запроса"""
        logging.debug(f'Начало метода parse_request_line')
        raw = rfile.readline(MAX_LINE + 1)  # читаем сырую строку из fileobject
        logging.debug(f'Сырая строчка из fileobject: {raw}')
        if len(raw) > MAX_LINE:  # если слишком длинная, кидаем исключение
            logging.error('Слишком длинная строка')
            raise HTTPError(400, 'Bad request',
                            'Request line is too long')

        req_line = str(raw, 'iso-8859-1')  # формируем нормальную строку запроса
        logging.debug(f'Нормальная строка из сырой: {req_line}')
        words = req_line.split()  # разбиваем на "пред"заголовки
        logging.debug(f'После разбиения получаем: {words}')
        if len(words) != 3:  # если "слов" больше 3, то неправильный формат запроса
            logging.error('Ошибка 400 - слишком много')
            raise HTTPError(400, 'Bad request',
                            'Malformed request line')

        method, target, ver = words
        if ver != 'HTTP/1.1':  # возьмем только HTTP/1.1
            logging.error('Версия HTTP не 1.1')
            raise HTTPError(505, 'HTTP Version Not Supported')
        logging.debug('Конец метода parse_request_line')
        return method, target, ver

    def parse_headers(self, rfile):
        """Получаем заголовки в нормальном виде"""
        logging.debug('Начало метода parse_headers')
        headers = []
        while True:
            line = rfile.readline(MAX_LINE + 1)
            logging.debug(f'Прочитанная строка: {line}')
            if len(line) > MAX_LINE:
                logging.error('Слишком длинная строка')
                raise HTTPError(494, 'Request header too large')

            if line in (b'\r\n', b'\n', b''):
                break

            headers.append(line)
            if len(headers) > MAX_HEADERS:
                logging.error('Слишком много заголовков')
                raise HTTPError(494, 'Too many headers')
        logging.debug(f'Получившиеся headers: {headers}')
        sheaders = b''.join(headers).decode('iso-8859-1')
        logging.debug(f'Приведение к iso-8859-1: {sheaders}')
        logging.debug(f'Распаршенные заголовки: {Parser().parsestr(sheaders)}')
        logging.debug('Конец parse_headers')
        return Parser().parsestr(sheaders)

    def handle_request(self, req):
        logging.debug('Начало обработки распаршенного запроса (handle_request_')
        logging.debug(f'request.path = {req.path}')
        if req.target.startswith('http://') or req.target.startswith('https://') or req.target.startswith('www.'):
            logging.debug('GET -> url')
            return self.handle_get_html(req)

        if req.path == '/users' and req.method == 'POST':
            logging.debug('POST -> users')
            return self.handle_post_users(req)

        if req.path == '/users' and req.method == 'GET':
            logging.debug('GET -> users')
            return self.handle_get_users(req)

        if req.path.startswith('/users/'):
            logging.debug('Path starts with /users/')
            user_id = req.path[len('/users/'):]
            if user_id.isdigit():
                return self.handle_get_user(req, user_id)
        logging.debug('Конец метода handle_request, ошибка 404')
        raise HTTPError(404, 'Not found')

    def send_response(self, conn, resp):
        logging.debug('Начало send_response')
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        logging.debug(f'Status line is {status_line}')
        wfile.write(status_line.encode('iso-8859-1'))

        if resp.headers:
            logging.debug('Заголовки есть')
            for (key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                logging.debug(f'Header line is: {header_line}')
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if resp.body:
            logging.debug(f'Тело ответа есть, {resp.body.decode()}')
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()
        logging.debug('Конец send_response')

    def send_error(self, conn, err):
        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode('utf-8')
        except:
            status = 500
            reason = b'Internal Server Error'
            body = b'Internal Server Error'
        resp = Response(status, reason,
                        [('Content-Length', len(body))],
                        body)
        self.send_response(conn, resp)

    def handle_get_html(self, req):
        logging.debug('Начало метода handle_get_html')
        accept = req.headers.get('Accept')
        logging.debug(f'Возвращаемый тип - {accept}')
        url = req.target
        logging.debug(f'Полученный URL - {url}')
        try:
            resp = requests.get(url)
        except Exception as e:
            logging.error(f'Ошибка! {e}')
            return Response(404, e)
        clean_text = list(BeautifulSoup(requests.get(url).text, "html.parser").stripped_strings)
        logging.debug(f'Список слов был получен - {clean_text}')
        processed_text = list(map(lambda x: re.sub(r'\xa0', ' ', x), clean_text))
        logging.debug(f'После удаления неразрывных пробелов имеем {processed_text}')
        fl = lambda *n: (e for a in n for e in (fl(*a) if isinstance(a, (tuple, list)) else (a,)))
        flatten = lambda x: list(fl(x))
        splitted_words = flatten([re.split(r'\s+', string.lower()) for string in processed_text])
        logging.debug(f'Теперь слова по одиночке: \n {splitted_words}')
        stop_words = list()
        with open('Stop_words_useless.txt', 'r') as file:
            for line in file:
                stop_words.append(line[:-1])
        filtered_words = list(filter(lambda x: x not in stop_words, splitted_words))
        logging.debug(f'После фильтрования имеем следующий список:\n {filtered_words}')
        words = Counter(filtered_words)
        logging.debug(f'Посчитанные слова: \n {words}')
        top_10 = words.most_common(10)
        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            body = ''
            for elem in top_10:
                body += f'{elem[0]} - {elem[1]}'
        elif 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps(dict(top_10), ensure_ascii=False)
        else:
            return Response(406, 'Not acceptable')
        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        logging.debug('Конец handle_get_html')
        return Response(200, 'OK', headers, body)

    def handle_post_users(self, req):
        user_id = len(self._users) + 1
        self._users[user_id] = {'id': user_id,
                                'name': req.query['name'][0],
                                'age': req.query['age'][0]}
        return Response(204, 'Created')

    def handle_get_users(self, req):
        accept = req.headers.get('Accept')
        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            body = '<html><head></head><body>'
            body += f'<div>Пользователи ({len(self._users)})</div>'
            body += '<ul>'
            for u in self._users.values():
                body += f'<li>#{u["id"]} {u["name"]}, {u["age"]}</li>'
            body += '</ul>'
            body += '</body></html>'

        elif 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps(self._users)

        else:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        return Response(200, 'OK', headers, body)

    def handle_get_user(self, req, user_id):
        user = self._users.get(int(user_id))
        if not user:
            raise HTTPError(404, 'Not found')

        accept = req.headers.get('Accept')
        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            body = '<html><head></head><body>'
            body += f'#{user["id"]} {user["name"]}, {user["age"]}'
            body += '</body></html>'

        elif 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps(user)

        else:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        return Response(200, 'OK', headers, body)


class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile

    @property
    def path(self):
        return self.url.path

    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)

    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)

    def body(self):
        size = self.headers.get('Content-Length')
        if not size:
            return None
        return self.rfile.read(size)


class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


class HTTPError(Exception):
    def __init__(self, status, reason, body=None):
        super()
        self.status = status
        self.reason = reason
        self.body = body


if __name__ == '__main__':
    """Передача параметров через командную строку"""
    host = sys.argv[1]  # хост
    port = int(sys.argv[2])  # порт
    name = sys.argv[3]  # имя

    serv = MyHTTPServer(host, port, name)  # инициализируем сервер
    try:
        serv.serve_forever()  # пытаемся запустить его навечно
    except KeyboardInterrupt:
        pass
