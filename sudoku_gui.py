import tkinter as tk
from tkinter import  ttk
from sudoku_tricks import Tricks





class GUI(tk.Tk):

    def __init__(self,app):
        super().__init__()
        self.app = app
        self.appwidth = 800
        self.appheight = 800
        self.geometry(f'{self.appwidth}x{self.appheight}')
        self.title('SUDOKU SOLVER')
        self.eval('tk::PlaceWindow . center')
        self.minsize(800,800)


        self.board_frame = tk.Frame(self, highlightbackground="blue", highlightthickness=2)
        self.board_frame.configure(borderwidth=6)
        self.board_frame.place(relx=.5,rely=.5,anchor=tk.CENTER)

        self.controls_frame = tk.Frame(self,highlightbackground="blue", highlightthickness=2)
        self.controls_frame.configure(borderwidth=6)
        self.controls_frame.place(relx=.7,y=11)

        self.count = 0

        self.board = app.board
        #self.make_entries()

        # solve board
        self.solver_frame = tk.Frame(self.controls_frame)
        self.solver_frame.grid(row=0,column=0,padx=2,pady=2)
        # solve button
        self.solve_button = ttk.Button(self.solver_frame,text='SOLVE',command=self.solve)
        self.solve_button.grid(row=0,column=0)

        # reset board
        self.reset_button = tk.Button(self.controls_frame,text='RESET BOARD',command=self.reset)
        self.reset_button.grid(row=1,column=0)

        # time label
        self.time_label = tk.Label(self,font=('monospace 30 bold'))
        self.time_label.place(relx=.2,y=11)
        self.timer = ''


    def time(self):
        count_mins = self.count // 60
        count_mins = count_mins if len(str(count_mins)) > 1 else f'0{count_mins}'
        count_secs = self.count%60
        count_secs = count_secs if len(str(count_secs)) > 1 else f'0{count_secs}'
        new_time = f'time: |{count_mins}:{count_secs}|'
        self.time_label.config(text=new_time)
        self.timer = self.time_label.after(1000,self.time)
        self.count += 1

    def make_entries(self):
        temp_entries = [tk.Entry(self.board_frame,width=2,font='Helvetica 35 bold',justify=tk.CENTER) for _ in range(len(self.board)**2)]
        row_indices = [i for i in range(len(self.board))]
        column_indices = row_indices.copy()
        for row in row_indices:
            for column in column_indices:
                text = temp_entries.pop()
                text.grid(row=row,column=column)
                text.insert(-1,self.board[row][column])


    def solve(self):
        try:
           next(self.app.solve_board())
           self.clear_frame()
           self.make_entries()
        except:
            print('Board is Invalid')
       

    def reset(self):
        self.board = [['*' for _ in range(9)] for _ in range(9)]
        self.app.board = self.board
        self.app.emptycells = {}
        self.app.initialize_board()
        next(self.app.fill_givens())
        # kill timer
        self.time_label.after_cancel(self.timer)
        self.clear_frame()
        self.make_entries()
        self.count = 0
        self.time()
        self.app.initialize_candidate_set()
        self.app.generate_candidate_set()
        tricks = Tricks(self.app)
        self.app.board, self.app.empty_cells = tricks.single_position()
        

    def clear_frame(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()





