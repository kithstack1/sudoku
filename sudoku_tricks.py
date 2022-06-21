from time import sleep

class Tricks:

    def __init__(self,app):
        self.board = app.board
        self.empty_cells = app.empty_cells
        self.width = app.width
        self.block_width = app.block_width
        self.values = app.values
        self.blocks = app.blocks

    def single_position(self):
        # check row
        for row in self.empty_cells:
            value_map = {value:[0,[]] for value in self.values}
            for column in self.empty_cells[row]:
                for value in self.empty_cells[row][column]:
                    value_map[value][0] += 1
                    value_map[value][1].append(column)
            for value in value_map:
                if value_map[value][0] == 1: 
                    column = value_map[value][1][0]
                    self.board[row][column] = value
                    # delete the cell from empty_cells hash map
                    
                    try:
                       del self.empty_cells[row][column]
                    except Exception:
                        pass
                    # delete any occurence of the value in the p_candidates in the block its in
                    # the row its in and the column          
                    self.update_candidate_set(row,column,value)

        # check column
        for column in range(self.width):
            value_map = {value:[0,[]] for value in self.values}
            for row in self.empty_cells:
                if column in self.empty_cells[row]:
                    for value in self.empty_cells[row][column]:
                        value_map[value][0] += 1
                        value_map[value][1].append(row)
            for value in value_map:
                if value_map[value][0] == 1:
                   row = value_map[value][1][0]
                   self.board[row][column] = value
                   del self.empty_cells[row][column]
                   self.update_candidate_set(row,column,value)

        for block in self.blocks:
            value_map = {value:[0,[]] for value in self.values}
            row, col = block[0], block[1]
            for r in range(row, row+self.block_width):
                if r in self.empty_cells:
                    for c in range(col, col+self.block_width):
                        if c in self.empty_cells[r]:
                            for value in self.empty_cells[r][c]:
                                value_map[value][0] += 1
                                value_map[value][1].append((r,c))
            for value in value_map:
                if value_map[value][0] == 1: 
                    cell_cord = value_map[value][1][0]
                    r,c = cell_cord[0], cell_cord[1]
                    self.board[r][c] = value
                    # delete the cell from empty_cells hash map
                    del self.empty_cells[r][c]
                    # delete any occurence of the value in the p_candidates in the block its in
                    # the row its in and the column          
                    self.update_candidate_set(r,c,value)
       
        return self.board, self.empty_cells
    
    
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
        
        
