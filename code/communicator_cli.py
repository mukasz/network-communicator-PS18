#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 20:28:38 2018

@author: ukasz
"""

import socket
import sys

PORT = 12
HOST = '127.0.0.1'

if __name__ == '__main__':   
    if len(sys.argv) == 2:
        username = sys.argv[1]
    elif len(sys.argv) == 3:
        username = sys.argv[1]
        HOST = sys.argv[2]
    else:
        print "wrong number of arguments: (username, [ip_addr]) "
        sys.exit(-1)
    
    try:
        soc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        soc.connect( (HOST, PORT) )
        
        soc.send( bytearray( username ) ) #trying to loggin
        reply = soc.recv(128)
        print reply + '\n'
        if reply == 'Login:    OK':
            
        
    except socket.error as e:
        sys.stderr.write("Socket error({0}): {1}".format(e.errno, e.strerror))