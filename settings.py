from urllib.parse import urlparse

from wordpress_xmlrpc import Client

def init(
    username,
    password,
    xmlrpc_php,
    enable_deletion,
):
    url_info = urlparse(xmlrpc_php)

    global domain_name
    domain_name = url_info.netloc

    global wp
    wp = Client(xmlrpc_php, username, password)

    global _enable_deletion
    _enable_deletion = enable_deletion