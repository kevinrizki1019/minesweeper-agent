import sys
from clips import *
from itertools import combinations

class Cord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Board:

    def __init__(self):
        self.matrix = None
        self.matrix_revealed = None
        self.cord_revealed_num = 0
        self.bomb_cord = []
        self.flag_cord = []
    
    def load_file(self, filename):
        with open(filename) as f:
            self.size, self.bomb_num, *raw_bomb_cord = f.read().split('\n')
            self.size = int(self.size)
            self.bomb_num = int(self.bomb_num)
            for raw_cord in raw_bomb_cord:
                cord_list = raw_cord.split(',')
                x, y = cord_list[0], cord_list[1]
                self.bomb_cord.append(Cord(int(x), int(y)))
            f.close()
        
        self.build_matrix()
    
    def build_matrix(self):
        # setup
        self.matrix = [[0 for i in range(self.size)] for i in range(self.size)]
        self.matrix_revealed = [[' ' for i in range(self.size)] for i in range(self.size)]

        # Put bomb
        for cord in self.bomb_cord:
            self.matrix[cord.y][cord.x] = 'b'
        
        # Put number around the bombs
        for i in range(self.size):
            for j in range(self.size):

                if self.matrix[i][j] == 'b':
                    continue

                around = [[-1, -1], [0, -1], [-1, 0], [1, 1], [0, 1], [1, 0], [1, -1], [-1, 1]]
                bomb_num = 0
                for cord in around:
                    if self.is_cord_valid(i+cord[0], j+cord[1]):
                        if (self.matrix[i+cord[0]][j+cord[1]] == 'b'):
                            bomb_num += 1
                self.matrix[i][j] = bomb_num

    def is_cord_valid(self, x, y):
        return (-1 < x < self.size) and (-1 < y < self.size)

    def print_board_all(self):
        for row in self.matrix:
            for x in row:
                print(x, end='|') 
            print()
        print('----------------------------------')
    
    def print_board_revealed(self):
        for row in self.matrix_revealed:
            for x in row:
                print(x, end='|') 
            print()
        print('----------------------------------')

    def is_bomb(self, x, y):
        return self.matrix[y][x] == 'b'
    
    def is_safe(self, x, y):
        return self.matrix[y][x] == 0
    
    def is_flag(self, x, y):
        return self.matrix_revealed[y][x] == 'F'
    
    def put_flag(self, x, y):
        if not self.is_revealed(x, y):
            self.flag_cord.append(Cord(x, y))
            self.matrix_revealed[y][x] = 'F'

    def is_revealed(self, x, y):
        return self.matrix_revealed[y][x] != ' ' and self.matrix_revealed[y][x] != 'F' 

    def bomb_num_around(self, x, y):
        return self.matrix[y][x]
    
    def flag_num_around(self, x, y):
        num = 0
        around = [[-1, -1], [0, -1], [-1, 0], [1, 1], [0, 1], [1, 0], [1, -1], [-1, 1]]
        for cord in around:
            if self.is_cord_valid(x+cord[0], y+cord[1]):
                if (self.is_revealed(x+cord[0], y+cord[1]) and self.is_flag(x+cord[0], y+cord[1])):
                    num += 1
        return num
    
    def get_revealed_value(self, x, y):
        return self.matrix_revealed[y][x]
    
    def open_cord(self, x, y):
        if (self.is_bomb(x, y)):
            print('Game over')
            return False, True

        self.reveal_cord(x, y)
        if (self.cord_revealed_num == self.size^2-self.bomb_num):
            return True, True

        return False, False  

    def reveal_cord(self, x, y):
        if not self.is_cord_valid(x, y) or self.matrix_revealed[y][x] != ' ':
            return
        
        # Reveal cord
        self.matrix_revealed[y][x] = self.matrix[y][x]
        self.cord_revealed_num += 1
        
        if self.is_safe(x, y):
            # Reveal adjacent cord
            around = [[-1, -1], [0, -1], [-1, 0], [1, 1], [0, 1], [1, 0], [1, -1], [-1, 1]]
            for cord in around:
                self.reveal_cord(x+cord[0], y+cord[1])

class Agent:

    def __init__(self):
        # Create environment
        self.env = Environment()

        # Other
        self.rule_num = 0
        self.asserted_rules = []

    def assert_is_bomb(self, x, y):
        rule = f"(is-bomb {x} {y})"
        if rule not in self.asserted_rules:
            self.env.assert_string(rule)
            self.asserted_rules.append(rule)
    
    def assert_not_bomb(self, x, y):
        rule = f"(not-bomb {x} {y})"
        if rule not in self.asserted_rules:
            self.env.assert_string(rule)
            self.asserted_rules.append(rule)
    
    def assert_rule(self, rule):
        self.env.build(rule)

    def inference(self):
        self.env.run()
        for fact in self.env.facts():
            print(fact)
        self.reset()
    
    def reset(self):
        self.env.clear()
        self.env = Environment()
        self.rule_num = 0
        self.asserted_rules = []
    
    def is_edge_revealed(self, x, y, board):
        around = [[-1, -1], [0, -1], [-1, 0], [1, 1], [0, 1], [1, 0], [1, -1], [-1, 1]]

        if not board.is_revealed(x, y):
            return False

        for cord in around:
            if board.is_cord_valid(x+cord[0], y+cord[1]):
                if not board.is_revealed(x+cord[0], y+cord[1]):
                    return True
        return False
    
    def prepare_facts_rules(self, board):
        edge_blocks = []
        for y in range(board.size):
            for x in range(board.size):
                if self.is_edge_revealed(x, y, board):
                    edge_blocks.append((x, y))
        
        around = [[-1, -1], [0, -1], [-1, 0], [1, 1], [0, 1], [1, 0], [1, -1], [-1, 1]]
        for x, y in edge_blocks:
            # Get unrevealed blocks around
            unrevealeds = []
            value = board.get_revealed_value(x, y)
            flag_num_around = board.flag_num_around(x, y)
            for cord in around:
                if board.is_cord_valid(x+cord[0], y+cord[1]):
                    if not board.is_revealed(x+cord[0], y+cord[1]):
                        unrevealeds.append((x+cord[0], y+cord[1]))

            # Generate initial facts and rules
            if len(unrevealeds) == (value-flag_num_around):
                for unrevealed in unrevealeds:
                    self.assert_is_bomb(unrevealed[0], unrevealed[1])
            else:
                comb = combinations(unrevealeds, value-flag_num_around)
                for i in list(comb): 
                    bombs = list(i)  
                    not_bombs = list((set(unrevealeds)-set(i))) 

                    # Assert new rule
                    lhs = ""
                    for bomb in bombs:
                        lhs += f"(is-bomb {bomb[0]} {bomb[1]})\n"

                    rhs = "" 
                    for bomb in not_bombs:
                        rhs += f"(assert (not-bomb {bomb[0]} {bomb[1]}))\n"
                    
                    rule = f"""
                    (defrule R{self.rule_num}
                        {lhs}
                    =>
                        {rhs}
                    )
                    """
                    self.assert_rule(rule)
                    self.rule_num += 1


board = Board()
agent = Agent()
board.load_file('test.txt')
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
