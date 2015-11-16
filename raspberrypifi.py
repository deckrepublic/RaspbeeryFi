from clients import *
from utility import *


def request(context, flow):
    if is_new_client(flow.client_conn.address.host):
        handle_new_client_request(flow)
    else:
        replace_localhost_request_if_necessary(flow.request)


def response(context, flow):
    if is_new_client(flow.client_conn.address.host):
        add_dont_cache_headers(flow.response)
