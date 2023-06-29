import socket
import sys

recieverIP = "10.0.0.2"
recieverPort   = 20002
bufferSize  = 1024 
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_udp.bind((recieverIP, recieverPort))
print("UDP socket created successfully....." )


img = []
def extract(message: bytes):
    global SEQ
    data = message
    # print("It received", int.from_bytes(data[:2], 'big'))
    if int.from_bytes(data[:2], 'big') != SEQ+1:
        return SEQ.to_bytes(2, 'big')
        
    if data[2] == 1:
        with open('receivedFile.jpg', 'wb') as f:
            for line in img:
                f.write(line)
            print("Image Received")
            
    else:
        img.append(data[3:])
    SEQ += 1
    return SEQ.to_bytes(2, 'big')

SEQ = 0
while True:
    #wait to recieve message from the server
    bytesAddressPair = socket_udp.recvfrom(bufferSize)
    
    
    recievedMessage = bytesAddressPair[0]
    senderAddress = bytesAddressPair[1]

    ack = extract(recievedMessage)
    
    # Sending a reply to client
    message = ack
    socket_udp.sendto(message, senderAddress)