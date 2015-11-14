from netlib.http import Headers


_clients = []
_client_connect_flags = []


def add_client(host):
    if is_new_client(host):
        _clients.append(host)


def is_new_client(host):
    return host not in _clients


def has_login_info(response):
    # TODO
    return False


def set_client_connect_flag(host):
    if host not in _client_connect_flags:
        _client_connect_flags.append(host)


def unset_client_connect_flag(host):
    _client_connect_flags.remove(host)


def did_client_just_connect(host):
    return host in _client_connect_flags
