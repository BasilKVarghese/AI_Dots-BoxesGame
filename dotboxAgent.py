import numpy as np
#from dotBox import gameState
import copy
import random
from statistics import mean
import ast
from collections import Counter

class gameAgent():
    def __init__(self,gameState,depth):
        #print("Invoke Game agent")
        self.gameState = gameState
        self.depth = depth
        self.nodes = 0
        self.probabs = {}

    def getPacVal(self,gameState,depth):
            
        """Defining maximizer"""
        
        if (depth == self.depth) | (gameState.getWinner() != False):
            
            return {'score':gameState.evaluateState(),'action':""}
        else :   
            
            legalMoves = gameState.remainEdges
            random.shuffle(legalMoves)
            max_score = float("-inf")
            for action in legalMoves:
                self.nodes = self.nodes+1
                copyState = copy.deepcopy(gameState)
                copyState.generateSuccessor(action,'2')
                if copyState.capture == '2':
                    score = self.getPacVal(copyState,depth)['score']
                else:
                    score = self.getGhostVal(copyState,depth)
                if score>max_score:
                    max_score = score
                    max_action = action
            return {'score': max_score,'action':max_action}


    def getGhostVal(self,gameState,depth):
            
            """Defining minimizer"""
            
            if (depth == self.depth) | (gameState.getWinner() != False):
                #print("Exit condition reached at ghost")
                #gameState.printState()
                return gameState.evaluateState()
            else:

                legalMoves = gameState.remainEdges
                random.shuffle(legalMoves)
                actionScores = []
                for action in legalMoves:
                    self.nodes = self.nodes+1
                    copyState = copy.deepcopy(gameState)
                    copyState.generateSuccessor(action,'1')
                    if copyState.capture == '1':
                        score = self.getGhostVal(copyState,depth)
                    else:
                        score = self.getPacVal(copyState,depth+1)['score']
                    actionScores.append(score)
                return min(actionScores)

    def getEdge_minimax(self):
        """Calling the maximizer of root node : pacman state"""  
    
        print('Running Minimax Algorithm')
        result = self.getPacVal(self.gameState,0)
        max_action = result["action"]
        print("Nodes Expanded: ", self.nodes)
        return {"max_action":max_action,"nodes":self.nodes}

    def getPacVal_AB(self,gameState,depth,alpha,beta):
             
            """Defining maximizer with alpha/beta pruning"""  
        
            if (depth == self.depth) | (gameState.getWinner() != False):
                return {'score':gameState.evaluateState(),'action':""}
            else :   
                legalMoves = gameState.remainEdges
                random.shuffle(legalMoves)
                max_score = float("-inf")
                for action in legalMoves:
                    #if depth == 0:
                        #print("Action",action)
                    self.nodes = self.nodes+1
                    copyState = copy.deepcopy(gameState)
                    copyState.generateSuccessor(action,'2')
                    if copyState.capture == '2':
                        score = self.getPacVal_AB(copyState,depth,alpha,beta)['score']

                    else:
                        score = self.getGhostVal_AB(copyState,depth,alpha,beta)
                    if score > max_score:
                        max_score = score
                        max_action = action
                    if max_score > beta:
                        #if depth == 0:
                            #print('Score Prune:',max_score)
                            #print("Max Action Prune:",max_action)
                        return {'score': max_score,'action':max_action}
                    alpha = max(alpha,max_score)
                #if depth == 0:    
                    #print("Score:",max_score)
                    #print("Max Action:",max_action)
                return {'score': max_score,'action':max_action}

    def getGhostVal_AB(self,gameState,depth,alpha,beta):
        if (depth == self.depth) | (gameState.getWinner() != False):
            #print("Exit condition reached at ghost")
            #gameState.printState()
            return gameState.evaluateState()
        else:
            legalMoves = gameState.remainEdges
            random.shuffle(legalMoves)
            min_score = float("inf")
            for action in legalMoves:
                self.nodes = self.nodes+1
                copyState = copy.deepcopy(gameState)
                copyState.generateSuccessor(action,'1')
                if copyState.capture == '1':
                    score = self.getGhostVal_AB(copyState,depth,alpha,beta)
                else:
                    score = self.getPacVal_AB(copyState,depth+1,alpha,beta)['score']
                if score < min_score:
                    min_score = score
                    if min_score < alpha:
                        return min_score
                    beta = min(beta,min_score)
            return min_score

    def getEdge_AB(self):
        alpha = float("-inf")
        beta = float("inf")    
        print('Running alpha/beta Algorithm')
        """Calling the maximizer of root node : pacman state"""   
        AB_res = self.getPacVal_AB(self.gameState,0,alpha,beta)
        max_action = AB_res["action"]
        score = AB_res["score"]
        #print("Final Action:",max_action)
        #print("FInal Score: ",score)
        #print("Node Expanded",self.nodes)
        return {"max_action":max_action,"nodes":self.nodes}
         
    def getPacVal_Exp(self,gameState,depth):
                
            """Defining maximizer"""
            
            if (depth == self.depth) | (gameState.getWinner() != False):
                
                return {'score':gameState.evaluateState(),'action':""}
            else :   
                
                legalMoves = gameState.remainEdges
                random.shuffle(legalMoves)
                max_score = float("-inf")
                for action in legalMoves:
                    self.nodes = self.nodes+1
                    copyState = copy.deepcopy(gameState)
                    copyState.generateSuccessor(action,'2')
                    if copyState.capture == '2':
                        score = self.getPacVal_Exp(copyState,depth)['score']
                    else:
                        score = self.getGhostVal_Exp(copyState,depth)
                    if score>max_score:
                        max_score = score
                        max_action = action
                return {'score': max_score,'action':max_action}

    def getGhostVal_Exp(self,gameState,depth):
                
                """Defining minimizer"""
                
                if (depth == self.depth) | (gameState.getWinner() != False):
                    #print("Exit condition reached at ghost")
                    #gameState.printState()
                    return gameState.evaluateState()
                else:

                    legalMoves = gameState.remainEdges
                    random.shuffle(legalMoves)
                    actionScores = []
                    for action in legalMoves:
                        self.nodes = self.nodes+1
                        copyState = copy.deepcopy(gameState)
                        copyState.generateSuccessor(action,'1')
                        if copyState.capture == '1':
                            score = self.getGhostVal_Exp(copyState,depth)
                        else:
                            score = self.getPacVal_Exp(copyState,depth+1)['score']
                        actionScores.append(score)
                    return mean(actionScores)


    def getEdge_Exp(self):

        print("Running Expectimax")
        result = self.getPacVal_Exp(self.gameState,0)
        max_action = result["action"]
        print("Nodes Expanded: ", self.nodes)
        return {"max_action":max_action,"nodes":self.nodes}

    def getEdge_Exp_Calc(self,number_of_dots):

        print("Running Expectimax with Calculated Probabilities")
        self.probabs = self.getProbabs(number_of_dots)
        result = self.getPacVal_Exp_Calc(self.gameState,0)
        max_action = result["action"]
        print("Nodes Expanded: ", self.nodes)
        return {"max_action":max_action,"nodes":self.nodes}

    def getProbabs(self,number_of_dots):
        
        lines = []
        filname = 'stateAction'+str(number_of_dots)+str(number_of_dots)+'.txt'
        with open(filname) as f:
            lines = f.readlines()
        stateActionList = [ast.literal_eval(x) for x in lines]
        
        tempDict = {}
        for item,val in stateActionList:
            try: 
                tempList = tempDict[tuple(item)]
            except:
                tempList = []
            tempList.append(val)
            tempDict[tuple(item)] = tempList

        countDict = {}
        for item,val in tempDict.items():
            countDict[item] = len(val)

        finalDict = {}
        for item,val in tempDict.items():
            finalDict[item] = dict(Counter(val))

        probDict = {}
        for item,val in finalDict.items():
            probDictTemp = {}
            for action,actionCount in val.items():
                probDictTemp[action] = actionCount/countDict[item]
            probDict[item] =  probDictTemp
        
        return probDict

    def calProb(self,actionScores,state):
        state = sorted(state)
        probabs = self.probabs[tuple(state)]
        score = 0
        for key in actionScores.keys():
            try:
                score = score + (actionScores[key] * probabs[key])
            except:
                pass
        return score



    def getPacVal_Exp_Calc(self,gameState,depth):
                
        """Defining maximizer"""
        
        if (depth == self.depth) | (gameState.getWinner() != False):
            
            return {'score':gameState.evaluateState(),'action':""}
        else :   
            
            legalMoves = gameState.remainEdges
            random.shuffle(legalMoves)
            max_score = float("-inf")
            for action in legalMoves:
                self.nodes = self.nodes+1
                copyState = copy.deepcopy(gameState)
                copyState.generateSuccessor(action,'2')
                if copyState.capture == '2':
                    score = self.getPacVal_Exp_Calc(copyState,depth)['score']
                else:
                    score = self.getGhostVal_Exp_Calc(copyState,depth)
                if score>max_score:
                    max_score = score
                    max_action = action
            return {'score': max_score,'action':max_action}

    def getGhostVal_Exp_Calc(self,gameState,depth):
                
        """Defining minimizer"""
        
        if (depth == self.depth) | (gameState.getWinner() != False):
            
            return gameState.evaluateState()
        else:

            legalMoves = gameState.remainEdges
            random.shuffle(legalMoves)
            actionScores = {}
            for action in legalMoves:
                self.nodes = self.nodes+1
                copyState = copy.deepcopy(gameState)
                copyState.generateSuccessor(action,'1')
                if copyState.capture == '1':
                    score = self.getGhostVal_Exp_Calc(copyState,depth)
                else:
                    score = self.getPacVal_Exp_Calc(copyState,depth+1)['score']
                actionScores[action] = score
            try:
                #print("From Calculated probabs")
                #print("Marked Edges :",gameState.markedEdges)
                
                score = self.calProb(actionScores,gameState.markedEdges)
                #print("Score:",score)
            except:
                print("Equally likely probabs")
                #print("Marked Edges :",gameState.markedEdges)
                score = mean(list(actionScores.values()))
                #print("Score:",score)
            return score
