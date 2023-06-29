import socket
import sys
import logging


## setting up logging config
logging.basicConfig(filename='client.log',
					level=logging.DEBUG,
					filemode='w',
					)


def MakeConnection(IP, port):
    s = socket.socket()
    print("Connecting to {}".format(IP))
    s.connect((IP, port))
    return s


courses = {
    'AI3000': "Reinforcement Learning",
    'AI3001': 'Advanced Topics in Machine Learning',
    'MA5060': 'Numerical Analysis',
    'CS2323': 'Computer Architecture',
    'EE2101': 'Control Systems',
    'CS3530': 'Computer Networks'
}


# get request
def GET(key, host):
    request = """GET /assignment1/courses/{} HTTP/1.1\r
Host: {}\r\n\r\n""".format(key, host)
    return request.encode()


def PUT(key, val, host):
    request = """PUT /assignment1/courses/{}/{} HTTP/1.1\r
Host: {}\r\n\r\n""".format(key, val, host)
    return request.encode()


def DELETE(key, host):
    request = """DELETE /assignment1/courses/{} HTTP/1.1\r
Host: {}\r\n\r\n""".format(key, host)
    return request.encode()


def MakeRequest(IP: str, port: int, method: str,
                key: str, val=None, verbose=False):
    dispatch = {
        'PUT': PUT,
        'GET': GET,
        'DELETE': DELETE
    }
    if verbose:
        print('Using {} method'.format(method))
    s = MakeConnection(IP, port)
    func = dispatch[method]
    request = func(key, val, IP) if method == 'PUT' else func(key, IP)
    s.send(request)
    recv = s.recv(1024)
    if verbose:
        print('Client received {}'.format(recv.decode()))


if __name__ == '__main__':
    port = 12346
    IP = '10.0.1.2'
    if sys.argv[-1] == '-i':
        while True:
            try:
                method = input('Enter the method (PUT/GET/DELETE): ').strip().upper()
                key = input('Enter the key: ')
                val = None
                if method == 'PUT':
                    val = input('Enter the val: ')
                MakeRequest(IP, port, method, key, val, verbose=True)
            except Exception as e:
                if e is not KeyboardInterrupt:
                    logging.error('Error occured: {}'.format(e))
    else:
        for key, val in courses.items():
            MakeRequest(IP, port, 'PUT', key, val, verbose=False)
        for key in courses:
            for _ in range(3):
                MakeRequest(IP, port, 'GET', key)
        # for key in courses:
        #     MakeRequest(IP, port, 'DELETE', key, verbose = True)

    