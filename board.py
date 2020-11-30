from cord import Cord

class Board:
    # Board Representation
    # matrix contain value each cord, matrix_revealed for terminal view
    def __init__(self):
        self.matrix = None
        self.matrix_revealed = None
        self.cord_revealed_num = 0
        self.bomb_cord = []
        self.flag_cord = []
    
    # Read setup game from file filename
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
    
    # Build matrix value of each tile
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

    # print board to terminal
    def print_board_revealed(self):
        for i in range(len(self.matrix)-1):
            print(i, end=" ")
        print(len(self.matrix)-1)
        print()
        for i,row in enumerate (self.matrix_revealed):
            for x in row:
                print(x, end='|') 
            print("  ",i)
        print('----------------------------------')
        print()

    # return true if cord in board's range
    def is_cord_valid(self, x, y):
        return (-1 < x < self.size) and (-1 < y < self.size)

    # return true if value equal zero
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
            self.matrix_revealed[x][y] = "B"
            print('Game over')
            return False, True

        self.reveal_cord(x, y)
        if (self.cord_revealed_num == self.size**2-self.bomb_num):
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