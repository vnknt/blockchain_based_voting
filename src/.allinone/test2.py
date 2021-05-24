from time import sleep, time
from Network import Network
import socket



test_socket = Network("localhost",5051)

test_socket.start()
test_socket.join_network()

data=0
while(True):
    
    data=input()
   
    if(data=="--nodes"):
        print(test_socket.nodes_in_network)
    elif(data=="--calculate"):
        test_socket.blockchain.calculateVote()
    else:
        test_socket.broadcast(data)
    
