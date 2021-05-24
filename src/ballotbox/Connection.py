from Blockchain import Blockchain
import jsonpickle
from Node import Node
from Socket import Socket
import commands
import json
from settings.terminal_set import bcolors
from helpers.terminal_helper import print_colored
from Message import Message
import os


os.system("color")
class Connection(Node):
    HEADER_LEN = 10     
    FORMAT = "utf-8"


    








    def __init__(self, ip, port):
        self.node_socket = Socket(ip,port)

    def start(self):
        self.node_socket.start(self.handle)

    def handle(self,conn,addr):
        client_ip=None
        client_port=None
        print_colored(f"{addr} connected to server", "green",5)
        connected = True
        msg_buffer=''
        flag = 1
        while (connected):
            full_msg=''
            new_msg=True

            while(True):
                if(new_msg):
                    if(flag == 1 ):
                        msg=msg_buffer + conn.recv(2048).decode(self.FORMAT)
                    else:
                        msg=msg_buffer

                    #Controlling if msg is bigger than header
                    if(len(msg) >=self.HEADER_LEN):
                        msg_len=int(msg[:self.HEADER_LEN])
                    else:
                        msg_buffer=msg
                        flag=1
                        continue
                
                    full_msg+=msg
                    if(len(full_msg )-self.HEADER_LEN == msg_len ):
                        msg_buffer = full_msg[self.HEADER_LEN  + msg_len:]
                        new_msg = False

                        break
                    elif(len(full_msg )-self.HEADER_LEN > msg_len ):
                        msg_buffer = full_msg[self.HEADER_LEN  + msg_len:]
                        full_msg = full_msg[:self.HEADER_LEN  + msg_len]
                        new_msg = False
                        flag = 0
                        break
                    else:
                        msg_buffer=full_msg
                        flag=1
                        full_msg=''

                        continue

                

            msg=full_msg[self.HEADER_LEN:]
            msg=json.loads(msg)
            try:
                index = self.message_logs.index(msg["id"])
            except:
                index=-1
                self.message_logs.append(msg["id"])


            if(index!=-1):
                continue


            if(len(self.message_logs) >=50000):
                
                self.message_logs.pop(0)



           

            if(commands.NODE_CON_ADDR in msg['title']):                                           #CONNECT TO ME COMMAND
                

                message=msg["message"]


                conn_addr=msg["message"].split(",")                                            #split ip and port
                
                conn_ip=conn_addr[0]
                conn_port=conn_addr[1]


                client_ip=conn_ip
                client_port=conn_port

                
                if(client_ip == "" or len(client_ip)==0):
                    peername=conn.getpeername()
                    client_ip=peername[0]

                conn_ip = client_ip
                addr=(client_ip,int(conn_port))
                print_colored(f"{addr} wants to establish connection", "yellow")



                try:
                    conn_index=self.connections.index(addr)     
                except:
                    conn_index=-1




                if conn_index==-1:
                    self.connect_to_node(conn_ip,int(conn_port))                      #if connection has not established so far, connect to the node
                    print_colored(f"{addr} Connection Established", "green")
                else:
                    print_colored(f"{addr} 2 Way Connection Established...", "green")

        
            if(commands.VOTE_READING in msg["title"]):
                #self.blockchain:Blockchain
                transaction_id = msg["message"]
                isExist = self.blockchain.findTransaction(transaction_id)

                if(isExist == -1):
                    response=self.short_json_msg("","not_exists")
                    self.reply(conn,response)
                    print_colored("this vote does not_exist","red")
                elif(isExist):
                    if(transaction_id in self.counted_votes):
                        response=self.short_json_msg("","already_counted")
                        self.reply(conn,response)
                        print_colored("this vote already counted","yellow")
                    else:
                        response=self.short_json_msg("","success")
                        print_colored("successfully counted","green")
                        self.reply(conn,response)
                        msg=self.short_json_msg(commands.VOTE_COUNTED,transaction_id)
                        self.counted_votes.append(transaction_id    )
                        self.broadcast(msg)

                pass
            
            if(commands.VOTE_COUNTED in msg["title"]):
                
                self.counted_votes.append(msg["title"])
                print_colored("successfully counted","green")
                






            if(commands.ASK_NODES_TO_CONNECT in msg["title"]):
                print_colored(f"{addr} ASKED NODES TO CONNECT","yellow",2)
                got_nodes=self.getSelfOrAdjacent()
                message=self.short_json_msg("",got_nodes)
                self.reply(conn,message)
                #print(message)

 

            if ( commands.DISCONNECT_MESSAGE in msg["title"]):
                connected = False
                print_colored(f"{client_ip}:{client_port} DISCONNECTED", "red",2)
                self.remove_connection(conn,addr[0], addr[1])
                break



            if(commands.ASK_RANDOM_NODE in msg["title"]):
                print_colored(f"{addr} ASKED RANDOM NODE ", "yellow")
                conn_addr=msg["message"].split(",")                                            #split ip and port
                conn_ip=conn_addr[0]
                conn_port=conn_addr[1]
                rndNode=self.getRandomNode()
                #print(rndNode)
                self.reply(conn,rndNode)
                
            if(commands.GIVE_NODES_IN_NETWORK in msg['title'] ):
                print_colored("GIVE_NODES_IN_NETWORL")
                node_msg=self.short_json_msg("",self.nodes_in_network)
                self.reply(conn,node_msg)

            if(commands.JOINED_IN_NETWORK in msg["title"] ):
                node_msg=self.short_json_msg("",self.nodes_in_network)
                self.reply(conn,node_msg)



            if("#TRANSACTION" in msg["title"] ):
                transaction = msg["message"]
                self.blockchain.addPendingTransaction(transaction)
            



            if(commands.ASK_CURRENT_CHAIN in  msg["title"] ) :
                

                chain_json = jsonpickle.encode(self.blockchain)

                chain_msg =self.short_json_msg("REPLY",chain_json)

                self.reply(conn,chain_msg)

                print("\n\nCHAIN ASKED\n\n")

                



            if("#BROADCAST" == msg["title"] or  "#TRANSACTION" == msg["title"]):

                self.broadcast(msg,True)
                
                print(f'Broadcast msg : { msg["message"]}')
                if(msg['message']=="#JOINED_IN_NETWORK"):

                    msg_sender_ip   =msg['sender_ip']
                    msg_sender_port =msg['sender_port']
                    if(msg_sender_ip == "" or msg_sender_ip ==None or len(msg_sender_ip) ==0):
                        msg_sender_ip = conn.getpeername()
                        msg_sender_ip= msg_sender_ip[0]

                    


                    print_colored(f"{msg['sender_ip']}:{msg['sender_port']} has joined to network","green")


                    self.nodes_in_network.append({"ip_addr":msg_sender_ip, "port":msg['sender_port']})
      
                
    



    def send(self,conn,msg,hasResponse=0):

        message=self.encode_message(msg)
        
        conn.send(message)
        

        if(hasResponse):
            
            msg=self.get_message(conn)
            #msg = conn.recv(4096).decode(self.FORMAT)
            
        else:
            msg=""
        return msg[self.HEADER_LEN:]
    

    def reply(self,conn,msg):
        
        message=self.encode_message(msg)
        conn.send(message)
        
    
    def encode_message(self,msg):
    
        message=json.dumps(msg)
        temp_len=len(message)
        message=f'{temp_len:^{self.HEADER_LEN}}'+message
        message=message.encode(self.FORMAT)
        return message


    def get_message(self,conn):

        full_msg=''
        new_msg=True
        flag=1
        msg_buffer=''
        while(True):

            if(new_msg):

                if(flag == 1 ):

                    msg=msg_buffer + conn.recv(2048).decode(self.FORMAT)
                else:
                    msg=msg_buffer
                #Controlling if msg is bigger than header
                if(len(msg) >=self.HEADER_LEN):
                    msg_len=int(msg[:self.HEADER_LEN])
                else:
                    msg_buffer =msg
                    flag=1
                    
                    continue
            
                full_msg+=msg
                if(len(full_msg )-self.HEADER_LEN == msg_len ):
                    msg_buffer = full_msg[self.HEADER_LEN  + msg_len:]
                    new_msg = False

                    break
                elif(len(full_msg )-self.HEADER_LEN > msg_len ):
                    msg_buffer = full_msg[self.HEADER_LEN  + msg_len:]
                    full_msg = full_msg[:self.HEADER_LEN  + msg_len]
                    new_msg = False
                    flag = 0
                    break
                else:
                    msg_buffer=full_msg
                    flag=1
                    full_msg=''

                    continue

        return full_msg
