import socket
import logging


## setting up logging config
logging.basicConfig(filename='server.log',
					level=logging.DEBUG,
					filemode='w',
					)


courses = {}


def RunServer(serverIP, port):
  s = socket.socket()
  print ("Socket successfully created")
  s.bind((serverIP, port))
  print ("socket binded to {}".format(port))
  s.listen(5)
  print ("socket is listening...")
  return s


def GET(key, data):
	try:
		val = data[key]
		return 'HTTP/1.1 200 OK {}\r\n\r\n'.format(val)
	except KeyError:
		return """HTTP/1.1 404 Not Found\r\n\r\n"""


def PUT(key, val, data):
	data[key] = val


def handle_response(msg, data):
	temp = msg.split()
	if temp[0] == 'GET':
		key = msg.split('/')[-3].split()[0]
		return GET(key, data)

	elif temp[0] == 'PUT':
		val = ' '.join(msg.split('/')[-2].split()[:-1])
		key = msg.split('/')[-3]
		PUT(key, val, data)
		return "HTTP/1.1 200 OK\r\n\r\n"

	else:
		return "HTTP/1.1 400 Bad Request\r\n\r\n"

if __name__ == '__main__':
	IP = '10.0.1.3'
	port = 12346
	s = RunServer(IP, port)
	while True:
		try:
			c, addr = s.accept()
			logging.info('Got Connection from {}'.format(addr))
			recvmsg = c.recv(1024).decode()
			logging.debug("Server Received: {}".format(recvmsg))
			c.send(handle_response(recvmsg, courses).encode())
			c.close()
		except Exception as e:
			if e is not KeyboardInterrupt:
				logging.error("Error encountered: {}".format(e))


