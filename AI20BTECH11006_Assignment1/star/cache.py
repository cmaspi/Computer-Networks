# import socket
import logging
from server import RunServer
from client import MakeConnection
from client import GET as parse_GET
from client import PUT as parse_PUT

cache = {}

## setting up logging config
logging.basicConfig(filename='cache.log',
					level=logging.DEBUG,
					filemode='w',
					)


def GET(key, cache, IP, port):
    if key in cache:
        return cache[key]
    else:
        s = MakeConnection(IP, port)
        request = parse_GET(key, IP)
        s.send(request)
        recv = s.recv(1024)
        temp = recv.decode()
        temp = temp.split()[1]
        if temp == '200':
            cache[key] = recv.decode()
        return cache[key]

def PUT(key, val, IP, port):
    s = MakeConnection(IP, port)
    request = parse_PUT(key, val, IP)
    s.send(request)
    return s.recv(1024).decode()


def handle_response(msg, cache, IP, port):
    temp = msg.split()
    if temp[0] == 'GET':
        key = msg.split('/')[-3].split()[0]
        return GET(key, cache, IP, port)
    elif temp[0] == 'PUT':
        val = ' '.join(msg.split('/')[-2].split()[:-1])
        key = msg.split('/')[-3]
        return PUT(key, val, IP, port)
    else:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"


if __name__ == '__main__':
    IP, port = '10.0.1.2', 12346
    serverIP, serverPort = '10.0.1.3', 12346
    s = RunServer(IP, port)
    while True:
        try:
            c, addr = s.accept()
            logging.info('Got Connection from {}'.format(addr))
            recvmsg = c.recv(1024).decode()
            logging.debug("Server Received: {}".format(recvmsg))
            c.send(handle_response(recvmsg, cache, serverIP, serverPort).encode())
            c.close()
        except Exception as e:
            if e is not KeyboardInterrupt:
                logging.error("Error Encounter: {}".format(e))
            break


        