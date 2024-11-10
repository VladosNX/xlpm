import socket
import os
import subprocess

uiPath = 'xlpm-daemon-ui'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 19340))


def readOption(option):
    return option.split('=')

server.listen(10)
while True:
    client, addr = server.accept()
    data = client.recv(1024).decode()
    print(data)
    command = data.split('\n')[0].split(' ')[1].split('?')[0]
    client.send('HTTP/1.1 200 OK\n\nxlpm command accepted'.encode())
    client.close()
    options_raw = None
    if len(data.split('\n')[0].split(' ')[1].split('?')) > 1:
        options_raw = data.split('\n')[0].split(' ')[1].split('?')[1].split('&')
        print(options_raw)
    
    options = {}
    if not options_raw == None:
        for o in options_raw:
            key = o.split('=')[0]
            value = o.split('=')[1]
            options[key] = value

    if command == '/getgit' and options['pkg']:
        pkgGit = f"{options['pkg'].split('___')[0]}/{options['pkg'].split('___')[1]}"
        print(pkgGit)
        xtermCommand = f'xterm -geometry 60x10 -bg black -fg white -e "{uiPath} getgit {pkgGit}"'
        print('getgit executing')
        subprocess.getoutput(xtermCommand)
    print(command)