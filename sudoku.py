# new branch
from random import randint, choice
import os
from time import sleep
import string
#create empty board
EMPTY = '#'
# what percentage of the board is filled
PFILLED = 20
empty_cells = {}
FILLED = '*'
# VALUES = list(range(1,10))
VALUES = list(string.ascii_uppercase[0:9])
board = [[EMPTY for _ in range(len(VALUES))] for _ in range(len(VALUES))]
grid_len = int((len(board)**0.5))
pset = {}
PFILLED = int((len(board)**2)*(PFILLED/100))

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


def check_criteria(value,row,col):
    global board, grid_len
    # vertical check
    for i in range(len(board)):
        if board[i][col] == value:
            return False
    # horizontal check
    for j in range(len(board)):
        if board[row][j] == value:
            return False
    # box check
    x0 = col//grid_len * grid_len
    y0 = row//grid_len * grid_len

    for row in range(y0,y0+grid_len):
        for col in range(x0,x0+grid_len):
            if board[row][col] == value:
                return False
    return True

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


def prefill():
    global num, VALUES, board
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == '*':
                for value in VALUES:
                    if check_criteria(value, row, col):
                        board[row][col] = value
                        prefill()
                        board[row][col] = '*'
                return
    if num == 0:
        pset_init()
        gen_pset()
        num += 1
    solve_board()

def init_board():
    global empty_cells, board, EMPTY, VALUES
    to_be_filled = make_empty()


    for cell in to_be_filled:
        row, col = cell[0], cell[1]
        board[row][col] = '*'
    

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
# and the entire row and also find restricted cells
def gen_pset():
    # generate all possible values for each cell ahead of time
    global EMPTY, board, VALUES, empty_cells
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                for value in VALUES:
                    if check_criteria(value, row, col):
                        empty_cells[row][col].append(value)
                # the single candidate
                if len(empty_cells[row][col]) == 1:
<<<<<<< HEAD
                    # got a singleton
                    print('GOT A SINGLETON')
                    # sleep(4)
=======
>>>>>>> new
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


def solve_board():
    global board, empty_cells, EMPTY, tFILLED
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                for value in empty_cells[row][col]: 
                    if check_criteria(value,row,col):
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
