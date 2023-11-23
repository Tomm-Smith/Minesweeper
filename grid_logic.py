import tkinter as tk
import os
import random

global debug
debug = 0


class MineSweeper:
    """ 
    ToDo:
        - Experiment with using an image class for a generalized definition
          of required images used.
        - High Score system
        - Rename images s/bomb/mine/g
    NOTES:
        - Make sure the game reset destroy()'s all the button widgets/bindings
        - What's not your sweep? Minesweeper. 
        - What did the CEO call the janitor? MineSweeper.
    """
    def __init__(self):
        self.root = tk.Tk()
        #self.root.resizable(width=False, height=False) 
        if debug:
            self.root.attributes('-alpha', 1)
        
        """ 
        Image objects
        """
        path = os.getcwd()
        
        # 7 Segment Display
        self.sevenseg = [n for n in range(10)]
        self.sevenseg[0]= tk.PhotoImage(file=fr"{path}\img\7_segment\0.gif")
        self.sevenseg[1] = tk.PhotoImage(file=fr"{path}\img\7_segment\1.gif")
        self.sevenseg[2] = tk.PhotoImage(file=fr"{path}\img\7_segment\2.gif")
        self.sevenseg[3] = tk.PhotoImage(file=fr"{path}\img\7_segment\3.gif")
        self.sevenseg[4] = tk.PhotoImage(file=fr"{path}\img\7_segment\4.gif")
        self.sevenseg[5] = tk.PhotoImage(file=fr"{path}\img\7_segment\5.gif")
        self.sevenseg[6] = tk.PhotoImage(file=fr"{path}\img\7_segment\6.gif")
        self.sevenseg[7] = tk.PhotoImage(file=fr"{path}\img\7_segment\7.gif")
        self.sevenseg[8] = tk.PhotoImage(file=fr"{path}\img\7_segment\8.gif")
        self.sevenseg[9] = tk.PhotoImage(file=fr"{path}\img\7_segment\9.gif")
        
        self.smile_face = tk.PhotoImage(file=fr"{path}\img\smile_face.gif")
        self.smile_face_pressed = tk.PhotoImage(file=fr"{path}\img\smile_face_pressed.gif")
        self.wow_face = tk.PhotoImage(file=fr"{path}\img\wow_face.gif")
        self.lose_face = tk.PhotoImage(file=fr"{path}\img\lose_face.gif")
        self.win_face = tk.PhotoImage(file=fr"{path}\img\win_face.gif")
        
        # Mine cover blocks
        self.blank_block = tk.PhotoImage(file=fr"{path}\img\blank_block.gif")
        self.flag_block = tk.PhotoImage(file=fr"{path}\img\flag.gif")
        self.question_block = tk.PhotoImage(file=fr"{path}\img\question.gif")
        
        # Mine blocks. ...not yours!
        self.mine = tk.PhotoImage(file=fr"{path}\img\bomb.gif")
        self.mine_clicked = tk.PhotoImage(file=fr"{path}\img\bomb_clicked.gif")
        self.mine_wrong = tk.PhotoImage(file=fr"{path}\img\bomb_wrong.gif")
        
        # MineField numbers
        self.mine_nums = [n for n in range(9)]
        self.mine_nums[0] = tk.PhotoImage(file=fr"{path}\img\field_numbers\0.gif")
        self.mine_nums[1] = tk.PhotoImage(file=fr"{path}\img\field_numbers\1.gif")
        self.mine_nums[2] = tk.PhotoImage(file=fr"{path}\img\field_numbers\2.gif")
        self.mine_nums[3] = tk.PhotoImage(file=fr"{path}\img\field_numbers\3.gif")
        self.mine_nums[4] = tk.PhotoImage(file=fr"{path}\img\field_numbers\4.gif")
        self.mine_nums[5] = tk.PhotoImage(file=fr"{path}\img\field_numbers\5.gif")
        self.mine_nums[6] = tk.PhotoImage(file=fr"{path}\img\field_numbers\6.gif")
        self.mine_nums[7] = tk.PhotoImage(file=fr"{path}\img\field_numbers\7.gif")
        self.mine_nums[8] = tk.PhotoImage(file=fr"{path}\img\field_numbers\8.gif")
        
        """
        Environment elements
        """
        self.mine_pxs = 16
        self.grid_size = 9
        
        # Mine Border Calc - DO NOT CHANGE
        self.mine_border = 5
        
        self.field_width = self.mine_pxs * self.grid_size
        self.field_height = self.field_width
        
        self.field_width_bd = self.field_width + (self.mine_border * 2)
        self.field_height_bd = self.field_width_bd
        
        self.root.geometry("164x222")
        
        """
        MineSweeper()
        """
        self.__gui__()
        self.__events__()
        #self.draw_grid()
        #self.draw_blocks()
        #self.gen_field_matrix(9)
        
    def __gui__(self):
        self.root.config(background="#C0C0C0")
        ### File Menu ###
        """self.menubar = Menu(self.root)
        
        self.file = Menu(self.menubar, tearoff=0)
        self.file.add_command(label="New", command=None)
        self.file.add_separator()
        self.file.add_radiobutton(label="Beginner", command=None)
        self.file.add_radiobutton(label="Intermediate", command=None)
        self.file.add_radiobutton(label="Expert", command=None)
        self.file.add_radiobutton(label="Custom...", command=None)
        self.file.add_separator()
        self.file.add_checkbutton(label="Marks (?)", command=None)
        self.file.add_checkbutton(label="Color", command=None)
        self.file.add_checkbutton(label="Sound", command=None)
        self.file.add_separator()
        self.file.add_command(label="Best Times...")
        self.file.add_separator()
        self.file.add_command(label="Exit", command=tk.Quit)
        
        self.help = Menu(self.menubar, tearoff=0)
        self.help.add_comman(label="About", command=None)"""
        
        
        ### ScoreBoard ###
        self.scoreboard_frm = tk.Frame(self.root)
        self.scoreboard_frm.pack(side="top")
        
        self.scoreboard = tk.Canvas(self.scoreboard_frm, width=self.field_width,
            height=33, border=0, background="black")
        self.scoreboard.pack()
        
        #self.mine_cnt = tk.Canvas(self.scoreboard, )
        
        #self.mine_face = 
        
        #self.mine_timer = 
        
        
        ### MineField ###
        # Border
        self.minefield_bd_frm = tk.Frame(self.root, border=self.mine_border, 
            background="#C0C0C0")
        self.minefield_bd_frm.pack(side="bottom")
        
        self.minefield_bd = tk.Canvas(self.minefield_bd_frm, 
            height=self.field_height_bd, 
            width=self.field_width_bd, 
            background="#C0C0C0", 
            border=0, highlightthickness=0)
        self.minefield_bd.pack(fill="none", expand=False)
        
        self.draw_mine_border()
        
        # Field
        self.minefield = tk.Canvas(self.minefield_bd, 
            height=self.field_height, 
            width=self.field_width, 
            background="#C0C0C0",
            border=0, highlightthickness=0)
        self.minefield_bd.create_window(3, 3, anchor="nw", window=self.minefield)
        
    def __events__(self):
         None
         
    def field_click(self, event):
        btn = self.field_btns[event.widget.id]
        
        if btn.flag == 1:
            return
        
        else:
            btn.destroy()
        
    def field_flag_click(self, event):
        """ 0 - blank, 1 - bomb, 2 - question"""
        event.widget.flag = (event.widget.flag + 1) % 3
        
        if event.widget.flag == 0:
            event.widget.config(image=self.blank_block)

        elif event.widget.flag == 1:
            event.widget.config(image=self.flag_block)

        elif event.widget.flag == 2:
            event.widget.config(image=self.question_block)

        else:
            print("ERROR: field_flag_click(): unhandled exception")

    def draw_scoreboard_border(self):
        pass
        
    def draw_mine_border(self):
        # TODO: Make this dynamnically populated
        dark_edge = "#808080"
        transient_edge = "#c0c0c0"
        light_edge = "#FFFFFF"
        
        # Top Edge
        self.minefield_bd.create_line(0, 0, 149, 0, fill=dark_edge)
        self.minefield_bd.create_line(149, 0, 150, 0, fill=transient_edge)
        
        self.minefield_bd.create_line(0, 1, 148, 1, fill=dark_edge)
        self.minefield_bd.create_line(148, 1, 149, 1, fill=transient_edge)
        self.minefield_bd.create_line(149, 1, 150, 1, fill=light_edge)
        
        self.minefield_bd.create_line(0, 2, 147, 2, fill=dark_edge)
        self.minefield_bd.create_line(147, 2, 148, 2, fill=transient_edge)
        self.minefield_bd.create_line(148, 2, 150, 2, fill=light_edge)

        # Left / Right Edge Fill
        self.minefield_bd.create_line(0, 3, 0, 147, fill=dark_edge)
        self.minefield_bd.create_line(1, 3, 1, 147, fill=dark_edge)
        self.minefield_bd.create_line(2, 3, 2, 147, fill=dark_edge)
        
        self.minefield_bd.create_line(147, 3, 147, 150, fill=light_edge)
        self.minefield_bd.create_line(148, 3, 148, 150, fill=light_edge)
        self.minefield_bd.create_line(149, 3, 149, 150, fill=light_edge)
        
        #Bottom Edge
        self.minefield_bd.create_line(0, 147, 2, 147, fill=dark_edge)
        self.minefield_bd.create_line(2, 147, 3, 147, fill=transient_edge)
        self.minefield_bd.create_line(3, 147, 149, 147, fill=light_edge)
        
        self.minefield_bd.create_line(0, 148, 1, 148, fill=dark_edge)
        self.minefield_bd.create_line(1, 148, 2, 148, fill=transient_edge)
        self.minefield_bd.create_line(2, 148, 149, 148, fill=light_edge)
        
        self.minefield_bd.create_line(0, 149, 1, 149, fill=transient_edge)
        self.minefield_bd.create_line(1, 149, 149, 149, fill=light_edge)
        
    def draw_grid(self):
        # Draw grid
        for n in range(self.grid_size):
            # Horizontal
            self.minefield.create_line(0, n * self.mine_pxs, 
                self.field_width, n * self.mine_pxs)
            # Vertical
            self.minefield.create_line(n * self.mine_pxs, 0, 
                n * self.mine_pxs, self.field_height)
                
        #self.minefield.create_line(0, self.field_height-1, 
        #    self.field_width, self.field_height-1)
            
        #self.minefield.create_line(self.field_width-1, 0, 
        #    self.field_width-1, self.field_height)
            
    def draw_blocks(self):
        # Cover mine field with blocks
        self.field_btns = [n for n in range(self.grid_size * self.grid_size)]
        # Canvas/Button place offset
        field_x, field_y = 0, 0
        step=0
        
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                # Create blank img button
                self.field_btns[step] = tk.Label(self.minefield, 
                    image = self.blank_block, highlightthickness=0, bd=0)
                    
                self.field_btns[step].id = step
                self.field_btns[step].bind("<Button-1>", self.field_click)
                self.field_btns[step].bind("<Button-3>", self.field_flag_click)
                self.field_btns[step].flag = 0
                
                self.field_btns[step].place(x=field_x, 
                    y=field_y)
                # Offset x
                field_x += self.mine_pxs
                step += 1
                
            field_x = 0
            field_y += self.mine_pxs
                
    def place_image(self, img):
        pass
        
    def gen_field_matrix(self, size):
        self.field = []
        
        for i in range(size):
            fld = [0 for x in range(size)]
            self.field.append(fld)
            
        if debug:
            print(self.field)
    
    def place_mine(self):
        x = random.randrange(0, self.grid_size)
        y = random.randrange(0, self.grid_size)
        
        return [x, y]
        
    def gen_mines(self, qty, field):
        mine = place_mine()
        
        if field[mine[0]][mine[1]] == 'x':
            mine = place_mine()
            
        else:
            field[mine[x]][mine[y]] = 'x'
        
    def draw_field(self, qty):
        self.lbl = tk.Label(self.root, image=self.mine, highlightthickness=0, bd=0)
        self.lbl.place(x=2, y=2)
        
    def mainloop(self):
        self.root.mainloop()
        
        
if __name__ == "__main__":
    ms = MineSweeper()
    ms.mainloop()