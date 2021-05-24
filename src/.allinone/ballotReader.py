from os import read
import cv2 
import numpy as np
from pyzbar.pyzbar import decode
from  mss import mss
from PIL import Image
import pyautogui
from BallotReaderNetwork import BallotReaderNetwork
import math
import json
from Network import Network 
import commands
from settings.terminal_set import bcolors
from helpers.terminal_helper import print_colored


sct = mss()

last_qr=None

selections=dict()
parties=["","A","B","C","D"]







class BallotReader:

    def __init__(self) :
        
        self.node = BallotReaderNetwork()
        self.node.join_network()
        

    def readingVote(self,transaction_id):
        
        self.node.nodes

        msg = self.node.short_json_msg(commands.VOTE_READING,transaction_id)

        readingResponse= self.node.send(self.node.nodes[0] , msg , 1) 
        response = json.loads(readingResponse)
        
        return response["message"]










reader  = BallotReader()




while 1:
    w, h = 1920, 1024
    xpos,ypos  = pyautogui.position()

    monitor = {'top': ypos, 'left': xpos, 'width': 300, 'height':300}
    
    img = Image.frombytes('RGB', (300,300), sct.grab(monitor).rgb)
    img=np.array(img)


    for barcode in decode(img):

        points=np.array([barcode.polygon],np.int32)
        points = points.reshape((-1,1,2))
        cv2.polylines(img,[points],True,(255,0,255),5)





        if( not barcode.data.decode("utf-8")==last_qr ):

            last_qr = barcode.data.decode("utf-8")

            data = json.loads(last_qr)
            readingResponse = reader.readingVote(data["transaction_id"])

            if(readingResponse == "success"):
                print_colored("Oy başarıyla sayıldı","green")
                if(data["selection"] in selections):
                    selections[data["selection"]]+=1
                else:
                    selections[data["selection"]] = 1
                for key in selections:
                    print(parties[key],selections[key])

            if(readingResponse =="already_counted"):

                print_colored("Bu oy, zaten daha önce sayıldı","yellow")

            if(readingResponse == "not_exists"):
                print_colored("Geçersiz Oy","red")
            
            
        

 
    cv2.imshow('test', cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    