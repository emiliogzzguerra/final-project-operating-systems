#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This sample program, based on the one in the standard library documentation, receives incoming messages and echos them back to the sender. It starts by creating a TCP/IP socket.

import socket
import sys
import time
import heapq

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

# List to sort all the processes
processes = []
# List to divide the input into multiple strings
splitData = []
# Used to determine the number of each process
processNumber = 1
# Used to delete record after "running" the process
copyNonEditedRunning = ()
# Used to run the process, decrementing the timeToLive
currentRunning = []
# Used to determine the global time, dependent on the quantum the client sends
currentTime = 0
# Are we done?
done = False

try:
    print >>sys.stderr, 'connection from', client_address

    # Receive the data
    while True:
        data = connection.recv(256)
        if data:
            # Split the data received to understand which is the action to do
            splitData = data.split()

            if(splitData[1] == "CREATE"):
                aux = (int(splitData[3]), processNumber, len(processes)+1)

                # This is run only for the first process that is created
                if not processes:
                    copyNonEditedRunning = aux
                    currentRunning = [int(splitData[3]), processNumber]
                    print 'CT:{} || Started ({},P{})'.format(currentTime,currentRunning[0], currentRunning[1])

                # Every we add the process, then we sort the whole list
                processes.append(aux)
                processes = sorted(processes, key = lambda tup: (tup[0], tup[2]))

                # Increment the process number
                processNumber += 1
            elif(splitData[1] == "QUANTUM"):
                # Increment the global time, and decrement the timeToLive of
                # the current runnning process
                currentTime += 1
                currentRunning[0] -= 1

                # If the time of the current running process is up
                # we remove that process from the list, and assign a new
                # currentRunning process.
                if(currentRunning[0] == 0):
                    print 'CT:{} || Finished ({},P{})'.format(currentTime,currentRunning[0], currentRunning[1])
                    processes.remove(copyNonEditedRunning)

                    # There are no more processes, we're done
                    if not processes:
                        print 'CT:{} || We are DONE'.format(currentTime)
                        done = True
                    else: # There are still more processes
                        copyNonEditedRunning = processes[0]
                        currentRunning = [processes[0][0], processes[0][1]]
                        print 'CT:{} || Started ({},P{})'.format(currentTime,currentRunning[0], currentRunning[1])
                else:
                    # We're in the process of running a process, we just display
                    # the progress.
                    if not done:
                        print 'CT:{} || ({},P{}) Running'.format(currentTime,currentRunning[0], currentRunning[1])
            elif(splitData[1] == "INICIA"):
                # No idea what to do here yet
                dummy = 1
            elif(splitData[1] == "TERMINA"):
                # No idea what to do here yet either
                dummy = 1
            elif(splitData[1] == "END"):
                # The client ordered the communication to be done.
                print 'CT:{} || Ending program'.format(currentTime)
            else: # KILLING a process
                # Determine wether that process is still on the list
                for process in processes:
                    if (process[1] == int(splitData[2])):
                        removeTuple = process
                    pass
                # If it is on the list
                if(removeTuple != ()):
                    print 'CT:{} || Killed P{}'.format(currentTime,removeTuple[1])
                    processes.remove(removeTuple)

                    # This happens if we kill an ongoing process
                    if(removeTuple[1] == currentRunning[1]):
                        copyNonEditedRunning = processes[0]
                        currentRunning = [processes[0][0], processes[0][1]]
                        print 'CT:{} || Started ({},P{})'.format(currentTime,currentRunning[0], currentRunning[1])
                    removeTuple = ()
                else:
                    #Not on the list, inform the client it's not in the list
                    print """\
CT:{} || Tried to kill P{}, but it
         has already been killed or
         done processing""".format(currentTime,splitData[2])

            connection.sendall('ACK')
finally:
    #Close the communication
    connection.close()
    sys.exit(0)
    def main(args):
        return 0
        if __name__ == '__main__':
            import sys
            sys.exit(main(sys.argv))
