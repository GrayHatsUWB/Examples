#!/usr/bin/env python
from socket import getaddrinfo, socket, AF_UNSPEC, SOCK_STREAM, AI_PASSIVE
from sys import argv, exit

s = None

for r in getaddrinfo(None, int(argv[1]), AF_UNSPEC, SOCK_STREAM, 0, AI_PASSIVE):
    af, socktype, proto, canonname, sockaddr = r

    try:
        s = socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
	
    try:
        s.bind(sockaddr)
        s.listen(1)
    except OSError as msg:
        s.close()
        s = None
        continue
	
    break

if s is None:
    print('Could Not Open Socket')
    exit(1)

while True:
    conn, addr = s.accept()
    data = conn.recv(1024)

    if not data:
        break

    print('Recieved {} from {}'.format(repr(data), addr))
    conn.send(data)
    conn.close()
