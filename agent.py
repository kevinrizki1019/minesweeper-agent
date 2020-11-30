from itertools import combinations
from clips import *

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