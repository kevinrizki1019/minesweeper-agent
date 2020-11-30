import sys
from clips import *
from cord import Cord
from board import Board
from agent import Agent
import time

if __name__ == "__main__":    
    board = Board()
    agent = Agent()
    board.load_file(sys.argv[1])
    win = False
    gameover = False
    first_move = True

    print()
    print("*********** Game Start ***********")
    i = 0
    while True:
        print()
        print("*********** Step", i,"***********")
        i += 1

        board.print_board_revealed()

        if first_move:
            board.open_cord(0, 0)
            first_move = False
            print("Next move choosen by agent: open 0 0 ")
            # inp = input('Press enter to continue ')
            time.sleep(1)
            continue

        agent.prepare_facts_rules(board)
        next_move_x, next_move_y = agent.inference(board)
        print("Next move choosen by agent: open", next_move_x, next_move_y)

        command = 'o'
        # x, y = int(inp[1]), int(inp[2])
        x, y = next_move_x, next_move_y

        # inp = input('Press enter to continue ')
        time.sleep(1)

        if command == 'o':
            win, gameover = board.open_cord(x, y)
        elif command == 'f':
            board.put_flag(x, y)

        if gameover:
            break


    board.print_board_revealed()
    if win:
        print('Congratulatios You win!')
    else:
        print('Game over')
        print('You lose!')
