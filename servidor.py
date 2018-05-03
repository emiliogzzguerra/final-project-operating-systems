#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This sample program, based on the one in the standard library documentation, receives incoming messages and echos them back to the sender. It starts by creating a TCP/IP socket.

import socket
import sys
import time
import heapq
from tabulate import tabulate
from prettytable import PrettyTable

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Then bind() is used to associate the socket with the server address. In this case, the address is localhost, referring to the current server, and the port number is 10000.

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

#Calling listen() puts the socket into server mode, and accept() waits for an incoming connection.

# Listen for incoming connections
sock.listen(1)

# Wait for a connection
print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()

# accept() returns an open connection between the server and client, along with
# the address of the client. The connection is actually a different socket on
# another port (assigned by the kernel). Data is read from the connection with
# recv() and transmitted with sendall().

# List to divide the input into multiple strings
splitData = []
# Used to determine the number of each process
processNumber = 1
# Used to delete record after "running" the process
copyNonEditedRunning = ()
# Used to run the process, decrementing the timeToLive
cpu1 = []
# Used to determine the global time, dependent on the quantum the client sends
currentTime = 0
# Are we done?
done = False
# List to store the processes that just arrived
arrived = []
# List to store the processes that are added to the ready queue
readyQueue = []
# List to store the processes currently on CPU 1
cpu1 = []
# List to store the blocked readyQueue
blocked = []
# List to store the finished readyQueue
finished = []
# Table for 1 CPU
table1data = [[],[],[],[],[],[]]
table1 = PrettyTable(['Timestamp',
         'Llegadas',
         'Cola de listos',
         'CPU 1',
         'Procesos bloqueados',
         'Procesos terminados'])
# Table for 2 CPU's
table2data = [[],[],[],[],[],[],[]]
table2 = PrettyTable(['Timestamp',
         'Llegadas',
         'Cola de listos',
         'CPU 1',
         'CPU 2',
         'Procesos bloqueados',
         'Procesos terminados'])

try:
    print >>sys.stderr, 'connection from', client_address
    if(sys.argv[1] == "SJF"):
        if(sys.argv[2] == "1"): # One CPU
            print "One CPU, SJF"
            while True:
                data = connection.recv(256)
                if data:
                    # Split the data received to understand which is the action to do
                    splitData = data.split()

                    if(splitData[1] == "CREATE"):
                        aux = (int(splitData[3]), processNumber, len(readyQueue)+1)

                        # This is run only for the first process that is created
                        if not readyQueue:
                            copyNonEditedRunning = aux
                            cpu1 = [int(splitData[3]), processNumber]
                            print 'CT:{} || Started ({},P{})'.format(currentTime,cpu1[0], cpu1[1])

                        # Every we add the process, then we sort the whole list
                        arrived.append(aux)
                        readyQueue.append(aux)
                        readyQueue = sorted(readyQueue, key = lambda tup: (tup[0], tup[2]))

                        # Increment the process number
                        processNumber += 1
                    elif(splitData[1] == "QUANTUM"):
                        # Print current state
                        table1.add_row([currentTime,arrived,readyQueue,cpu1,blocked,finished])
                        print table1
                        arrived = []

                        # Increment the global time, and decrement the timeToLive of
                        # the current runnning process
                        currentTime += 1
                        cpu1[0] -= 1

                        # If the time of the current running process is up
                        # we remove that process from the list, and assign a new
                        # cpu1 process.
                        if(cpu1[0] == 0):
                            print 'CT:{} || Finished ({},P{})'.format(currentTime,cpu1[0], cpu1[1])
                            finished.append(cpu1)
                            readyQueue.remove(copyNonEditedRunning)

                            # There are no more readyQueue, we're done
                            if not readyQueue:
                                print 'CT:{} || We are DONE'.format(currentTime)
                                done = True
                            else: # There are still more readyQueue
                                copyNonEditedRunning = readyQueue[0]
                                cpu1 = [readyQueue[0][0], readyQueue[0][1]]
                                readyQueue.remove(copyNonEditedRunning)
                                print 'CT:{} || Started ({},P{})'.format(currentTime,cpu1[0], cpu1[1])
                        else:
                            # We're in the process of running a process, we just display
                            # the progress.
                            if not done:
                                print 'CT:{} || ({},P{}) Running'.format(currentTime,cpu1[0], cpu1[1])
                    elif(splitData[1] == "INICIA"):
                        # Make sure that the process is currently running
                        if (cpu1[1] == int(splitData[3])):
                            blocked.append(cpu1)

                    elif(splitData[1] == "TERMINA"):
                        # Find the blocked process
                        for blockedProcess in blocked:
                            if (blockedProcess[1] == int(splitData[3])):
                                readyQueue.append(blockedProcess)
                                blocked.remove(blockedProcess)
                                readyQueue = sorted(readyQueue, key = lambda tup: (tup[0], tup[2]))
                            pass
                    elif(splitData[1] == "END"):
                        # The client ordered the communication to be done.
                        print 'CT:{} || Ending program'.format(currentTime)
                    else: # KILLING a process
                        # Determine wether that process is still on the list
                        for process in readyQueue:
                            if (process[1] == int(splitData[2])):
                                removeTuple = process
                            pass
                        # If it is on the list
                        if(removeTuple != ()):
                            print 'CT:{} || Killed P{}'.format(currentTime,removeTuple[1])
                            readyQueue.remove(removeTuple)

                            # This happens if we kill an ongoing process
                            if(removeTuple[1] == cpu1[1]):
                                copyNonEditedRunning = readyQueue[0]
                                cpu1 = [readyQueue[0][0], readyQueue[0][1]]
                                print 'CT:{} || Started ({},P{})'.format(currentTime,cpu1[0], cpu1[1])
                            removeTuple = ()
                        else:
                            #Not on the list, inform the client it's not in the list
                            print "CT:{} || Tried to kill P{}".format(currentTime,splitData[2])

                    connection.sendall('ACK')
        else: # Two CPU's
            print "Two CPU, SJF"

    elif(sys.argv[1] == "SRT"):
        if(sys.argv[2] == "1"): # One CPU
            print "One CPU, SRT"

        else: # Two CPU's
            print "Two CPU, SRT"

    else:
        print "Nuestro equipo no considero la politica {}".format(sys.argv[1])

finally:
    #Close the communication
    connection.close()
    sys.exit(0)
    def main(args):
        return 0
        if __name__ == '__main__':
            import sys
            sys.exit(main(sys.argv))
