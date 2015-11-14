from netlib.http import Headers
from utility import *


_clients = []
destinations = dict()


def add_client(host, username, password):
    if is_new_client(host):
        _clients.append(Client(host, username, password))
        debug(str(_clients[-1]) + '\n')


def is_new_client(host):
    for client in _clients:
        if client.host == host:
            return False
    return True


def has_login_info(request):
    return request.host == 'localhost' and request.path == '/index.html'


def change_request_to_login_page(request):
    request.host = 'localhost'
    request.path = '/login.html'
    request.method = 'GET'
    request.scheme = 'http'


class Client:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def __str__(self):
        return self.host + " - " + self.username + ":" + self.password
