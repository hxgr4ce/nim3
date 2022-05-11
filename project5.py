#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 5
Hadley Lim
2 May 2022
I have neither given nor received unauthorized aid on this program.	
"""
import random

num0 = int(input("Number in pile 0? "))
num1 = int(input("Number in pile 1? "))
num2 = int(input("Number in pile 2? "))
nn = int(input("Number of games to simulate? "))

print("\nInitial board is", str(num0)+"-"+str(num1)+"-"+str(num2)+", simulating "+str(nn)+" games.")

qtable = {}

board = {0:num0, 1:num1, 2:num2}

def possibleNextMoves(state):
    possible = []
    for pile in state:
        if state[pile] != 0:
            for remove in range (1, state[pile] + 1):
                action = str(pile)+str(remove)
                possible.append(action)
    return possible

def nextState(action, state):
    
    newState = {}
    for pile in state:
        newState[pile] = state[pile]
    
    pile = int(action[:1])
    numRemoved = int(action[-1])
    newState[pile] -= numRemoved
    
    return newState

def printQ():
    for state in qtable:
        for action in qtable[state]:
            print("Q["+state+", "+action+"] = " + str(qtable[state][action]))

"""
generate all Q[s,a] values
"""
def makeQTable(player, state):
    if not (state[0] <= 0 and state[1] <= 0 and state[2]<=0):
        
        stateStr = player+str(state[0])+str(state[1])+str(state[2])
        qtable[stateStr] = {}
        
        possible = possibleNextMoves(state)
                
        for action in possible:
            #initialize all Q[s,a] to 0
            qtable[stateStr][action] = 0 
                        
            nextBoard = nextState(action, state)
            
            if player == "A": nextPlayer = "B"
            else: nextPlayer = "A"
            
            #simulate next turn recursively
            makeQTable(nextPlayer, nextBoard) 

makeQTable("A", board)

"""
Q-learning phase
"""
for game in range (0, nn):
    #reset game state
    currentPlayer = "A"
    board = {0:num0, 1:num1, 2:num2}
    while not (board[0] <= 0 and board[1] <= 0 and board[2]<=0):
        possiblePiles = []
        for pile in board:
            #only want to pick from non-zero piles
            if board[pile] != 0: possiblePiles.append(pile)
            
        #randomly choosing what pile to pick from and how much to remove
        pile = random.choice(possiblePiles)
        numRemove = random.randrange(1, board[pile] + 1)
        
        #calculate update value: alpha = 1, gamma = 0.9
        stateStr = currentPlayer+str(board[0])+str(board[1])+str(board[2])
        action = str(pile) + str(numRemove)
    
        prevQ = qtable[stateStr][action]
        nextS = nextState(action, board)
        nextA = possibleNextMoves(nextS) #all next possible actions
        
        if currentPlayer == "A":
            nextStateStr = "B"+str(nextS[0])+str(nextS[1])+str(nextS[2])
            
            #finding minimum Q[s',a']
            minVal = 9999999999999
            for move in nextA:
                qvalue = qtable[nextStateStr][move]
                if qvalue <= minVal:
                    minVal = qvalue
            
            reward = 0
            #if B wins, reward is -1000
            if nextStateStr == "B000": 
                reward = -1000
                minVal = 0
            
            qtable[stateStr][action] = prevQ + reward + 0.9*minVal - prevQ
        else:
            nextStateStr = "A"+str(nextS[0])+str(nextS[1])+str(nextS[2])
            
            #finding maximum Q[s',a']
            maxVal = -9999999999999
            for move in nextA:
                qvalue = qtable[nextStateStr][move]
                if qvalue >= maxVal:
                    maxVal = qvalue
            
            reward = 0
            #if A wins, reward is 1000
            if nextStateStr == "A000": 
                reward = 1000
                maxVal = 0
            qtable[stateStr][action] = prevQ + reward + 0.9*maxVal - prevQ
        
        board[pile] -= numRemove
        
        #next player's turn to go
        if currentPlayer == "A": currentPlayer = "B"
        else: currentPlayer = "A"

print("\nFinal Q-values:")
printQ()

"""
Play!
"""
play = 1

while play == 1:
    board = {0:num0, 1:num1, 2:num2}
    
    firstPlayer = int(input("Who moves first, (1) User or (2) Computer? "))
    
    if firstPlayer == 1: currPlayer = 1
    else: currPlayer = 2
    
    while not (board[0] <= 0 and board[1] <= 0 and board[2]<=0):
        boardStr = "("+str(board[0])+", "+str(board[1])+", "+str(board[2])+")"
        #user's turn
        if currPlayer == 1:
            print("\nPlayer", end = " ")
            if currPlayer == firstPlayer: print("A", end = " ")
            else: print("B", end = " ")
            print("(user)'s turn, board is:", boardStr)

            pile = int(input("What pile? "))
            numRemove = int(input("How many? "))
            
            #do move if valid
            if board[pile] >= numRemove: board[pile] -= numRemove
            else: raise NameError("Invalid Move")
            
        #computer's turn
        else:
            print("\nPlayer", end = " ")
            
            if currPlayer == firstPlayer: player = "A"
            else: player = "B"
            print(player, "(computer)'s turn, board is:", boardStr)
        
            stateStr = player+str(board[0])+str(board[1])+str(board[2])
            
            bestAction = ""
            bestActionVal = 0
            
            if player == "A": bestActionVal = -9999999999999
            else: bestActionVal = 9999999999999
            
            #search q table for the best next move
            for possibleAction in qtable[stateStr]:
                if player == "A":
                    if qtable[stateStr][possibleAction] > bestActionVal:
                        bestActionVal = qtable[stateStr][possibleAction]
                        bestAction = possibleAction
                else:
                    if qtable[stateStr][possibleAction] < bestActionVal:
                        bestActionVal = qtable[stateStr][possibleAction]
                        bestAction = possibleAction
            
            pile = int(bestAction[:1])
            numRemove = int(bestAction[-1])
            
            print("Computer chooses pile", pile, "and removes", numRemove)
            board[pile] -= numRemove
        
        #switch currPlayer
        if currPlayer == 1: currPlayer = 2
        else: currPlayer = 1
    
    #game over message
    print("\nGame over.\nWinner is", end = " ")
    if currPlayer == firstPlayer: print("A", end = " ")
    else: print("B", end = " ")
    if currPlayer == 1: print("(user).")
    else: print("(computer).")
    
    play = int(input("Play again? (1) Yes (2) No: "))