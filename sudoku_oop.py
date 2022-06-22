from random import randint
from sudoku_tricks import Tricks
import string
from sudoku_gui import GUI


class Sudoku:

    """ simple CLI sudoku solver and sudoku generator """

    def __init__(self, pfilled:int, values:list):
        self.EMPTY = '*'
        self.gen_filled = '#'
        self.pfilled = pfilled
        self.values = values
        self.width = len(values)
        self.block_width = int(self.width**0.5)
        self.empty_cells = {}
        self.board = [[self.EMPTY for _ in range(len(self.values))] for _ in range(len(self.values))]
        self.blocks = self.get_blocks() 

    def draw_board(self):
        for i in range(self.width):
            row_data = []
            for j in range(self.width):
                if (not j%self.block_width) and (j != self.width-1) and j != 0:
                    cell_data = f'| {self.board[i][j]}'
                else:
                    cell_data = f'  {self.board[i][j]}'
                row_data.append(cell_data)    
                print(cell_data,end='') 
            print('',end='\n')
            if (not (i+1)%self.block_width) and i!= 0 and i != (self.width-1):
                print('-'*len(''.join(row_data)))
        print()


    def mark_empty(self):
        i = 0
        p_filled_set = []
        while i < self.pfilled:
            row, col = randint(0,self.width-1), randint(0,self.width-1)
            cell = (row,col)
            if cell in p_filled_set:
                continue
            p_filled_set.append(cell)
            i += 1
        return p_filled_set

    def initialize_board(self):
        filled_by_generator = self.mark_empty()
        for cell in filled_by_generator:
            row, col = cell[0], cell[1]
            self.board[row][col] = self.gen_filled

    def is_valid(self,value,row,col):
        # vertical check
        for i in range(len(self.board)):
            if self.board[i][col] == value:
                return False
        # horizontal check
        for j in range(self.width):
            if self.board[row][j] == value:
                return False
        # block check
        x0 = col//self.block_width * self.block_width
        y0 = row//self.block_width * self.block_width


        for row in range(y0,y0+self.block_width):
            for col in range(x0,x0+self.block_width):
                if self.board[row][col] == value:
                    return False
        return True
    
    def fill_givens(self):
        for row in range(self.width):
            for col in range(self.width):
                if self.board[row][col] == self.gen_filled:
                    for value in self.values:
                        if self.is_valid(value, row, col):
                            self.board[row][col] = value
                            yield from self.fill_givens()
                            self.board[row][col] = self.gen_filled
                    return
        self.initialize_candidate_set()
        self.generate_candidate_set()
        yield
    
    def initialize_candidate_set(self):
        for row in range(self.width):
            if self.EMPTY in self.board[row]:
                self.empty_cells[row] = {}
                for col in range(self.width):
                    if self.board[row][col] == self.EMPTY:
                        self.empty_cells[row][col] = []

    def generate_candidate_set(self):
        for row in range(self.width):
            for col in range(self.width):
                if self.board[row][col] == self.EMPTY:
                    for value in self.values:
                        if self.is_valid(value, row, col):
                            self.empty_cells[row][col].append(value)
                    # the single candidate
                    if len(self.empty_cells[row][col]) == 1:
                        # got a singleton
                        # force the value into the board
                        self.board[row][col] = self.empty_cells[row][col][0]
                        # delete the cell from empty_cells
                        del self.empty_cells[row][col]
                        # clear any occerence of the value in p_candidates in the cell's block , row and column
                        self.update_pset(row, col, value)
                    elif len(self.empty_cells[row][col]) == 0:
                        # board is unsolvable
                        # probabaly too many prefilled cells
                        print('board is unsolvable')

    def update_candidate_set(self,row,col,value):
        # clear value from p_candidates in  row
        for cell in self.empty_cells[row]:
            try:
                self.empty_cells[row][cell].remove(value)
            except Exception:
                continue

        # clear value from p_candidates in  column
        for r in self.empty_cells:
            try:
                self.empty_cells[r][col].remove(value)
            # just in case the r, c intersection isn't empty in any row for this empty cell
            except Exception:
                continue

        # clear value from p_candidates in  block
        x0 = (col // self.block_width) * self.block_width
        y0 = (row // self.block_width) * self.block_width
        for r in range(y0+self.block_width):
            for c in range(x0,x0+self.block_width):
                try:
                    self.empty_cells[r][c].remove(value)
                except Exception:
                    continue



    def solve_board(self):
        for row in range(self.width):
            for col in range(self.width):
                if self.board[row][col] == self.EMPTY:
                    for value in self.empty_cells[row][col]: 
                        if self.is_valid(value,row,col):
                            self.board[row][col] = value
                            yield from self.solve_board()
                            self.board[row][col] = self.EMPTY
                    self.lastrow, self.lastcol = row, col
                    return # all values incompatible , return to parent caller
        print('board is solved , no more empty slots')
        yield(self.draw_board())


    def get_blocks(self):
        row_indices = [i for i in range(0,self.width) if not i%self.width]
        col_indices = row_indices.copy()
        blocks = []
        for i in row_indices:
            for j in col_indices:
                blocks.append((i,j))
        return blocks


values = list(string.ascii_uppercase)[:9]
app = Sudoku(pfilled=20,values=values)


def main():
    gui = GUI(app)
    gui.app.initialize_board()
    next(gui.app.fill_givens())
    #gui.app.draw_board()
    gui.make_entries()
    gui.time()
    gui.app.initialize_candidate_set()
    gui.app.generate_candidate_set()
    tricks = Tricks(gui.app)
    gui.app.board, gui.app.empty_cells = tricks.single_position()
    gui.mainloop()


if __name__ == '__main__':
   main()
 



