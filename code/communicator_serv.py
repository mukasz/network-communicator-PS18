#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 20:27:14 2018

@author: ukasz
"""

import socket
import sys
import threading
import Queue

HOST = ''
PORT = 12

class ClientConnection( threading.Thread ):
    def __init__( self, conn, username, queue ):
        threading.Thread.__init__( self )
        self.conn = conn
        self.remote_host = conn.getpeername()
        self.stopThread = False
        self.username = username
        self.msgbuff = queue
        
    def run( self ):
        #self.conn.send('Polaczono')
        try:
            self.conn.close()
        finally:
            print 'Host ' + str( self.remote_host ) + ' has disconnected'
            
            with users_lock:
                users.pop[self.username]
            with msgbuff_lock:
                msgbuff.pop[self.username]
        
if __name__ == '__main__':
    connections = {}
    users = {} #(username: addr)
    msgbuff = {}

    users_lock = threading.Lock()
    msgbuff_lock = threading.Lock()
    try:
        soc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind( (HOST, PORT) )
        soc.listen( 1 )
        
        while True:
            conn, addr = soc.accept()
            print 'Host ' + str( addr ) + ' is connected'
            username = conn.recv(128)
            with users_lock:
                if users.has_key( username ):
                    conn.send( bytearray('Login: NOTOK') )
                    conn.close()
                    break;
                else:
                    conn.send( bytearray('Login:    OK') ) #logging complete
                    queue = Queue.Queue(100)
                    with msgbuff_lock:
                        msgbuff[username] = queue
                    connections[addr] = ClientConnection( conn, username, queue )
                    users[username] = (addr, True) #(addr, is_available)
                    
                    connections[addr].run() #start nec connection-thread
        
    except socket.error as e:
        print "Socket error({0}): {1}".format(e.errno, e.strerror)
        
    except KeyboardInterrupt:
        print "Server is closing..."
        for c in connections:
            c.stopThread = True
            c.join()
        