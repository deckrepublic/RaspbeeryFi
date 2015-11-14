from libmproxy.models import decoded
from clients import *
from utility import *


def clientconnect(context, root_layer):
    set_client_connect_flag(root_layer.client_conn.address.host)


def request(context, flow):
    if is_new_client(flow.client_conn.address.host):
        if flow.request.host != 'localhost':
            change_request_to_login_page(flow.request)
        elif flow.request.host == 'localhost' and (not flow.request.path or 
            flow.request.path == '/'):
            change_request_to_login_page(flow.request)
        elif has_login_info(flow.request):
            # TODO: store login info
            add_client(flow.client_conn.address.host)


def response(context, flow):
    with decoded(flow.response):
        pass
