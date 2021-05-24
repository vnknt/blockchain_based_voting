from array import array
from hashlib import sha256
import hashlib
from helpers.terminal_helper import print_colored

import json

import time
from typing import Type
import jsonpickle




class VoteTransaction:

    def __init__(self,ballotBoxId,voterId,selection,timestamp) -> None:

        self.ballotBoxId = ballotBoxId

        self.voterId = voterId

        self.selection=selection

        self.timestamp = timestamp
        
        self.transaction_id = self.calculateHash()

    def __eq__(self,other):
        if (isinstance(other, VoteTransaction)):
            return self.ballotBoxId == other.ballotBoxId \
                    and self.selection == other.selection \
                    and self.voterId == other.voterId \
                    and self.timestamp == other.timestamp

    def calculateHash(self):
            return sha256( f"{self.ballotBoxId},{self.voterId},{self.timestamp},{self.selection}".encode()).hexdigest()



class Block:
    def __init__(self,timestamp,data,previousHash):
        
        self.timestamp=timestamp
        self.previousHash = previousHash
        self.data:list(VoteTransaction)=data
        
        self.nonce=0
        self.hash=self.calculateHash()
        
    def calculateHash(self):
        return sha256( f"{self.previousHash},{jsonpickle.encode(self.data)},{self.nonce}".encode()).hexdigest()

    def mine(self,difficulty):
        zeros='0'*difficulty
        print(zeros)
        while(self.hash[0:difficulty] != zeros  ):
            self.hash=self.calculateHash()
            self.nonce+=1
        print(self.hash)
        pass





class Blockchain:
    


    def __init__(self):
        self.isChainUpToDate=False
        self.chain=[self.generateGenesisBlock()]

        self.difficulty=0

        self.pendingTransaction=[]

        self.transaction_buffer_size=20

        self.transactions_in_block=5

    def generateGenesisBlock(self)->Block:
        transaction = VoteTransaction(1,1,-1,1)
        return  Block(timestamp=1,data=[transaction],previousHash= sha256("Hello world".encode()).hexdigest())


    def getLatestBlock(self)->Block:
        return self.chain[-1]


    def isChainValid(self)->bool:
        i=1
        while(i<len(self.chain)):
            if(self.chain[i].previousHash != self.chain[i-1].hash):
                return False
            i+=1
        return True



    def calculateVote(self):
        selection=dict()
        parties=["","A","B","C","D"]
        for block in self.chain :
 
            transactions=block.data
            for transaction in transactions :

                if(transaction.selection in selection):
                    selection[transaction.selection]+=1
                else:
                    selection[transaction.selection]=1

        for transaction in self.pendingTransaction:
                if(transaction.selection in selection):
                    selection[transaction.selection]+=1
                else:
                    selection[transaction.selection]=1

        print("\n\n")
        print("SELECTON\tTOTAL VOTE")
        print("_________\t__________")
        for i in selection:
            if(i==-1):
                continue
            print(f"{parties[i]}\t\t\t{selection[i]}")
    



    def addPendingTransaction(self,transaction):
        transaction_obj = jsonpickle.decode(transaction)
        
        
        self.pendingTransaction.append(transaction_obj)
        self.sortTransactions()
        print("Transaction is added : latest transaction")
        #print(self.chain[-1].data[-1].__dict__)
        
        if(len(self.pendingTransaction)>=5):
            self.createBlock()
        
            


    def find_pending_transaction(self,transaction:VoteTransaction)->int: 

        for t in self.pendingTransaction:
            if(t==transaction):
                return self.pendingTransaction.index(t)
        return None




    def sync_chain(self,recieved_chain):


        recieved_chain:Blockchain=recieved_chain
        
        recieved_last_transaction=recieved_chain.getLastTransaction()

        index = self.find_pending_transaction(recieved_last_transaction)
        if(index!=-1):
            transactions=self.pendingTransaction[index:]
            self.pendingTransaction=[]
            self.chain=recieved_chain

            self.chain.isChainValid=True
            for transaction in transactions:
                self.addPendingTransaction(transaction)


    def findTransaction(self,transaction_id):
        for block in self.chain:
           
            for transaction in block.data:
                
                if transaction.transaction_id == transaction_id:
                    return 1
        
        return -1

        



    def sortTransactions(self):
        pass
        #self.pendingTransaction = sorted(self.pendingTransaction,key=lambda x: x.timestamp)


    def getLastTransaction(self):
        return self.chain[-1].data


            
    def checkIsChainUpToDate(func):
        def wrapper( self , *args, **kwargs):
            if(self.isChainUpToDate):
                func(self,*args,**kwargs)
            self.sortTransactions()
        return wrapper





    @checkIsChainUpToDate
    def createBlock(self):
        block  = Block(time.time(),self.pendingTransaction[0:5] ,self.getLatestBlock().hash)
        self.pendingTransaction = self.pendingTransaction[5:]
        block.mine(self.difficulty)
        print("block is mined")
        self.chain.append(block)




    def printBlocks(self):
        print(self.chain)

