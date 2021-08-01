from socket import *
from pathlib import Path
import sys

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('', 8000))
tcpSerSock.listen(20)

while True:
    # Start receiving data from the client
    print('Ready to serve...')

    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    message = tcpCliSock.recv(1024).decode()
    # Extract the fileUrl from the given message
    fileUrl = message.split()[1].partition("/")[2]

    fileExist = False
    
    try:
        # Check wether the file exist in the cache
        f = open('cache/' + fileUrl, "r")
        outputdata = f.readlines()
        f.close()

        fileExist = True

        # ProxyServer finds a cache hit and generates a response message
        headers = [
            'HTTP/1.0 200 OK\r\n',
            'Content-Type:text/html\r\n\r\n'
        ]
        for header in headers:
            tcpCliSock.send(header.encode())

        for line in outputdata:
            tcpCliSock.send(line.encode())

        print('Read from cache')
    
    # Error handling for file not found in cache
    except IOError:
        if fileExist == False:
            # Create a socket on the proxyserver
            proxySocket = socket(AF_INET, SOCK_STREAM)
            
            try:
                # Connect to the socket to port 80
                hostname = fileUrl.partition('/')[0]
                port = 80
                proxySocket.connect((hostname, port))

                path = fileUrl.partition('/')[2]

                # Create a temporary file on this socket and ask port 80
                # for the file requested by the client
                fileObj = proxySocket.makefile('rwb', 0)
                headers = [
                    f'GET /{path} HTTP/1.0\r\n',
                    f'Host: {hostname}\r\n\r\n'
                ]
                for header in headers:
                    fileObj.write(header.encode())
                
                # Read the response into buffer
                rawData = fileObj.read()
                # Extract file from raw data (by excluding header)
                requestedFile = rawData.split(b'\r\n\r\n')[1]

                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache

                # Save all files in folder named 'cache'
                fileUrl = 'cache/' + fileUrl 
                folders = fileUrl.split('/')
                if len(folders) > 1:
                    folders = folders[0 : len(folders) - 1]
                    foldersPath = '/'.join(folders)
                    Path(foldersPath).mkdir(parents=True, exist_ok=True)

                tmpFile = open(fileUrl, "wb")
                tmpFile.write(requestedFile)
                tmpFile.close()
                
                headers = [
                    'HTTP/1.1 200 OK\r\n',
                    'Content-Type:text/html\r\n\r\n'
                ]
                for header in headers:
                    tcpCliSock.send(header.encode())

                tcpCliSock.send(requestedFile)

            except Exception as e:
                tcpCliSock.send('HTTP/1.0 500 Internal Server Error\r\n\r\n'.encode())

            proxySocket.close()

        else:
            tcpCliSock.send('HTTP/1.0 500 Internal Server Error\r\n\r\n'.encode())

    # Close the client and the server sockets
    tcpCliSock.close() 


tcpSerSock.close()