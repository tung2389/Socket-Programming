from socket import *
from datetime import datetime

serverIP = '127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

for seq in range(1, 11):

    sendTime = datetime.now()
    message =  "Ping" + " " + str(seq) + " " + str(sendTime) 
    clientSocket.sendto(message.encode(), (serverIP, serverPort)) 
    clientSocket.settimeout(1)

    try:
        responseMessage = clientSocket.recv(1024).decode()
        recvTime = datetime.now()

        roundTripTime = recvTime - sendTime
        print("Message: " + responseMessage + " | " + "Round trip time: " + str(roundTripTime))

    except:
        print("Request timed out")

clientSocket.close()

