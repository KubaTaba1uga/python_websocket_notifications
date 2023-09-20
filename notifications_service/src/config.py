def get_proxy_endpoint_url():
    """
    Notifications service has one endpoint to receive all notifications and
     pass them to appropriate websockets (that's why called proxy).
    """
    return "http://somedummyurl.com/proxy"
