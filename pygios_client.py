#!/usr/bin/env python

import socket
import sys
import datetime
import psutil, time
import re

if  len(sys.argv) < 2:
        print "Please specify a host..."
        sys.exit()

def get_memory():
    re_parser = re.compile(r'^(?P<key>\S*):\s*(?P<value>\d*)\s*kB')
    result = dict()
    for line in open('/proc/meminfo'):
        match = re_parser.match(line)
        if not match:
            continue;
        key, value = match.groups(['key', 'value'])
        result[key] = int(value)

    MemTotal = float(result['MemTotal'])
    MemFree = float(result['MemFree'])
    Cached = float(result['Cached'])
    MemUsed = MemTotal - (Cached + MemFree)
    SwapTotal = float(result['SwapTotal'])
    SwapFree = float(result['SwapFree'])
    return int(MemTotal), int(MemUsed), int(SwapTotal), int(SwapFree)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server given by the caller
server_address = (sys.argv[1], 8888)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    welcome = False

    print "Awaiting welcome message..."

    while not welcome:
        welcome = sock.recv(1024)

    print >>sys.stderr, '[RECV] "%s"' % welcome

    message = "[" + datetime.datetime.now().strftime("%m/%d/%y %H:%M") + "]6a736f6e:" + str(get_memory())

    print >>sys.stderr, '[SEND] "%s"' % message
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print >>sys.stderr, '[RECV] "%s"' % data

finally:
    sock.close()
