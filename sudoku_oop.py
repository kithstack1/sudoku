from random import randint
from time import sleep
import string
from colorama import Fore 

GREEN, WHITE = Fore.GREEN, Fore.WHITE



# the set of values used for the sudoku , could be letters or numbers , or anything else
# none of these should be repeated , like i said , it is a set .. allowed set lengths are 9,16,12,25,100[the mega sudoku]
VALUES = list(string.ascii_uppercase[0:16])
# a var to mark the cells for solving
EMPTY = '#'
# the sudoku board , it will be a list of lists{length of each will be the length of the values set}
# each list representing a row , all lists of equal length 
# each list representing a row , all lists of equal length # and each index in list representing a cell ie intersection of a row and a column 
board = [[EMPTY for _ in range(len(VALUES))] for _ in range(len(VALUES))]
# what percentage of the board is has givens 
PFILLED = 20
PFILLED = int((len(board)**2)*(PFILLED/100))
empty_cells = {}
# the FILLED var will be used by the givens generator code to know which
# cells to fill and which cells not to fill
FILLED = '*'
# this will represent the height and width of the small blocks within the sudoku
# eg a 9 by 9 sudoku has 3 by 3 bloacks in it ... 3 being the sqrt of 9___
grid_len = int((len(board)**0.5))
# this will be used for carrying out some optimization ie the program will not rely solely on 
# backtracking ... bruteforcing method to solve the board .. some other techniques like {single position, simgle candidate
# candidate line will be used too... the pset will hold a hashmap of all empty cells, each cell will have a list of all 
# possible occupants... 
pset = {}

# trying to splve number of spaces hit by logic and not bruteforce
logic = 0
# draw board to screen
def draw_board():
    global grid_len, board
    
    for i in range(len(board)):
        row_data = []
        for j in range(len(board)):
            if (not j%grid_len) and (j != len(board)-1) and j != 0:
                cell_data = f'| {board[i][j]}'
            else:
                cell_data = f'  {board[i][j]}'
            row_data.append(cell_data)    
            print(cell_data,end='') 
        print('',end='\n')
        if (not (i+1)%grid_len) and i!= 0 and i != len(board)-1:
            print('-'*len(''.join(row_data)))
    print()

# the validity checker logic goes here
def is_valid(value,row,col):
    global board, grid_len
    # vertical check
    for i in range(len(board)):
        if board[i][col] == value:
            return False
    # horizontal check
    for j in range(len(board)):
        if board[row][j] == value:
            return False
    # block check
    x0 = col//grid_len * grid_len
    y0 = row//grid_len * grid_len

    for row in range(y0,y0+grid_len):
        for col in range(x0,x0+grid_len):
            if board[row][col] == value:
                return False
    return True


# generates cells that will be filled with givens based 
# on percentage of board to be filled specified at start of script
def make_empty():
    global board, PFILLED
    i = 0
    p_filled_set = []
    while i < PFILLED:
        row, col = randint(0,len(board)-1), randint(0,len(board)-1)
        cell = (row,col)
        if cell in p_filled_set:
            continue
        p_filled_set.append(cell)
        i += 1
    return p_filled_set
# this var is to ensure generation of a pset only once
num = 0

# add some green formatting to the board solution inputs
def pprint(value):
    return f'{GREEN}{value}{WHITE}'


# the givens generator code.. since this program will be for now
# solving sudokus it generates on its own.. the code will as well
# call the solver function immediately after making a board..
# the reason being the function creating the board is recursive and if left 
# to reach final return will have to create all possible sudokus befor actually completing
# will have to solve this with python generators some time from now
def prefill():
    global num, VALUES, board
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == '*':
                for value in VALUES:
                    if is_valid(value, row, col):
                        board[row][col] = value
                        yield from prefill()
                        board[row][col] = '*'
                return
    pset_init()
    gen_pset()
    print('GENERATED BOARD')
    yield(draw_board())


# the init_board fn marks with asterisks the cells that will be filled with givens
def init_board():
    global board, FILLED
    to_be_filled = make_empty()


    for cell in to_be_filled:
        row, col = cell[0], cell[1]
        board[row][col] = FILLED
    
# prepare candidate set hashmap for each empty cell
def pset_init():
    global board, EMPTY
    for row in range(len(board)):
        empty_cells[row] = {}
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                empty_cells[row][col] = []



# need to find  a way to code in the naked pair logic
# ie if 2 cells in the same row and grid have the same pset then
# all the cells in that grid cant have the elemnts in that pset
# same applies to the entire row and also find restricted cells
def gen_pset():
    # generate all possible values for each cell ahead of time
    global EMPTY, logic, grid_len,  board, VALUES, empty_cells
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                for value in VALUES:
                    if is_valid(value, row, col):
                        empty_cells[row][col].append(value)
                # the single candidate
                if len(empty_cells[row][col]) == 1:
                    # got a singleton
                    print('GOT A SINGLETON')
                    # force the value into the board
                    board[row][col] = empty_cells[row][col][0]
                    logic += 1
                    # delete the cell from empty_cells
                    del empty_cells[row][col]
                    # clear any occerence of the value in p_candidates in the cell's block , row and column
                    update_pset(row, col, value)
                elif len(empty_cells[row][col]) == 0:
                    # board is unsolvable
                    # probabaly too many prefilled cells
                    print('board is unsolvable')
    single_position()
