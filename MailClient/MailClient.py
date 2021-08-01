from socket import *
import ssl
import base64
from dotenv import dotenv_values

config = dotenv_values('.env')

SENDER_EMAIL_ADDRESS = config["SENDER_EMAIL_ADDRESS"]
SENDER_EMAIL_PASSWORD = config["SENDER_EMAIL_PASSWORD"]
RECIPIENT_EMAIL_ADDRESS = config["RECIPIENT_EMAIL_ADDRESS"]

def main():
    # Choose a mail server (e.g. Google mail server) and call it mailserver
    mailserver = 'smtp.gmail.com'
    mailserverPort = 587

    # Create socket called clientSocket and establish a TCP connection with mailserver
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, mailserverPort))
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Google\r\n'
    sendCommandAndPrintResponse(clientSocket, heloCommand, '250')

    starttlsCommand = 'STARTTLS\r\n'
    sendCommandAndPrintResponse(clientSocket, starttlsCommand, '220')

    clientSocket = ssl.wrap_socket(clientSocket)

    # Send AUTH LOGIN command
    authCommand = 'AUTH LOGIN\r\n'
    sendCommandAndPrintResponse(clientSocket, authCommand, '334')

    # Send sender's email address
    sendAuthDataAndPrintResponse(clientSocket, base64.b64encode(SENDER_EMAIL_ADDRESS.encode()) + '\r\n'.encode(), '334')

    # Send sender's email password
    sendAuthDataAndPrintResponse(clientSocket, base64.b64encode(SENDER_EMAIL_PASSWORD.encode()) + '\r\n'.encode(), '235')

    # Send MAIL FROM command and print server response.
    mailFromComamnd = 'MAIL FROM:' + '<' + SENDER_EMAIL_ADDRESS + '>' + '\r\n'
    sendCommandAndPrintResponse(clientSocket, mailFromComamnd, '250')

    # Send RCPT TO command and print server response.
    rcptToCommand = 'RCPT TO:' + '<' + RECIPIENT_EMAIL_ADDRESS + '>' + '\r\n'
    sendCommandAndPrintResponse(clientSocket, rcptToCommand, '250')

    # Send DATA command and print server response.
    dataCommand = 'DATA\r\n'
    sendCommandAndPrintResponse(clientSocket, dataCommand, '354')

    # Send message data.
    subject = 'Subject:This is an email sent by a Python client using TLS\r\n'
    message = 'Hello. I\'m learning Computer Networking'
    endMsg = "\r\n.\r\n"
    sendCommandAndPrintResponse(clientSocket, subject + message + endMsg, '250')

    # Send QUIT command and get server response.
    quitCommand = 'QUIT\r\n'
    sendCommandAndPrintResponse(clientSocket, quitCommand, '221')

    clientSocket.close()

def sendCommandAndPrintResponse(socket, command, status):
    socket.send(command.encode())
    recv = socket.recv(1024).decode()
    print(recv)
    if recv[:3] != status:
        print(status + ' reply not received from server.')

def sendAuthDataAndPrintResponse(socket, data, status):
    socket.send(data)
    recv = socket.recv(1024).decode()
    print(recv)
    if recv[:3] != status:
        print(status + ' reply not received from server.')

main()