#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
HOST = '127.0.0.1'  
PORT = 8000        
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()
        # message is something like GET /HelloWorld.html HTTP/1.1 ... /page1/helloworld.html
        filename = message.split()[1]

        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        #Send one HTTP header line into socket
        headerLine = 'HTTP/1.1 200 OK\r\n\r\n'
        connectionSocket.send(headerLine.encode())

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        #Send response message for file not found
        headerLine = 'HTTP/1.1 404 Not Found\r\n\r\n'
        data = 'File not found'
        responseMessage = headerLine + data
        
        for i in range(0, len(responseMessage)): 
            connectionSocket.send(responseMessage[i].encode())

        #Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit() #Terminate the program after sending the corresponding data 