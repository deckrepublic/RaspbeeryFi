from libmproxy.models import decoded
from clients import *
from utility import *


def clientconnect(context, root_layer):
    set_client_connect_flag(root_layer.client_conn.address.host)


def request(context, flow):
    if is_new_client(flow.client_conn.address.host):
        if did_client_just_connect(flow.client_conn.address.host):
            flow.request.host = 'localhost'
            flow.request.path = '/login.html'
            unset_client_connect_flag(flow.client_conn.address.host)
        elif has_login_info(flow.response):
            # TODO: store login info
            add_client(flow.client_conn.address.host)


def response(context, flow):
    with decoded(flow.response):
        pass
