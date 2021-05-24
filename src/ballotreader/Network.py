import jsonpickle
from Connection import Connection
from Socket import Socket
from Blockchain import Blockchain
from Node import Node
import socket
import time
import threading
import commands
import random
import json
import hashlib

from settings.terminal_set import bcolors
from helpers.terminal_helper import print_colored
from Message import Message

import os

import config
os.system("color")



# class EventHandler1:
#     def join(self):

#     pass







class Network(Connection,Socket):

    def __init__(self,ip="",port=None):
        if(ip==""):
            ip=config.SELF_STATIC_IP
        if(ip=="localhost"):
            ip = socket.gethostbyname(socket.gethostname())
        Socket.__init__(self,   ip,port)
        Connection.__init__(self,ip,port)
        self.SERVER_IP=ip
        self.blockchain = Blockchain()
        self.nodes_in_network.append({"ip_addr":self.GENESIS_NODE_ADDR,"port":self.GENESIS_NODE_PORT})
        self.counted_votes=list()


    def broadcast(self,data,isJson=False,title="#BROADCAST"):

        if isJson==False:
            msg = self.short_json_msg(title,data)
        else:
            msg=data

        try:
            index = self.message_logs.index(msg["id"])

        except:
            index=-1
            self.message_logs.append(msg["id"])




        for node in self.nodes:

            try:
                self.send(node,msg) 

            except:
                pass
                #print_colored("MESSAGE COULDN'T SEND, RECIEVER MAY BE DISCONNECTED ","red")

    

    def join_network(self   ,ip=None,port=None):
        
        if ip==None:
            ip=self.GENESIS_NODE_ADDR
        if port==None:
            port=self.GENESIS_NODE_PORT


        print(f"{ip}{port}")
        conn=self.create_connection(ip, port)

        random_node = self.ask_random_node(conn)
        
        node = json.loads(random_node)
        

        if node==None:
            self.remove_connection(conn, ip, port)
            print("Network is not exist...")
            print("Connecting to Genesis Node",end="\n\n")
            self.connect_to_node(self.GENESIS_NODE_ADDR, self.GENESIS_NODE_PORT)
            
        else:

            self.remove_connection(conn, ip, port)
            
            self.ask_nodes(node["ip_addr"], node["port"])
            

            
        temp_node = self.nodes[0]
        
        



        

        broadcast_msg=Message(self.SERVER_IP,self.SERVER_PORT).msg("#JOINED_IN_NETWORK","#BROADCAST")

        self.broadcast(broadcast_msg,isJson=True)
        msg=Message().short_msg(commands.GIVE_NODES_IN_NETWORK,"")

        nodes = self.send(temp_node,msg,1)


      
        nodes=json.loads(nodes)

        nodes=nodes["message"]



        for node in nodes:
            
            try:
                index = self.nodes_in_network.index(node)
            except:
                index = -1

            if index ==-1 :

                self.nodes_in_network.append(node)




        random_conn_id=random.randint(0,len(self.nodes)-1)
        random_conn = self.nodes[random_conn_id]
        chain = self.ask_blockchain(random_conn)
        print_colored("Chain Recieved","green")






    def ask_blockchain(self,conn):

        message=self.short_json_msg(commands.ASK_CURRENT_CHAIN,"")
        chain = self.send(conn,message,1)
        chain=json.loads(chain)
        
        chain:Blockchain=jsonpickle.decode(chain["message"])
        print(chain.chain[-1].data[-1].__dict__)
        
        self.blockchain=chain




    def ask_nodes(self,ip,port):

        conn = self.create_connection(ip, port)

        msg_json=self.short_json_msg(commands.ASK_NODES_TO_CONNECT,"")

        msg = self.send(conn,msg_json,1)

        disconnect_msg=self.short_json_msg(self.DISCONNECT_MSG)

        self.send(conn,disconnect_msg)

        msg=json.loads(msg)

        nodes=msg["message"]


        print_colored(f"{len(nodes)} Node address recieved...","cyan")


        for node in nodes:
            self.connect_to_node(node["ip_addr"], node["port"])
            


            
    def ask_random_node(self,conn):

    
        message=self.short_json_msg(commands.ASK_RANDOM_NODE,f"{self.SERVER_IP},{self.SERVER_PORT}")
        
        msg = self.send(conn,message,1)
        
        
        disconnect_msg=self.short_json_msg(self.DISCONNECT_MSG)

        self.send(conn,disconnect_msg)
        
        return msg



    def connect_to_node(self,ip,port):
        
        print(f"_______{ip}_{port}_______________________-")

        self.CONN_ADDR=(ip,port)

        if(self.CONN_ADDR not in self.connections):

            connection=self.node_socket.create_connection(ip,port)

            x={"ip_addr":ip,"port":port}

            self.nodes.append(connection)

            self.connections.append(self.CONN_ADDR)

            self.connections_json.append(x)


            msg=self.short_json_msg(commands.NODE_CON_ADDR,f"{self.SERVER_IP},{self.SERVER_PORT}")
            
            self.send(connection,msg)



        print_colored(f"Connected To->{ip}:{port}","green",2)
        return


