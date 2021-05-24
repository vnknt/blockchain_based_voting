import socket
import time
import threading
# import commands
import random
import json
import hashlib
# from settings.terminal_set import bcolors
# from helpers.terminal_helper import print_colored
import os

import jsonpickle
# import Node
# from Node import Node
from Message import Message
from Network import Network











class BallotBoxNetwork(Network):


    def __init__(self,ip="",port=None):
        super().__init__(ip,port)


    def startBallotBox(self,port):
        super().start(port)


    def connect_to_node(self,address,port):
        print(f"_______{address}_{port}_______________________-")
        self.CONN_ADDR=(address,port)

        if(self.CONN_ADDR not in self.connections):

            connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            connection.connect(self.CONN_ADDR)

            x={"ip_addr":address,"port":port}

            self.nodes.append(connection)
            self.connections.append(self.CONN_ADDR)
            self.connections_json.append(x)
    def join_network(self    ,ip=None,port=None):
        
        if ip==None:
            ip=self.GENESIS_NODE_ADDR
        if port==None:
            port=self.GENESIS_NODE_PORT


        print(f"{ip}{port}")
        conn=self.create_connection(ip, port)


 
        random_node = self.ask_random_node(conn)
        print(random_node)
        node = jsonpickle.decode(random_node)

        print(f"------->{node}")
        if node==None:

            self.remove_connection(conn, ip, port)

            print("Network is not exist...")
            print("Connecting to Genesis Node",end="\n\n")

            self.connect_to_node(self.GENESIS_NODE_ADDR, self.GENESIS_NODE_PORT)
            print("asadasd")
        else:
            """
                Ask adjacent from random node that given by network
            """
            self.remove_connection(conn, ip, port)
            

            print(node["ip_addr"])

            self.ask_nodes(node["ip_addr"], node["port"])



            

  
    
