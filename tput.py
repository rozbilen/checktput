#! /usr/bin/env python
# 1) throughput -s [port]                    # start a server
# 2) throughput -c  count host [server IP] [port]      # start a client

import sys, time
from socket import *

MY_PORT = 50000 + 42

BUFSIZE = 1024


def main():
    if len(sys.argv) < 2:
        usage()
    if sys.argv[1] == '-s':
        server()
    elif sys.argv[1] == '-c':
        client()
    else:
        usage()


def usage():
    sys.stdout = sys.stderr
    print ('Usage:    (on host_A) throughput -s [port]')
    print ('and then: (on host_B) throughput -c count host_A [port]')
    sys.exit(2)


def server():
    if len(sys.argv) > 2:
        port = eval(sys.argv[2])
    else:
        port = MY_PORT
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', port))
    s.listen(1)
    print ('Server ready...')
    while 1:
        conn, (host, remoteport) = s.accept()
        while 1:
            data = conn.recv(BUFSIZE)
            if not data:
                break
            del data
        conn.send('OK\n')
        conn.close()
        print (('Done with', host, 'port', remoteport))


def client():
    if len(sys.argv) < 4:
        usage()
    count = int(eval(sys.argv[2]))
    host = sys.argv[3]
    if len(sys.argv) > 4:
        port = eval(sys.argv[4])
    else:
        port = MY_PORT
    testdata = 'x' * (BUFSIZE-1) + '\n'
    t1 = time.time()
    s = socket(AF_INET, SOCK_STREAM)
    t2 = time.time()
    s.connect((host, port))
    t3 = time.time()
    i = 0
    while i < count:
        i = i+1
        s.send(testdata.encode('utf-8'))
    s.shutdown(1) # Send EOF
    t4 = time.time()
    data = s.recv(BUFSIZE)
    t5 = time.time()
    print (data)
    print (('Raw timers:', t1, t2, t3, t4, t5))
    print (('Intervals:', t2-t1, t3-t2, t4-t3, t5-t4))
    print (('Total:', t5-t1))
    print (('Throughput:', round((BUFSIZE*count*0.001) / (t5-t1), 3),))
    print (('K/sec.'))


main()
