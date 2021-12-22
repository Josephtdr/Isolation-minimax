import random
from minimax import *

class IsolaGamestate:
    xLength = 7
    yLength = 7
    unblockedPosition = '▢' 
    blockedPosition = '■'

    players = ['x','y']
    playerCoords = [0,0]
    player = 0

    def __init__(self):
        self.board = [self.unblockedPosition for _ in range(self.xLength*self.yLength)]
        
        while(self.playerCoords[0] == self.playerCoords[1]):
            self.playerCoords[0] = random.randint(0, self.xLength*self.yLength - 1)
            self.playerCoords[1] = random.randint(0, self.xLength*self.yLength - 1)
        
        for i in range(2):
            self.board[self.playerCoords[i]] = self.players[i]

        self.minimax = minimax()
        self.numSquaresToEdge = self.buildMoveData()
        self.possibleInputs = self.buildPossiblePlayerInputs()

    def performMove(self, move):
        previousSquare = self.playerCoords[self.player]

        self.board[self.playerCoords[self.player]] =  self.blockedPosition
        self.playerCoords[self.player] = move
        self.board[self.playerCoords[self.player]] =  self.players[self.player]
        self.player = 1-self.player

        return previousSquare

    def unPerformMove(self, move):
        self.player = 1-self.player
        self.board[self.playerCoords[self.player]] =  self.unblockedPosition
        self.playerCoords[self.player] = move
        self.board[self.playerCoords[self.player]] =  self.players[self.player]
        
    def getMove(self):
        if self.player==0:
            return self.humanMove()
        else:
            move = self.aiMove()
            print("AI played " + self.possibleInputs[move])
            return move

    def humanMove(self):
        legalMoves = self.getValidMoves(0)
        move = input("> ")
        while(True):
            if move not in self.possibleInputs:
                move = input("Impossible Input > ")
            else:
                targetSquare = self.possibleInputs.index(move)
                if targetSquare > len(self.board):
                        targetSquare -= len(self.board)
                if targetSquare not in legalMoves:
                    move = input("Illegal Move > ")
                else:
                    break
        return targetSquare

    def aiMove(self):
        startTime = time.time()
        targetSquare = self.minimax.iterativeDeepening(self, 4)


        print("in {:.2} seconds.".format((time.time() - startTime)))
        return targetSquare

    def getValidMoves(self, player):
        directionOffsets = [7, -7, 1, -1, 8, -8, 6, -6]
        validMoves = []

        originSquare = self.playerCoords[player]
        for directionIndex in range(8):
            for n in range(self.numSquaresToEdge[originSquare][directionIndex]):

                targetSquare = originSquare + directionOffsets[directionIndex] * (n+1)
                if self.board[targetSquare]!=self.unblockedPosition:
                    break

                validMoves.append(targetSquare)

        return validMoves 
        
    def isTerminal(self):
        return self.isWin(0) or self.isWin(1)

    def isDraw(self):
        return self.isWin(0) and self.isWin(1)

    def isWin(self, player):
        return len(self.getValidMoves(1-player))==0

    def getRewards(self, player):
        if self.isDraw():
            return 0
        elif self.isWin(player):
            return math.inf
        elif self.isWin(1-player):
            return -math.inf
        
        numCurPlayer = len(self.getValidMoves(player))
        numPreviousPlayer = len(self.getValidMoves(1-player))

        return numCurPlayer - pow(numPreviousPlayer, 3)

    def buildPossiblePlayerInputs(self):
        possibleInputs = [[] for _ in range(len(self.board)*2)]

        ranks = [i+1 for i in range(self.xLength)]
        letters = ['a','b','c','d','e','f','g']

        for row in range(self.xLength):
            for col in range(self.yLength):
                boardpos = row * 7 + col
                possibleInputs[boardpos] = letters[col]+str(ranks[row])
                boardpos += len(self.board)
                possibleInputs[boardpos] = str(ranks[row])+letters[col]

        return possibleInputs
        
    def buildMoveData(self):
        numSquaresToEdge = [[] for _ in self.board]

        for row in range(self.xLength):
            for col in range(self.yLength):

                numSouth = 6 - row
                numNorth = row
                numWest = col
                numEast = 6 - col

                boardpos = row * 7 + col

                numSquaresToEdge[boardpos] = [
                    numSouth,
                    numNorth,
                    numEast,
                    numWest,
                    min(numSouth, numEast),
                    min(numNorth, numWest),
                    min(numSouth, numWest),
                    min(numNorth, numEast)
                ]
        return numSquaresToEdge
    
    def printBoard(self):
        ranks = [i+1 for i in range(self.xLength)]
        
        for row in range(self.xLength):
            print()
            print("{}:".format(ranks[row]), end='')
            for col in range(self.yLength):
                pos = row * 7 + col
                print("| {} ".format(self.board[pos]), end='')
            print("|", end='')
        print()
        print("    a   b   c   d   e   f   g")

