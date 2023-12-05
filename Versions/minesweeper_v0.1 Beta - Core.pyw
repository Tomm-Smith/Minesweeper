import tkinter as tk
import os
import random

global debug
debug = True



class MineSweeper:
    """ MineSweeper - GUI / Game Logic Object
    ToDo:
        - Organize methods by functional purpose, alphabetically
        - Experiment with using an image class for a generalized definition
          of required images used.
        - High Score system
        - Rename images s/bomb/mine/g
        - Manually populate minefield from Game and analyze / store
        - Make generalized function for 7 segment display updating. 
            EG. set_display('timer', 30) - Works on both displays
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
        self.sevenseg = [n for n in range(11)]
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
        self.sevenseg[10] = tk.PhotoImage(file=fr"{path}\img\7_segment\-.gif")
        
        # Mine Face... is a handsome one
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
        if debug:
            self.root.geometry("164x202+350+468")
        else:
            self.root.geometry("164x202")
        
        # UI details
        self.dark_edge = "#808080"
        self.transient_edge = "#C0C0C0"
        self.light_edge = "#FFFFFF"
        
        self.mine_pxs = 16
        self.field_size = 9
        
        self.mines = 10
        self.mines_remaining = self.mines
        
        # Mine Border Calc - DO NOT CHANGE
        self.mine_border = 4
        
        # Field dimensions
        self.field_width = self.mine_pxs * self.field_size
        self.field_height = self.field_width
        
        # Field adjusted border
        self.field_width_bd = self.field_width + (self.mine_border * 2)
        self.field_height_bd = self.field_width_bd

        # Field declaration
        self.field = []
        self.field_imgs = []
        
        # Mine Counter image ID index
        self.mine_cnt_ids = [None, None, None]
        
        # Timer basis
        self.mine_time = 0
        self.mine_time_limit = 999
        self.mine_timer_bool = False
        self.mine_timer_ids = [None for i in range(3)]
        
        """
        MineSweeper()
        """
        self.__gui__()
        self.__events__()
        self.draw_grid()
        
        self.mainloop()
        
    def __gui__(self):
        self.root.config(background="#C0C0C0")
        ### File Menu ###
        self.menubar = tk.Menu(self.root)
        
        if not debug:
            self.file = tk.Menu(self.menubar, tearoff=0)
            self.file.add_command(label="Something", command="")
            self.menubar.add_cascade(label="File", menu=self.file)
            
            self.help = tk.Menu(self.menubar, tearoff=0)
            self.help.add_command(label="Or Another", command="")
            self.menubar.add_cascade(label="Help", menu=self.help)
            """ Help Dialog:
                - EasterEgg?
                - It aslways seems impossible until it's done. - Nelson Mandela
            """
        
        if debug:
            self.debug = tk.Menu(self.menubar, tearoff=0)

            self.debug.add_separator()

            self.menubar.add_cascade(label="Debug", menu=self.debug)
            
            
            self.field_menu = tk.Menu(self.menubar, tearoff=0)

            self.field_menu.add_separator()

            self.menubar.add_cascade(label="Field", menu=self.field_menu)
        
        self.root.config(menu=self.menubar)
        
        ### MineField ###
        # Border
        self.minefield_bd_frm = tk.Frame(self.root, border=self.mine_border, 
            background="#C0C0C0")
        self.minefield_bd_frm.pack(side="bottom")
        
        self.minefield_bd = tk.Canvas(self.minefield_bd_frm, 
            height=self.field_height_bd, 
            width=self.field_width_bd, 
            background="#C0C0C0", 
            bd=0, highlightthickness=0)
        self.minefield_bd.pack(fill="none", expand=False)
        
        self.draw_mine_border()
        
        # Field
        self.minefield = tk.Canvas(self.minefield_bd, 
            height=self.field_height, 
            width=self.field_width, 
            background="#C0C0C0",
            bd=0, highlightthickness=0)
        self.minefield_bd.create_window(3, 3, anchor="nw", window=self.minefield)
        
        ### ScoreBoard ###
        self.scoreboard_frm = tk.Frame(self.root, highlightthickness=0)
        self.scoreboard_frm.pack(side="bottom")
        
        self.scoreboard = tk.Canvas(self.scoreboard_frm, width=150,
            height=37, highlightthickness=0, background="#C0C0C0")
        self.scoreboard.pack()
        
        self.draw_scoreboard_border()
        
        # Mine Cnt
        self.mine_cnt = tk.Canvas(self.scoreboard, height=25, width=41,
            bd=0, highlightthickness=0, background="#C0C0C0")
        self.scoreboard.create_window(9, 8, anchor="nw", window=self.mine_cnt)
        
        self.set_mine_count()
        
        # Mine Face
        self.mine_face = tk.Label(self.root, image=self.smile_face, 
            bd=0, highlightthickness=0)
        self.scoreboard.create_window(62, 6, anchor="nw", window=self.mine_face)
        
        # Mine Timer
        self.mine_timer = tk.Canvas(self.scoreboard, height=25, width=41,
            bd=0, highlightthickness=0, background="#C0C0C0")
        self.scoreboard.create_window(102, 8, anchor="nw", window=self.mine_timer)
        
        self.draw_7seg_border()
        self.set_time(0)

    """ Event Handling Methods """
    def __events__(self):
        self.mine_face.bind("<ButtonPress-1>", self.mine_face_click)
        self.mine_face.bind("<ButtonRelease-1>", self.mine_face_release)

    def mine_face_click(self, event=None):
        pass

    def mine_face_release(self, event=None):
        pass

    def minefield_click(self, event=None):
        pass

    def minefield_release(self, event=None):
        pass

    """ Drawing Methods """
    def draw_scoreboard_border(self):
        # Top Edge
        self.scoreboard.create_line(0, 0, 148, 0, fill=self.dark_edge)
        self.scoreboard.create_line(0, 1, 148, 1, fill=self.dark_edge)
        
        # Top Right Corner
        self.scoreboard.create_line(148, 0, 149, 0, fill=self.dark_edge)
        self.scoreboard.create_line(149, 0, 150, 0, fill=self.transient_edge)
        self.scoreboard.create_line(148, 1, 149, 1, fill=self.transient_edge)
        self.scoreboard.create_line(149, 1, 150, 1, fill=self.light_edge)
        
        # Right Edge
        self.scoreboard.create_line(148, 2, 149, 150, fill=self.light_edge)
        self.scoreboard.create_line(149, 2, 150, 150, fill=self.light_edge)
        
        # Bottom Edge
        self.scoreboard.create_line(2, 35, 150, 35, fill=self.light_edge)
        self.scoreboard.create_line(2, 36, 150, 36, fill=self.light_edge)
        
        # Left Edge
        self.scoreboard.create_line(0, 0, 0, 35, fill=self.dark_edge)
        self.scoreboard.create_line(1, 0, 1, 35, fill=self.dark_edge)

        # Bottom Left Corner
        self.scoreboard.create_line(0, 35, 0, 36, fill=self.dark_edge)
        self.scoreboard.create_line(0, 36, 0, 37, fill=self.transient_edge)
        self.scoreboard.create_line(1, 35, 1, 36, fill=self.transient_edge)
        self.scoreboard.create_line(1, 36, 1, 37, fill=self.light_edge)
        
    def draw_7seg_border(self):
        ## Mine cnt 
        # Top Edge
        self.mine_cnt.create_line(0, 0, 40, 0, fill=self.dark_edge)
        
        # Right Edge
        self.mine_cnt.create_line(40, 1, 40, 24, fill=self.light_edge)
        
        # Bottom Edge
        self.mine_cnt.create_line(41, 24, 0, 24, fill=self.light_edge)
        
        # Left Edge
        self.mine_cnt.create_line(0, 0, 0, 24, fill=self.dark_edge)
        
        
        ## Mine Timer
        # Top Edge
        self.mine_timer.create_line(0, 0, 40, 0, fill=self.dark_edge)
        
        # Right Edge
        self.mine_timer.create_line(40, 1, 40, 24, fill=self.light_edge)
        
        # Bottom Edge
        self.mine_timer.create_line(41, 24, 0, 24, fill=self.light_edge)
        
        # Left Edge
        self.mine_timer.create_line(0, 0, 0, 24, fill=self.dark_edge)
        
    def draw_mine_border(self):
        # Top Edge
        self.minefield_bd.create_line(0, 0, 149, 0, fill=self.dark_edge)
        self.minefield_bd.create_line(149, 0, 150, 0, fill=self.transient_edge)
        
        self.minefield_bd.create_line(0, 1, 148, 1, fill=self.dark_edge)
        self.minefield_bd.create_line(148, 1, 149, 1, fill=self.transient_edge)
        self.minefield_bd.create_line(149, 1, 150, 1, fill=self.light_edge)
        
        self.minefield_bd.create_line(0, 2, 147, 2, fill=self.dark_edge)
        self.minefield_bd.create_line(147, 2, 148, 2, fill=self.transient_edge)
        self.minefield_bd.create_line(148, 2, 150, 2, fill=self.light_edge)

        # Left / Right Edge Fill
        self.minefield_bd.create_line(0, 3, 0, 147, fill=self.dark_edge)
        self.minefield_bd.create_line(1, 3, 1, 147, fill=self.dark_edge)
        self.minefield_bd.create_line(2, 3, 2, 147, fill=self.dark_edge)
        
        self.minefield_bd.create_line(147, 3, 147, 150, fill=self.light_edge)
        self.minefield_bd.create_line(148, 3, 148, 150, fill=self.light_edge)
        self.minefield_bd.create_line(149, 3, 149, 150, fill=self.light_edge)
        
        #Bottom Edge
        self.minefield_bd.create_line(0, 147, 2, 147, fill=self.dark_edge)
        self.minefield_bd.create_line(2, 147, 3, 147, fill=self.transient_edge)
        self.minefield_bd.create_line(3, 147, 149, 147, fill=self.light_edge)
        
        self.minefield_bd.create_line(0, 148, 1, 148, fill=self.dark_edge)
        self.minefield_bd.create_line(1, 148, 2, 148, fill=self.transient_edge)
        self.minefield_bd.create_line(2, 148, 149, 148, fill=self.light_edge)
        
        self.minefield_bd.create_line(0, 149, 1, 149, fill=self.transient_edge)
        self.minefield_bd.create_line(1, 149, 149, 149, fill=self.light_edge)
            
    def draw_grid(self):
        # Draw grid
        for n in range(self.field_size):
            # Horizontal
            self.minefield.create_line(0, n * self.mine_pxs, 
                self.field_width, n * self.mine_pxs, 
                fill="#808080")
            # Vertical
            self.minefield.create_line(n * self.mine_pxs, 0, 
                n * self.mine_pxs, self.field_height, 
                fill="#808080")
    
    """ UI Methods """
    def set_mine_count(self, step=0):
        """
        TODO: Make this dynamically update per only what needs changed in the 
                7 seg display
        """
        try:
            int(step)
        except ValueError:
            raise ValueError("Minesweeper -> set_mine_count(step): expects integer, other given")
        
        if step == 0:
            self.mines_remaining = self.mines
            
            
        self.mines_remaining += step
        
        if self.mines_remaining > 999:
            self.mines_remaining = 000
            
        # Delete previous images
        for i in range(len(self.mine_cnt_ids)):
            if self.mine_cnt_ids[i] != None:
                self.mine_cnt.delete(i)
                self.mine_cnt_ids[i] = None
            
        # Seperate our intergar
        _str = str(self.mines_remaining)

        # Properly pad with 0's
        if self.mines_remaining < -9:
            mines = [10, int(_str[1]), int(_str[2])]
            
        elif self.mines_remaining < 0:
            mines = [10, 0, int(_str[1])]
            
        elif self.mines_remaining == 0:
            mines = [0, 0, 0]
            
        elif self.mines_remaining < 10:
            mines = [0, 0, int(_str[0])]
        
        elif self.mines_remaining > 99:
            mines = [int(_str[0]), int(_str[1]), int(_str[2])]
            
        elif self.mines_remaining > 9:
            mines = [0, int(_str[0]), int(_str[1])]
            
        else:
            mines = [10, 10, 10]
        
        # Store img ID and assign image respectively
        self.mine_cnt_ids[0] = self.mine_cnt.create_image(1, 1, 
            image=self.sevenseg[mines[0]], anchor="nw")
        self.mine_cnt_ids[1] = self.mine_cnt.create_image(14, 1, 
            image=self.sevenseg[mines[1]], anchor="nw")
        self.mine_cnt_ids[2] = self.mine_cnt.create_image(27, 1, 
            image=self.sevenseg[mines[2]], anchor="nw")
            
        return True
            
    def timer_handle(self, time=None):
        """ Handle the timer hook to mainloop() and update the timer display"""
        # Stop timing loop if past time limit
        if self.mine_time >= self.mine_time_limit:
            if debug: print("MineSweeper -> timer_handle(): broke timer loop due to exceedance")
            return
        
        # Ensure only int on provided time
        if time != None:
            try:
                int(time)
            except TypeError:
                self.mine_time=0
                if debug: print("Internal Error: Minesweeper -> timer_handle(): given argument type other than int")
        
        # Update time and display
        self.mine_time += 1
        self.set_time(self.mine_time)
        
        # Attach our timer hook to mainloop()
        if self.mine_timer_bool:
            self.root.after(1000, self.timer_handle)
        
    def set_time(self, time=None):
        """TODO: Make this dynamically update the display; change the _ids list
           to include numbers of displayed segments
           TODO: Create is_int() method"""
            
        # Set argument default value to self.mine_time
        # Python does not allow self.vars to be argument defaults to methods
        # So if None: time = self.mine_time
        if time != None:
            # Ensure provided time is within range
            if time > self.mine_time_limit or time < 0:
                if debug: print("Limit Exceedance: Minesweeper -> set_time(): provided time argument is outside time limit")
                self.mine_time = 999
            else:
                self.mine_time = time
                
        ## Set mine time
        # integer's lack lefthand 0's, so we define and pad respectively
        segs = [0, 0, 0]
        
        # Single Digit Number
        if self.mine_time < 10:
            segs[2] = self.mine_time
        
        ## digits > 9 require string casting for individualizing the integer
        # Cast integer type to string, slice, cast to integer
        # Double Digit Number
        elif self.mine_time < 100:
            segs[1] = int(str(time)[0])
            segs[2] = int(str(time)[1])
        
        # Triple Digit Number
        elif self.mine_time < 1000:
            segs[0] = int(str(time)[0])
            segs[1] = int(str(time)[1])
            segs[2] = int(str(time)[2])
        
        # Clear our timer image ID's and reset index
        for i in range(len(self.mine_timer_ids)):
            self.mine_timer.delete(self.mine_timer_ids[i])
            self.mine_timer_ids[i] = None
            
        # Draw our timer segments
        self.mine_timer_ids[0] = self.mine_timer.create_image(1, 1, 
            image=self.sevenseg[segs[0]], 
            anchor="nw")
        self.mine_timer_ids[1] = self.mine_timer.create_image(14, 1, 
            image=self.sevenseg[segs[1]], 
            anchor="nw")
        self.mine_timer_ids[2] = self.mine_timer.create_image(27, 1, 
            image=self.sevenseg[segs[2]], 
            anchor="nw")

    """ Field Methods """
    def gen_field_matrix(self):
        pass
        
    def place_mines(self):
        pass
        
    def analyze_field(self):
        pass
    
    def sweep_field(self):
        pass
        
    def clear_field(self):
        pass
        
    def draw_field(self):
        pass
        
    def in_field(self):
        pass
        
    def is_mine(self):
        pass
        
    def is_flag(self):
        pass

    def mainloop(self):
        self.root.mainloop()
        
    
    """ DEBUG METHODS """


if __name__ == "__main__":
    ms = MineSweeper()