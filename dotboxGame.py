#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 11:33:30 2022

@author: basilkvarghese
"""

from tkinter import *
import numpy as np
from dotBox import gameState
from dotboxAgent import gameAgent
import copy
from datetime import datetime
import ast
import pandas as pd
size_of_board = 600
number_of_dots = 4
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#7BC043'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'
Green_color = '#7BC043'
dot_width = 0.25*size_of_board/number_of_dots
edge_width = 0.1*size_of_board/number_of_dots
distance_between_dots = size_of_board / (number_of_dots)

depth_0 = 1
depth_1 = 1
depth_2 = 2
#algo = 'minimax'
algo = 'AB'
#algo = 'expt'
#algo = 'expcal'
def runGameAlgo(gameState):
    if algo == 'minimax':
        result = gameState.getEdge_minimax()
    elif algo == 'AB':
        result = gameState.getEdge_AB()
    elif algo == 'expt':
        result = gameState.getEdge_Exp()
    else:
        result = gameState.getEdge_Exp_Calc(number_of_dots)
    
    return result



class PlayGame(gameState):


    def __init__(self):
        print("New Game")
        self.grid1 = gameState(number_of_dots-1,number_of_dots-1)
        self.window = Tk()
        self.window.title('Dots_and_Boxes')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>',self.click)
        self.refresh_board()
        self.ply = '1'
        self.nextPly = '1'
        self.turntext_handle = []
        self.score_handle = []
        self.display_turn_text_first()
        self.display_scores()
        self.turnCount = 0
        self.time_avg = []
        self.nodes_avg = []
        self.stateAction = []


    def mainloop(self):
        self.window.mainloop()

    def refresh_board(self):
            for i in range(number_of_dots):
                x = i*distance_between_dots+distance_between_dots/2
                self.canvas.create_line(x, distance_between_dots/2, x,
                                        size_of_board-distance_between_dots/2,
                                        fill='gray', dash = (2, 2))
                self.canvas.create_line(distance_between_dots/2, x,
                                        size_of_board-distance_between_dots/2, x,
                                        fill='gray', dash=(2, 2))

            for i in range(number_of_dots):
                for j in range(number_of_dots):
                    start_x = i*distance_between_dots+distance_between_dots/2
                    end_x = j*distance_between_dots+distance_between_dots/2
                    self.canvas.create_oval(start_x-dot_width/2, end_x-dot_width/2, start_x+dot_width/2,
                                            end_x+dot_width/2, fill=dot_color,
                                            outline=dot_color)

    def markLine(self,grid_position):

        grid_position = np.array(grid_position)
        position = (grid_position-distance_between_dots/4)//(distance_between_dots/2)
        logical_position = []
        type = False
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0]-1)//2)
            c = int(position[1]//2)
            logical_position = [r, c]
            type = 'row'
            # self.row_status[c][r]=1
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'
        if type == 'row':
            start_x = distance_between_dots/2 + logical_position[0]*distance_between_dots
            end_x = start_x+distance_between_dots
            start_y = distance_between_dots/2 + logical_position[1]*distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x

        self.canvas.create_line(start_x, start_y, end_x, end_y, width=edge_width)
        return ((start_x, start_y, end_x, end_y),type)

    def markLineDots(self,edge):
        start_x = distance_between_dots / 2 + edge[0][0] * distance_between_dots
        start_y = distance_between_dots / 2 + edge[0][1] * distance_between_dots 
        end_x = distance_between_dots / 2 + edge[1][0] * distance_between_dots
        end_y = distance_between_dots / 2 + edge[1][1] * distance_between_dots
        self.canvas.create_line(start_x, start_y, end_x, end_y, width=edge_width)

    def getMarkedEdge(self,co_ords):

        start_x, start_y, end_x, end_y = co_ords
        point_1_x =  (start_x - (distance_between_dots/2)) / distance_between_dots
        point_1_y =  (start_y - (distance_between_dots/2)) / distance_between_dots
        point_1 = (int(point_1_x),int(point_1_y))

        point_2_x =  (end_x - (distance_between_dots/2)) / distance_between_dots
        point_2_y =  (end_y - (distance_between_dots/2)) / distance_between_dots
        point_2 = (int(point_2_x),int(point_2_y))
        marked_edge = (point_1,point_2)
        return marked_edge

    def display_turn_text_first(self):
        text = 'Current turn:Player1 '
        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/3.5,
                                                       font="cmr 15 bold",text=text)
    def display_turn_text(self):
        text = 'Current turn:'
        if self.ply == '1':
            text += "Player 1"
        else:
            text += "Player 2"
        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/3.5,
                                                       font="cmr 15 bold",text=text)

    def display_game_over(self):
        self.saveActions()
        self.canvas.delete("all")
        if (self.grid1.playerBoxes['1'] == self.grid1.playerBoxes['2']):
            text = "Its a Tie"
            self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 50 bold",text=text)
        else:
            text = "Game Over\nPlayer "+self.grid1.getWinner()+" is the winner"
            self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 50 bold",text=text)
        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 30 bold",text=score_text)

        score_text = 'Player 1 : ' + str(self.grid1.playerBoxes['1']) + '\n'
        score_text += 'Player 2 : ' + str(self.grid1.playerBoxes['2']) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold",text=score_text)

    def postGame(self):

        time_avg = np.mean(self.time_avg)
        node_avg = np.mean(self.nodes_avg)
        if self.grid1.playerBoxes['1'] == self.grid1.playerBoxes['2']:
            winFlag = -1
        elif self.grid1.getWinner() == '2':
            winFlag = 1
        else:
            winFlag = 0

        print('AVG reaction time: ',time_avg)
        print('AVG Nodes Expanded: ',node_avg)
        board_size = str(number_of_dots)+" X "+str(number_of_dots)

        try:
            report = pd.read_csv("GameReport.csv")
            new_report = pd.DataFrame({'Algorithm':algo,'Board_Size':board_size,'reaction_time':time_avg,'nodes':node_avg,'AgentWin':winFlag,'Depth':depth_2},index = [0])
            report = pd.concat([report,new_report])
        except:
            report = pd.DataFrame({'Algorithm':algo,'Board_Size':board_size,'reaction_time':time_avg,'nodes':node_avg,'AgentWin':winFlag,'Depth':depth_2},index = [0])
        report = report.drop_duplicates()
        report.to_csv("GameReport.csv",index = False)



    def decide_next_player(self):
        if self.ply == '1':
            self.nextPly = '2'
        else:
            self.nextPly = '1'

        if self.grid1.capture =='0':
            self.ply = self.nextPly
        else:
            self.ply = self.grid1.capture



    def display_scores(self):

        score_text = 'Player 1 : ' + str(self.grid1.playerBoxes['1']) + '\n'
        score_text += 'Player 2 : ' + str(self.grid1.playerBoxes['2'])

        self.canvas.delete(self.score_handle)
        self.score_handle = self.canvas.create_text(size_of_board - 5.7*len(score_text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold",text=score_text)     


    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[0][0] * distance_between_dots + edge_width/2
        start_y = distance_between_dots / 2 + box[0][1] * distance_between_dots + edge_width/2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')    


    def mark_boxes(self):
        
        player_1_boxCorners = self.grid1.playerBoxCorners['1'] 
        if (len(player_1_boxCorners)>0):
            for box in player_1_boxCorners:
                self.shade_box(box, player1_color)  
        player_2_boxCorners = self.grid1.playerBoxCorners['2'] 
        if (len(player_2_boxCorners)>0):
            for box in player_2_boxCorners:
                self.shade_box(box, player2_color)                            

    def agentPlay(self,depth_x):
        stateCopy = copy.deepcopy(self.grid1)
        agentState = gameAgent(stateCopy,depth_x)
        start_time = datetime.now()
        result = runGameAlgo(agentState)
        marked_edge = result['max_action']
        nodes = result['nodes']
        end_time = datetime.now()
        time_taken = end_time - start_time
        time_taken = time_taken.total_seconds()*1000
        self.time_avg.append(time_taken)
        self.nodes_avg.append(nodes)
        if depth_x == depth_0:
            print('Phase 0')
        if depth_x == depth_1:
            print('Phase 1')
        if depth_x == depth_2:
            print('Phase 2')
        print('Duration:',time_taken)
        return marked_edge
        

    def saveActions(self):
        lines = []
        filname = 'stateAction'+str(number_of_dots)+str(number_of_dots)+'.txt'
        try:
            with open(filname) as f:
                lines = f.readlines()
            stateActionList = [ast.literal_eval(x) for x in lines]
        except:
            stateActionList = []
        stateActionList.extend(self.stateAction)
        textfile = open(filname, "w")
        for element in stateActionList:
            textfile.write(str(element) + "\n")
        textfile.close()


    def click(self,event):
        if len(self.grid1.remainEdges) > 0:
            if self.ply == '1':
                grid_position = [event.x, event.y]
                co_ords,type = self.markLine(grid_position)
                marked_edge = self.getMarkedEdge(co_ords)
            else:
                half_count = int(((number_of_dots**2) - number_of_dots)*(7/5))
                quarter_count = int(half_count/2)
                if self.turnCount >= half_count:
                    marked_edge = self.agentPlay(depth_2)
                elif self.turnCount >= quarter_count:
                    marked_edge = self.agentPlay(depth_1)
                else:
                    marked_edge = self.agentPlay(depth_0)
                   
                type = True
                self.markLineDots(marked_edge)
            
            if type != False:
                markedEdges = self.grid1.markedEdges.copy()
                markedEdges = sorted(markedEdges)
                self.stateAction.append((markedEdges,marked_edge))
                self.grid1.generateSuccessor(marked_edge,self.ply)
                self.mark_boxes()
                self.refresh_board()
                self.decide_next_player()
                self.display_turn_text()
                self.display_scores()

        else:
            self.display_game_over()
            self.postGame()
        self.turnCount = self.turnCount+1


game_instance = PlayGame()
game_instance.mainloop()


