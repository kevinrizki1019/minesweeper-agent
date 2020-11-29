import sys

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
            print(self.size, "wooooooooooooooooooooooooy")
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
    
    def put_flag(self, x, y):
        self.flag_cord.append(Cord(x, y))
        self.matrix_revealed[y][x] = 'F'
    
    def bomb_num_around(self, x, y):
        return self.matrix[y][x]
    
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
        
        if self.bomb_num_around(x, y) == 0:
            # Reveal adjacent cord
            around = [[-1, -1], [0, -1], [-1, 0], [1, 1], [0, 1], [1, 0], [1, -1], [-1, 1]]
            for cord in around:
                self.reveal_cord(x+cord[0], y+cord[1])


board = Board()
board.load_file('test.txt')
win = False

while True:
    board.print_board_revealed()
    board.print_board_all()
    cord = input('open coordinat (ex: 1 2): ').split(' ')
    win, gameover = board.open_cord(int(cord[0]), int(cord[1]))
    if gameover:
        break

if win:
    print('Congratulatios You win!')
else:
    print('Game over')
    print('You lose!')
