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
        agent.inference()
        
        inp = input('open coordinat (ex:o 1 2): ').split(' ')
        command = inp[0]
        x, y = int(inp[1]), int(inp[2])

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
