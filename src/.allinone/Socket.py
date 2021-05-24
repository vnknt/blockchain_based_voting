
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

class Socket():
    
    HEADER_LEN = 10     
    FORMAT = "utf-8"
    DISCONNECT_MSG = "!DISCONNECT"
    CONN_PORT    =None
    CONN_ADDR    =None
    SERVER_IP=socket.gethostbyname(socket.gethostname())
    SERVER_PORT=None
    SERVER_ADDR=None

    def __init__(self,ip=SERVER_IP,port=SERVER_PORT):


        self.SERVER_IP=ip
        self.SERVER_PORT=port
        self.SERVER_ADDR=(ip,port)
        

    def bindAndListen(self,handler_func):
      
        self.SERVER_ADDR = (self.SERVER_IP, self.SERVER_PORT)

        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        self.server.bind(self.SERVER_ADDR)

        
        print(f"[LISTENING...-->]{self.SERVER_PORT}")

        self.server.listen()

        while True:

            (conn,addr)=self.server.accept()
            print(conn,addr)
            thread=threading.Thread(target=handler_func,args=(conn,addr))
            thread.start()



    def start(self,handler_func):

        thread = threading.Thread(target=self.bindAndListen, args=(handler_func,))
        thread.start()
        return
    


    def create_connection(self,ip,port):

        CONN_ADDR=(ip,port)
        connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connection.connect(CONN_ADDR)
        return connection




    
