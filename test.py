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
moves_made = []
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
        game_result = playgame(game, ai, iteration)
        if game_result == "won":
            won += 1
        elif game_result == "lost":
            lost += 1
            #print(f"iteration: {iteration}")
            #print(f"moves: {moves_made}")
            #print(f"mines: {str(game.mines)}")
            #return
        elif game_result == "lost in start":
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
    moves_made = []
    movesn = 0
    while True:
        movesn += 1
        # print("knowledge:")
        # for sentence in ai.knowledge:
        #     print(f"\t{sentence.cells}: {sentence.count}")
    
        move = ai.make_safe_move()
        if move is None:
            move = ai.make_random_move()
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
        moves_made.append(move)
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
                    if movesn <= exclude:
                        return "lost in start"
                    #print(f"iteration: {iteration}")
                    #print(f"moves: {moves_made}")
                    #print(f"mines: {str(game.mines)}")
                    return "lost"
loop()