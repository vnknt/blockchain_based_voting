from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PIL import Image,ImageDraw,ImageFont
import qrcode
import sys
import time
import jsonpickle
from  Blockchain import VoteTransaction

from Network import Network
from Node import Node
from BallotBoxNetwork import BallotBoxNetwork
import json
import argparse
import os
class BallotBox:

    def __init__(self,number) :
        self.number=number
        self.node = BallotBoxNetwork()
        self.node.join_network()
        
        self.last_paper_id=1

class Voter: 
    
    voterId=1
    @classmethod
    def GetVoter(cls):
        cls.voterId+=1
        return cls.voterId


class BallotPaper:
    def __init__(self):
        self.area_height=175
        self.most_left_position=110
        self.ypos=200
        pass
    


    def create_paper(self,transaction:VoteTransaction):
        dir = f"./ballots/{ballotBox.number}"
        if(not os.path.exists(dir)):
            os.makedirs(dir)
            print("dir maked")

        self.xposition = self.most_left_position+(transaction.selection-1)*self.area_height
        vote_header={"transaction_id":transaction.transaction_id,"selection":transaction.selection}
    
        qr =QrCode()
        qr_code = qr.create_qr_code(json.dumps(vote_header))

        image = Image.open("pusula.png")
        
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("font.ttf", 70)
        draw.text((self.xposition, self.ypos), "X", fill=(255, 0, 0),font=font)
        pos = (image.size[0] - qr_code.size[0], image.size[1] - qr_code.size[1])
        image.paste(qr_code, pos)
        image.save(f"./ballots/{ballotBox.number}/{ballotBox.last_paper_id}.png")
        print("saved")
        



class QrCode:

    def create_qr_code(self,data):
        
        qr = qrcode.QRCode(box_size=4)
        
        qr.add_data(data)

        qr.make()
        img_qr = qr.make_image()
        return img_qr


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 300)
        Dialog.setMinimumSize(QtCore.QSize(300, 300))
        font = QtGui.QFont()
        font.setFamily("Arial")
        Dialog.setFont(font)
        Dialog.setStyleSheet("")
        self.selection1 = QtWidgets.QPushButton(Dialog)
        self.selection1.setGeometry(QtCore.QRect(20, 70, 111, 81))
        self.selection1.setStyleSheet("font-size:14pt;\n"
                                        "font-weight:bold;\n"
                                        "background:#F9C74F;\n"
                                        "color:black;")
        self.selection1.setObjectName("selection1")
        self.selection1.clicked.connect(lambda: self.vote(1))



        self.selection2 = QtWidgets.QPushButton(Dialog)
        self.selection2.setGeometry(QtCore.QRect(170, 70, 111, 81))
        self.selection2.setStyleSheet("font-size:14pt;\n"
                                        "font-weight:bold;\n"
                                        "background:#003566;\n"
                                        "color:white;")
        self.selection2.setObjectName("selection2")
        self.selection2.clicked.connect(lambda: self.vote(2))



        self.selection3 = QtWidgets.QPushButton(Dialog)
        self.selection3.setGeometry(QtCore.QRect(20, 190, 111, 81))
        self.selection3.setStyleSheet("font-size:14pt;\n"
                                        "font-weight:bold;\n"
                                        "background:#007200;\n"
                                        "color:white;")

        self.selection3.setObjectName("selection3")

        self.selection3.clicked.connect(lambda: self.vote(3))



        self.selection4 = QtWidgets.QPushButton(Dialog)
        self.selection4.setGeometry(QtCore.QRect(170, 190, 111, 81))
        
        self.selection4.setStyleSheet("font-size:14pt;\n"
                                        "font-weight:bold;\n"
                                        "background:#D62828;\n"
                                        "color:white;\n"
                                        "selection-color:#000000")
        self.selection4.setObjectName("selection4")
        self.selection4.clicked.connect(lambda: self.vote(4))






        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 20, 181, 21))
        self.label.setStyleSheet("font-size:12.5pt\n")
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "BALLOT BOX"))
        self.selection1.setText(_translate("Dialog", "A"))
        self.selection2.setText(_translate("Dialog", "B"))
        self.selection3.setText(_translate("Dialog", "C"))
        self.selection4.setText(_translate("Dialog", "D"))
        self.label.setText(_translate("Dialog", "YOUR SELECTION?"))
        pass
        
    

    def vote(self,selection):

        
        vote = VoteTransaction(1,Voter.GetVoter(),selection,time.time() )
        print(vote.__dict__)


        transaction = jsonpickle.encode(vote)
        
        ballotBox.node.broadcast(transaction,title="#TRANSACTION")
        paper = BallotPaper()
        paper.create_paper(vote)
        ballotBox.last_paper_id+=1

        #msg.exec_()
        

def window():

        app = QtWidgets.QApplication(sys.argv)
        style="""QPushbutton:hover#selection1{
                color:#ff0000;}
                """
        app.setStyleSheet(style)
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        sys.exit(app.exec_())



def window():

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())



if __name__=='__main__':

    
    parser = argparse.ArgumentParser(description='Ballot box')
    
    parser.add_argument('-n', '--number', metavar='number', required=True, help='ballot box number')

    args = parser.parse_args()

    print(args.number) 
    

    ballotBox = BallotBox(args.number)
    

    window()
