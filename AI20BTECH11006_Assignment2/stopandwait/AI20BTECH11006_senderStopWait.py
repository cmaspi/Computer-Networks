import socket
import multiprocessing
from collections import deque
import sys
import time
import os


senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# ---------------------------------------
def get_data_string():
    with open('testFile.jpg', 'rb') as f:
        while True:
            data = f.read(1000)
            if not data:
                break
            yield data


def gen_message():
    seq = 1
    end = 0
    for data_string in get_data_string():
        message = seq.to_bytes(2, 'big') + end.to_bytes(1, 'big') + data_string
        seq += 1
        yield message
    end = 1
    yield seq.to_bytes(2, 'big') + end.to_bytes(1, 'big')
#----------------------------------------

def receive(BASE, cache_size):
    for _ in range(cache_size):
        msg = socket_udp.recvfrom(bufferSize)
        NEXT = int.from_bytes(msg[0], 'big') - BASE.value + 1
        if NEXT > 0:
            BASE.value += NEXT


# ---------------------------------------
RETRANSMISSIONS = 0
packets = gen_message()
itr = 0
manager = multiprocessing.Manager()
window_size = 1
BASE = manager.Value('i', 1)
PREV_BASE = BASE.value - window_size
cache = deque(maxlen=window_size)

timeout = int(sys.argv[-1])
print("The timeout is:", timeout)
timeout /= 1000

num_packets = 0

START = time.time()
while True:
    itr += 1

    if BASE.value-PREV_BASE > 0:
        for i in range(BASE.value-PREV_BASE):
            try:
                packet = packets.__next__()
                cache.append(packet)
                socket_udp.sendto(packet,
                                recieverAddressPort)
                num_packets += 1
            except:
                if num_packets == BASE.value-1:
                    END = time.time()
                    FILE_SIZE = os.path.getsize('testFile.jpg')
                    print('Throughput:', FILE_SIZE/(1024*(END-START)))
                    print("Retransmissions:", RETRANSMISSIONS)
                    sys.exit()
        
        PREV_BASE = BASE.value

    else:

        for packet in cache:
            RETRANSMISSIONS += 1
            socket_udp.sendto(packet,
                              recieverAddressPort)
            
    p = multiprocessing.Process(target=receive,
                                args=(BASE, cache.__len__()))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
    for i in range(BASE.value-PREV_BASE):
        cache.popleft()
