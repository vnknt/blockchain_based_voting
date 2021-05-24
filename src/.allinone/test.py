from Network import Network





test_socket = Network("localhost",5050)
test_socket.start()
test_socket.blockchain.isChainUpToDate=True


data=input
while(True):
    data=input()
    if(data=="--nodes"):
        print(test_socket.nodes_in_network)
    elif(data=="--calculate"):
        test_socket.blockchain.calculateVote()
    else:
        test_socket.broadcast(data)
    

