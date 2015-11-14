from netlib.http import Headers


LOGIN_PAGE_PATH = 'html/login.html'
_clients = []
_client_flags = []


def add_client(host):
    if is_new_client(host):
        _clients.append(host)


def is_new_client(host):
    return host not in _clients


def has_login_info(response):
    # TODO
    return False


def set_client_connect_flag(host):
    if host not in _client_flags:
        _client_flags.append(host)


def unset_client_connect_flag(host):
    _client_flags.remove(host)


def did_client_just_connect(host):
    return host in _client_flags


def get_login_page_html():
    with open(LOGIN_PAGE_PATH, 'r') as file:
        html = file.read()
    return html


def replace_response_with_login_page(response):
    response.headers = Headers(content_type='text/html')
    response.content = get_login_page_html()
