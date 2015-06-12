import requesocks
import random


class pytor:
    # pre define tor ports
    ports = [9051, 9052, 9053, 9054, 9055]
    port = 0
    # init session
    session = requesocks.session()

    def __init__(self):
        self.random_jump()

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return self.port

    # jumps from current port to another port
    def random_jump(self):
        candidates = list(set(self.ports)-set([self.port]))
        new_port = (random.choice(candidates))
        self.session.proxies = {'http': 'socks5://127.0.0.1:',
                                'https': 'socks5://127.0.0.1:'}
        self.session.proxies['http'] += str(new_port)
        self.session.proxies['https'] += str(new_port)
        self.set_port(new_port)

    # sends a get request through previously set socks5 proxy
    def get(self, url, timeout=3):
        response = self.session.get(url, timeout=timeout)
        return response

    # get current session ip
    def test_connection(self):
        print (self.port, self.get('https://api.ipify.org'))
