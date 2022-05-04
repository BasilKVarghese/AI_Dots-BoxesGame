#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 14:13:28 2022

@author: basilkvarghese
"""

class Grid():
    
    def __init__(self,rows,columns):
        self.rows = rows
        self.columns = columns
        
    def getGrid(self):
        edges = []
        boxes = []
        for i in range(0,self.rows+1):
            for j in range(0,self.columns+1):
                if((i!=self.rows)):
                    point = ((i,j),(i+1,j))
                    edges.append(point)
                    
                    
                    
                if(j!=self.columns):
                    point = ((i,j),(i,j+1))
                    edges.append(point)
                    
                    
                if((i!=self.rows)&(j!=self.columns)):
                    box = [((i,j),(i+1,j)),((i,j),(i,j+1)),((i,j+1),(i+1,j+1)),((i+1,j),(i+1,j+1))]
                    boxes.append(box)
                
        return {"edges":edges,"boxes":boxes}
    
        
    
class gameState(Grid):
    
    
    def __init__(self,rows,columns,numPlayers=2):
        self.rows = rows
        self.columns = columns
        self.markedEdges = []
        self.remainEdges = self.getGrid()["edges"]
        self.boxes = self.getGrid()["boxes"]
        self.numPlayers = numPlayers
        self.playerBoxes = {}
        self.playerBoxCorners = {}
        for i in range(1,self.numPlayers+1):
            self.playerBoxes[str(i)] = 0
            self.playerBoxCorners[str(i)] = []
        
        self.capture = '0'
            
    def isEndState(self):
        if len(self.remainEdges) == 0:
            return True
        else:
            return False
    
    def getBoxes(self, edge):
        """Returns the edges of boxes that contain the given edge"""
        edgeBoxes = []
        for box in self.boxes:
            if edge in box:
                edgeBoxes.append(box)
        return edgeBoxes
    
    def checkBoxes(self, edge):
        """Checks if choosing an edge creates a new box"""
        edgeBoxes = self.getBoxes(edge)
        #print("\nboxes of edge: ")
        #print(edgeBoxes)
        boxCount = 0
        boxCorners = []
        for box in edgeBoxes:
            if all(elem in self.markedEdges for elem in box):
                boxCorners.append((box[0][0],box[2][1]))
                boxCount = boxCount+1
        return {"boxcount":boxCount,"boxcorners":boxCorners}
    
    def generateSuccessor(self,edge,player):
        
        #state = gameState(self,self.rows,self.columns)
        
        remainEdges = self.remainEdges
        markedEdges = self.markedEdges
        
        remainEdges.remove(edge)
        markedEdges.append(edge)
        
        self.remainEdges = remainEdges
        self.markedEdges = markedEdges
        newBoxes = self.checkBoxes(edge)['boxcount']
        self.playerBoxCorners[player].extend(self.checkBoxes(edge)['boxcorners'])
        self.playerBoxes[player] = self.playerBoxes[player]+newBoxes
        if newBoxes == 0:
            self.capture ='0'
        else:
            self.capture = player

    def evaluateState(self):
         score = self.playerBoxes['2'] - (self.playerBoxes['1'])
        #  if score < 0:
        #      score = -999999
        #  elif score > 0:
        #      score = 999999

         return score
    

    def getWinner(self):
        if self.isEndState() == True:
            return max(self.playerBoxes.items(), key=lambda x : x[1])[0]
        else:
            return False
        
    def printState(self):
        print("Marked Edges: ",self.markedEdges)
        print("Remaining Edges: ",self.remainEdges)
        print("Player Boxes: ",self.playerBoxes)
            
        

# game = ['0010','0001','0102','0212','1222','2122','2021','1020','1112','0111','1011','1121','0203','0304','1213','0313','1314']

# grid1 = gameState(2,2)
# #edges = grid1.getGrid()['edges']
# #boxes = grid1.getGrid()['boxes']
# #gameState.isEndState() == False
# i=0
# nextPly = '1'
# while(i<16):
#     if grid1.isEndState() == True:
#         print("Game Over")
#         print("winner is player",grid1.getWinner())
#         break
#     else:    
#         if grid1.capture =='0':
#             ply = nextPly
#         else:
#             ply = grid1.capture
#         print("\nPlayer ",ply)
#         #print("Marked Edges: ", grid1.markedEdges)
#         #print("Remaining Edges", grid1.remainEdges)
#         #edge = input()
#         #print("i: ",i)
#         edge = game[i]
#         #print("EDGE: ",edge)
#         edge = ((int(edge[0]),int(edge[1])),(int(edge[2]),int(edge[3])))
#         print("EDGE: ",edge)
#         grid1.generateSuccessor(edge,ply)
#         #print("Marked Edges: ", grid1.markedEdges)
#         #print("Remaining Edges", grid1.remainEdges)
#         for j in range(1,3):
#             print("Boxes by player ",j,": ",grid1.playerBoxes[str(j)] )
        
#         if ply == '1':
#             nextPly = '2'
#         else:
#             nextPly = '1'
#         i = i+1
    
    


    