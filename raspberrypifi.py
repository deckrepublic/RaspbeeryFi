from libmproxy.models import decoded
from clients import *
from utility import *


def request(context, flow):
    if is_new_client(flow.client_conn.address.host):
        if flow.request.host != 'localhost':
            if flow.client_conn.address.host not in destinations:
                destinations[flow.client_conn.address.host] = [flow.request.host,
                    flow.request.path]
            change_request_to_login_page(flow.request)
        elif flow.request.host == 'localhost' and (not flow.request.path or 
            flow.request.path == '/'):
            change_request_to_login_page(flow.request)
        elif has_login_info(flow.request):
            params = url_params_to_dict(flow.request.content)
            add_client(flow.client_conn.address.host, params['login'],
                params['password'])
            flow.request.host = destinations[flow.client_conn.address.host][0]
            flow.request.path = destinations[flow.client_conn.address.host][1]
            flow.request.method = 'GET'
            del destinations[flow.client_conn.address.host]
