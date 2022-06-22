from tkinter import *
import tkinter
from tkinter.ttk import *





class GUI:

    def __init__(self,app):
        self.app = app
        self.main_window = Tk()
        self.appwidth = 800
        self.appheight = 800
        self.main_window.geometry(f'{self.appwidth}x{self.appheight}')
        self.main_window.title('SUDOKU SOLVER')
        self.main_window.eval('tk::PlaceWindow . center')
        self.main_window.minsize(800,800)


        self.board_frame = tkinter.Frame(self.main_window, highlightbackground="blue", highlightthickness=2)
        self.board_frame.configure(borderwidth=6)
        self.board_frame.place(relx=.5,rely=.5,anchor=CENTER)

        self.controls_frame = tkinter.Frame(self.main_window,highlightbackground="blue", highlightthickness=2)
        self.controls_frame.configure(borderwidth=6)
        self.controls_frame.place(relx=.7,y=11)

        self.count = 0

        self.board = app.board
        self.make_entries()

        # solve board
        self.sframe = Frame(self.controls_frame)
        self.sframe.grid(row=0,column=0,padx=2,pady=2)
        # solve button
        self.solve_button = Button(self.sframe,text='SOLVE',command=self.solve)
        self.solve_button.grid(row=0,column=0)

        # reset board
        self.reset_button = Button(self.controls_frame,text='RESET BOARD',command=self.reset)
        self.reset_button.grid(row=1,column=0)

        # time label
        self.time_label = Label(self.main_window,font=('monospace 30 bold')).place(relx=0.3,rely=11)


    def time(self):
        count_mins = self.count // 60
        count_mins = count_mins if len(str(count_mins)) > 1 else f'0{count_mins}'
        count_secs = count%60
        count_secs = count_secs if len(str(count_secs)) > 1 else f'0{count_secs}'
        new_time = f'time: |{count_mins}:{count_secs}|'
        self.time_label.config(text=new_time)
        self.time_label.after(1000,self.time)
        count += 1

    def make_entries(self):
        temp_entries = [Entry(self.board_frame,width=2,font='Helvetica 35 bold',justify=CENTER) for _ in range(len(self.board)**2)]
        ri = [i for i in range(len(self.board))]
        ci = ri.copy()
        for row in ri:
            for col in ci:
                text = temp_entries.pop()
                text.grid(row=row,column=col)
                text.insert(-1,self.board[row][col])


    def solve(self):
        next(self.app.solve_board())

    def reset(self):
        self.app.__init__()
        self.__init__(self.app)