# naked pair logic goes here
def naked_pair():
    pass

# hidden pair logic goes here
def hidden_pair():
    pass
    
# naked tripple logic goes here
def naked_tripple():
    pass

# hidden tripple logic goes here
def hidden_tripple():
    pass

# locked candidate logic goes  here
# only candidate in the block in one row or column
def locked_candidate_1():
    global board, empty_cells, VALUES
    blocks = get_blocks()
    for block in blocks:
        row, col = block[0], block[1]

# the locked candidate type 2 ( only candidate in the row or column in one block)
def locked_candidate_2():
    global board, empty_cells, VALUES
    pass

# the x wing logic goes here
def x_wing():
    global board, empty_cells, VALUES
    pass

# the single position optimisation
def single_position():
    global empty_cells, logic,  VALUES, board
    # the single position
    # row check
    for row in empty_cells:
        value_map = {value:[0,[]] for value in VALUES}
        for cell in empty_cells[row]:
            for value in empty_cells[row][cell]:
                value_map[value][0] += 1
                value_map[value][1].append(cell)
        for value in value_map:
            if value_map[value][0] == 1: 
                board[row][value_map[value][1][0]] = value
                logic += 1
                # delete the cell from empty_cells hash map
                cell = value_map[value][1][0]
                del empty_cells[row][cell]
                # delete any occurence of the value in the p_candidates in the block its in
                # the row its in and the column          
                update_pset(row,cell,value)
    # check column
    for col in range(len(VALUES)):
        value_map = {value:[0,[]] for value in VALUES}
        for row in empty_cells:
            if col in empty_cells[row]:
                for value in empty_cells[row][col]:
                    value_map[value][0] += 1
                    value_map[value][1].append(row)
        for value in value_map:
            if value_map[value][0] == 1:
               row = value_map[value][1][0]
               board[row][col] = value
               logic += 1
               del empty_cells[row][col]
               update_pset(row,col,value)
    # block check
    blocks = get_blocks()
    for block in blocks:
        value_map = {value:[0,[]] for value in VALUES}
        row, col = block[0], block[1]
        for r in range(row, row+grid_len):
            if r in empty_cells:
                for c in range(col, col+grid_len):
                    if c in empty_cells[r]:
                        for value in empty_cells[r][c]:
                            value_map[value][0] += 1
                            value_map[value][1].append((r,c))
        for value in value_map:
            if value_map[value][0] == 1: 
                cell_cord = value_map[value][1][0]
                r,c = cell_cord[0], cell_cord[1]
                board[r][c] = value
                logic += 1
                # delete the cell from empty_cells hash map
                try:
                   del empty_cells[row][cell]
                except Exception as e:
                    print('error',e,empty_cells[row],cell)
                # delete any occurence of the value in the p_candidates in the block its in
                # the row its in and the column          
                update_pset(row,cell,value)



# get index of top left cell for each block
def get_blocks():
    global board, grid_len
    board_length = len(board)
    row_indices = [i for i in range(0,board_length) if not i%grid_len]
    col_indices = row_indices.copy()
    blocks = []
    for i in row_indices:
        for j in col_indices:
            blocks.append((i,j))
    return blocks



def update_pset(row, col, value):
    global BOARD, empty_cells, grid_len
    # clear value from p_candidates in  row
    for cell in empty_cells[row]:
        try:
            empty_cells[row][cell].remove(value)
        except Exception as e:
            pass

    # clear value from p_candidates in  column
    for r in empty_cells:
        try:
            empty_cells[r][col].remove(value)
        # just in case the r, c intersection isn't empty in any row for this empty cell
        except Exception as e:
            continue

    # clear value from p_candidates in  block
    x0 = (col // grid_len) * grid_len
    y0 = (row // grid_len) * grid_len
    for r in range(y0+grid_len):
        for c in range(x0,x0+grid_len):
            try:
                empty_cells[r][c].remove(value)
            except Exception as e:
                pass


# the backtracking logic.. the guess work happens here
# after all solving techniques have been tried ... and 
# p_candidates for each cell reduced to min size
def solve_board():
    global board, empty_cells, EMPTY , logic
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                for value in empty_cells[row][col]: 
                    if is_valid(value,row,col):
                        board[row][col] = value
                        yield from solve_board()
                        board[row][col] = EMPTY
                return # all values incompatible , return to parent caller
    print('board is solved , no more empty slots')
    print(f'{logic} number of cells was filled using logic')
    yield(draw_board())

def main():
    init_board()
    gen = prefill()
    next(gen)
    soln = solve_board()
    next(soln)



if __name__ == '__main__':
    main()



class Sudoku:

    """ simple CLI sudoku solver and bad sudoku generator """

    def __init__(self, pfilled, values):
        self.EMPTY = '*'
        self.FILLED = '#'
        self.values = values
        self.width = len(values)
        self.block_width = int(self.width**0.5)
        self.empty_cells = {}
        self.board = [[self.EMPTY for _ in range(len(self.values))] for _ in range(len(self.values))]


    def draw_board(self):
        pass

    def is_valid(self):
        pass

    def make_empty(self):
        pass

    def main(self):
        pass

    def solve_board(self):
        pass

    def init_board(self):
        pass

    def make_pset(self):
        pass

    def get_blocks(self):
        pass
