import math
import time

class minimax:
    def __init__(self):
        self.startTime = 0
        self.moveTime = 0
        self.pvMoves = []

    def iterativeDeepening(self, gs, moveTime):
        self.pvMoves = [None for _ in range(100)]
        self.depthDone = [None for _ in range(100)]

        self.moveTime = moveTime
        self.startTime = time.time()
        self.maxDepth = 1
        bestMove = 0

        while(self.depthDone[99] is None):
            score = self.nagamax(gs, self.maxDepth, -math.inf, math.inf, 1)
            if score is not None:
                bestMove = self.pvMoves[0]
                self.depthDone[self.maxDepth - 1] = 1
                self.maxDepth += 1
            else:
                break


        print("Compelted search of depth {} ".format(self.maxDepth), end='')
        return bestMove


    def nagamax(self, gs, depth, alpha, beta, player):
        if (gs.isTerminal() or depth == 0):
            return -gs.getRewards(player)


        validMoves = gs.getValidMoves(player)
        self.sortPVMoves(validMoves, self.maxDepth - depth)

        maxEval = -math.inf
        for targetSquare in validMoves:

            originSquare = gs.performMove(targetSquare)
            score = self.nagamax(gs, depth-1, -beta, -alpha, 1-player)
            gs.unPerformMove(originSquare)

            if time.time() - self.startTime > self.moveTime:
                return None

            if score > maxEval:
                maxEval = score
                self.storePVMove(targetSquare, self.maxDepth - depth)

            alpha = max(alpha, score)
            if beta <= alpha:
                break
        
        return -maxEval

    def sortPVMoves(self, validMoves, curDepth):
        if self.depthDone[curDepth] is not None:
            if self.pvMoves[curDepth] in validMoves:
                pvIndex = validMoves.index(self.pvMoves[curDepth])
                pvMove = validMoves.pop(pvIndex)
                validMoves.insert(0, pvMove)

    def storePVMove(self, pvMove, curDepth):
        self.pvMoves[curDepth] = pvMove
