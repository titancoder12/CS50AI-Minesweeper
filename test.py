import minesweeper
import random
from cprint import *

HEIGHT = 8
WIDTH = 8 
MINES = 8

cap = int(input("Enter number of iterations: ")) -1
exclude = int(input("Enter the number of moves in the beginning to exclude from the count of losses (enter 0 if you don't want to exclude any): "))

won = 0
lost = 0
iteration = 0
excludelost = 0
def loop():
    won = 0
    lost = 0
    iteration = 0
    excludelost = 0
    stuck = False
    while iteration <= cap:
        #input()
        iteration += 1
        random.seed(iteration)
        
        game = minesweeper.Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
        ai = minesweeper.MinesweeperAI(height=HEIGHT, width=WIDTH)
        
        print(f"iteration: {iteration}")
        print(f"Mines: {game.mines}")
        game = playgame(game, ai, iteration)
        if game == "won":
            won += 1
        elif game == "lost":
            lost += 1
            # Comment if you don't want to stop when losing
            #return
        elif game == "lost in start":
            excludelost +=1
        else:
            return None
    title = "---------------------------------------------- RESULTS ----------------------------------------------"
    won_str = f"won: {str(won)}"
    lost_1 = f"lost (excluding losses within first {exclude} moves): {str(lost)}"
    lost_2 = f"losses in beginning (within {exclude} moves): {str(excludelost)}"
    cprint.ok(title)
    cprint.info(won_str)
    cprint.fatal(lost_1)
    cprint.warn(lost_2)
    return
def playgame(game, ai, iteration):
    movesn = 0
    moves_made = []
    while True:
        movesn += 1
        # print("knowledge:")
        # for sentence in ai.knowledge:
        #     print(f"\t{sentence.cells}: {sentence.count}")
    
        move = ai.make_safe_move()
        if move != None:
            moves_made.append(move)
        if move is None:
            move = ai.make_random_move()
            moves_made.append(move)
            if move is None:
                if game.mines == ai.mines:
                    print("WON!!!!")
                    #won +=1
                    return "won"
                else:
                    print("stuck...")
                    #stuck = True
                    return "stuck"
            else:
                print(f"No known safe moves, AI making random move: {move}")
        else:
            print(f"AI making safe move: {move}")
        #time.sleep(0.2)
    
    
        # Make move and update AI knowledge
        if move:
            cprint.warn("iteration:")
            cprint.warn(iteration)
            for mine in game.mines:
                if move == mine:
                    print("LOST!!!!")
                    #lost+=1
                    #return
                    print(moves_made)
                    print(game.mines)
                    #print(game.knowledge)
                    if movesn <= exclude:
                        return "lost in start"
                    return "lost"
                #else:
            nearby = game.nearby_mines(move)
            ai.add_knowledge(move, nearby)
loop()