from random import randint, choice
import os
from time import sleep
import string

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
# the set of values used for the sudoku , could be letters or numbers , or anything else
# none of these should be repeated , like i said , it is a set .. allowed set lengths are 9,16,12,25,100[the mega sudoku]
VALUES = list(string.ascii_uppercase[0:9])
# this will represent the height and width of the small blocks within the sudoku
# eg a 9 by 9 sudoku has 3 by 3 bloacks in it ... 3 being the sqrt of 9___
grid_len = int((len(board)**0.5))
# this will be used for carrying out some optimization ie the program will not rely solely on 
# backtracking ... bruteforcing method to solve the board .. some other techniques like {single position, simgle candidate
# candidate line will be used too... the pset will hold a hashmap of all empty cells, each cell will have a list of all 
# possible occupants... 
pset = {}

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
num = 0

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
                        prefill()
                        board[row][col] = '*'
                return
    if num == 0:
        pset_init()
        gen_pset()
        num += 1
    solve_board()


# THE init_board fn marks with asterisks the cells that will be filled with givens
def init_board():
    global board, FILLED
    to_be_filled = make_empty()


    for cell in to_be_filled:
        row, col = cell[0], cell[1]
        board[row][col] = FILLED
    

def pset_init():
    global board
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
    global EMPTY, board, VALUES, empty_cells
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                for value in VALUES:
                    if is_valid(value, row, col):
                        empty_cells[row][col].append(value)
                # the single candidate
                if len(empty_cells[row][col]) == 1:
                    board[row][col] = empty_cells[row][col][0]
                    del empty_cells[row][col]
                elif len(empty_cells[row][col]) == 0:
                    # board is unsolvable
                    # probabaly too many prefilled cells
                    print('board is unsolvable')
    # the single position
    for row in empty_cells:
        value_map = {value:[0,[]] for value in VALUES}
        for cell in empty_cells[row]:
            for value in empty_cells[row][cell]:
                value_map[value][0] += 1
                value_map[value][1].append(cell)
        for value in value_map:
            if value_map[value][0] == 1: # got a single position
                board[row][value_map[value][1][0]] = value
                del empty_cells[row][value_map[value][1][0]]

    # naked pair logic goes here


    # hidden pair logic goes here

    # naked tripple logic goes here

    # hidden tripple logic goes here

# the backtracking logic.. the guess work happens here
# after all solving techniques have been tried ... and 
# psets for each cell reduced to min size
def solve_board():
    global board, empty_cells, EMPTY, tFILLED
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                for value in empty_cells[row][col]: 
                    if is_valid(value,row,col):
                        board[row][col] = value
                        solve_board()
                        board[row][col] = EMPTY
                return # all values incompatible , return to parent caller
    print('board is solved , no more empty slots')
    draw_board()
    input('more ?') # output more solutions if there is any

def main():
    init_board()
    prefill()



if __name__ == '__main__':
    main()
