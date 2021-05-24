from Socket import Socket
from Network import Network
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


os.system("color")




# class P2P(Node,Socket):
    
























#     def handle(self,conn,addr):

#         client_ip=None
#         client_port=None
        
#         print_colored(f"{addr} connected to server", "green",5)
        
#         connected = True

   
#         flag = 1

#         msg_buffer=''

#         while (connected):
            
#             full_msg = self.get_message(conn)
#             # msg=conn.recv(2048).decode(self.FORMAT)

#             # msg=msg[self.HEADER_LEN:]
            
            



#             # full_msg=''

#             # new_msg=True
#             # # while(True):
#             # #     if(new_msg):
#             # #         msg=conn.recv(2048).decode(self.FORMAT)

#             # while(True):
#             #     if(new_msg):
#             #         if(flag == 1 ):
#             #             msg=msg_buffer + conn.recv(2048).decode(self.FORMAT)
#             #         else:
#             #             msg=msg_buffer

#             #         #Controlling if msg is bigger than header
#             #         if(len(msg) >=self.HEADER_LEN):
#             #             msg_len=int(msg[:self.HEADER_LEN])
#             #         else:
#             #             msg_buffer=msg
#             #             flag=1
#             #             continue
                
#             #         full_msg+=msg
#             #         if(len(full_msg )-self.HEADER_LEN == msg_len ):
#             #             msg_buffer = full_msg[self.HEADER_LEN  + msg_len:]
#             #             new_msg = False

#             #             break
#             #         elif(len(full_msg )-self.HEADER_LEN > msg_len ):
                        
#             #             msg_buffer = full_msg[self.HEADER_LEN  + msg_len:]
#             #             full_msg = full_msg[:self.HEADER_LEN  + msg_len]
#             #             new_msg = False
#             #             flag = 0
#             #             break
#             #         else:
#             #             msg_buffer=full_msg
#             #             flag=1
#             #             full_msg=''

#             #             continue



#             print(full_msg)
            





















































            
#         #     if (msg_len):
#         #         ind+=1
                


#         #         full_msg=full_msg[self.HEADER_LEN:]
#         #         print(full_msg)

                
#         #         try:
#         #             msg = json.loads(full_msg)
#         #         except:
#         #             print_colored(msg,"green")
                


#         #         try:
#         #             index = self.message_logs.index(msg["id"])

#         #         except:
#         #             index=-1
#         #             self.message_logs.append(msg["id"])


#         #         if(index!=-1):
#         #             continue


#         #         if(len(self.message_logs) >=50000):
#         #             print(f"---{len(self.message_logs)}")
#         #             self.message_logs.pop(0)








#         #         if(commands.NODE_CON_ADDR in msg['title']):                                           #CONNECT TO ME COMMAND
                    
#         #             print_colored(f" {conn.getsockname()}","blue")


#         #             message=msg["message"]


#         #             conn_addr=msg["message"].split(",")                                            #split ip and port
                    
#         #             conn_ip=conn_addr[0]
#         #             conn_port=conn_addr[1]


#         #             client_ip=conn_ip
#         #             client_port=conn_port

                    
#         #             if(client_ip == "" or len(client_ip)==0):


#         #                 peername=conn.getpeername()
#         #                 client_ip=peername[0]


#         #             conn_ip = client_ip
                    
#         #             addr=(client_ip,int(conn_port))

#         #             print_colored(f"{addr} wants to establish connection", "yellow")


#         #             try:
#         #                 conn_index=self.connections.index(addr)     
#         #             except:
#         #                 conn_index=-1

#         #             if conn_index==-1:
#         #                 self.connectToNode(conn_ip,int(conn_port))                      #if connection has not established so far, connect to the node
#         #                 print_colored(f"{addr} Connection Established", "green")

#         #             else:
#         #                 print_colored(f"{addr} 2 Way Connection Established...", "green")

                

#         #         if(commands.CMD_JOIN_MSG in msg):

#         #             mssg = json.dumps(self.getSelfOrAdjacent())
#         #             mssg=f"{commands.MULTI_CONN_ADDR}{mssg}"
                    
#         #             conn.send(f"{mssg}".encode(self.FORMAT))
#         #             #(self.connections)
#         #             pass


#         #         if(commands.ASK_RANDOM_NODE in msg["title"]):
#         #             print_colored(f"{addr} ASKED RANDOM NODE ", "yellow")

#         #             conn_addr=msg["message"].split(",")                                            #split ip and port
                    
#         #             conn_ip=conn_addr[0]
#         #             conn_port=conn_addr[1]

#         #             rndNode=json.dumps(self.getRandomNode())
#         #             self.send(conn,rndNode)
#         #             #conn.send(f"{rndNode}".encode(self.FORMAT))
                    

#         #         if(commands.ASK_NODES_TO_CONNECT in msg["title"]):
#         #             print_colored(f"{addr} ASKED NODES TO CONNECT","yellow",2)
                    
#         #             got_nodes=self.getSelfOrAdjacent()
#         #             message=self.short_json_msg("",got_nodes)
#         #             self.reply(conn,message)
#         #             print("asdasfa------------")
#         #             print(message)
#         #             #conn.send(f"{got_nodes}".encode(self.FORMAT))

#         #         if("#GIVE_NODES_IN_NETWORK" in msg["title"] ):

#         #             node_msg=self.short_json_msg("",self.nodes_in_network)

#         #             print(node_msg)

#         #             self.reply(conn,node_msg)


#         #         if(commands.ASK_CURRENT_CHAIN in  msg["title"] ) :
                    

#         #             # chain_json = jsonpickle.encode(self.blockchain )

#         #             # chain_msg =self.short_json_msg("REPLY",chain_json)

#         #             # self.reply(conn,chain_msg)

#         #             print("\n\nCHAIN ASKED\n\n")

#         #             pass


#         #         if ( self.DISCONNECT_MSG in msg["title"]):
#         #             connected = False
                    
#         #             print_colored(f"{client_ip}:{client_port} DISCONNECTED", "red",2)

#         #             self.remove_connection(conn,addr[0], addr[1])
#         #             break

                
#         #         if("#TRANSACTION" in msg["title"] ):
                    
                  
#         #             transaction = msg["message"]
                
#         #             self.blockchain.addPendingTransaction(transaction)




#         #         if("#BROADCAST" == msg["title"] or  "#TRANSACTION" == msg["title"]):

#         #             self.broadcast(msg,True)
                    
#         #             #print(f'{msg["message"]}')

#         #             if(msg['message']=="#JOINED_IN_NETWORK"):

#         #                 msg_sender_ip   =msg['sender_ip']
#         #                 msg_sender_port =msg['sender_port']
#         #                 if(msg_sender_ip == "" or msg_sender_ip ==None or len(msg_sender_ip) ==0):
#         #                     msg_sender_ip = conn.getpeername()
#         #                     msg_sender_ip= msg_sender_ip[0]

#         #                 print(conn.getpeername())


#         #                 print_colored(f"{msg['sender_ip']}:{msg['sender_port']} has joined to network","green")


#         #                 self.nodes_in_network.append({"ip_addr":msg_sender_ip, "port":msg['sender_port']})
#         #                 print("NODES IN NETWORK ")
#         #                 print(self.nodes_in_network)
#         #         else:
                    
#         #             print(msg["message"])



#         # conn.close()
        
#         # return
