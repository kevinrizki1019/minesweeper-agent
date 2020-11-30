import sys
from clips import *
from cord import Cord
from board import Board
from agent import Agent

if __name__ == "__main__":    
    board = Board()
    agent = Agent()
    board.load_file(sys.argv[1])
    win = False
    gameover = False
    first_move = True

    while True:
        board.print_board_revealed()

        if first_move:
            board.open_cord(0, 0)
            first_move = False
            continue

        agent.prepare_facts_rules(board)
        next_move_x, next_move_y = agent.inference()
        print("Next move choosen by agent: open", next_move_x, next_move_y)

        command = 'o'
        # x, y = int(inp[1]), int(inp[2])
        x, y = next_move_x, next_move_y

        inp = input('Press enter to continue ')

        if command == 'o':
            win, gameover = board.open_cord(x, y)
        elif command == 'f':
            board.put_flag(x, y)

        if gameover:
            break

    if win:
        print('Congratulatios You win!')
    else:
        print('Game over')
        print('You lose!')
