import os
from gamestate import IsolaGamestate

def playGame():
    gs.printBoard();
    while(True):
        #cls()
        gs.printBoard();
        move = gs.getMove()
        gs.performMove(move)
        if gs.isTerminal():
            break

    gs.printBoard();
    if gs.isDraw():
        print("\ndraw")
    else:
        print("\nplr " + ("x" if gs.isWin(0) else "y") + " win")


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == "__main__": 
    gs = IsolaGamestate()
    playGame()