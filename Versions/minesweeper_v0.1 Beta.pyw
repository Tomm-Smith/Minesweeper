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
        self.gen_field_matrix(9)
        self.draw_blocks()
        #self.clear_field()
        
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
            self.debug.add_command(label="WildCard()", command=self.wildcard_debug)
            self.debug.add_command(label="toggle_buttons()", command=self.toggle_buttons)
            self.debug.add_command(label="flag_all()", command=self.flag_all)
            self.debug.add_command(label="question_all()", command=self.question_all)
            self.debug.add_separator()
            self.debug.add_command(label="mine++", command=lambda : self.set_mine_count(1))
            self.debug.add_command(label="mine--", comman=lambda : self.set_mine_count(-1))
            self.menubar.add_cascade(label="Debug", menu=self.debug)
            
            self.field_menu = tk.Menu(self.menubar, tearoff=0)
            self.field_menu.add_command(label="draw_field()", command=self.draw_field)
            self.field_menu.add_command(label="clear_field()", command=self.clear_field)
            self.field_menu.add_command(label="gen_mines() (Draw)", command=lambda : self.gen_mines(10))
            self.field_menu.add_command(label="print_field()", command=self.print_field)
            self.field_menu.add_command(label="print_field_imgs()", command=self.print_field_imgs)
            self.field_menu.add_separator()
            self.field_menu.add_command(label="debug_analyze_field()", command=self.debug_analyze_field)
            self.field_menu.add_command(label="debug_field()", command=self.debug_field)
            self.field_menu.add_command(label="debug_field_nums()", command=self.debug_field_nums)
            self.field_menu.add_separator()
            self.field_menu.add_command(label="debug_proof_wildcard()", command=self.debug_proof_wildcard)
            self.field_menu.add_command(label="debug_proof_1()", command=self.debug_proof_1)
            self.field_menu.add_command(label="debug_proof_2()", command=self.debug_proof_2)
            self.field_menu.add_command(label="debug_proof_3()", command=self.debug_proof_3)
            self.field_menu.add_separator()
            self.field_menu.add_command(label="Mines", command=lambda : self.fill_field('x'))
            self.field_menu.add_command(label="Blank", command=lambda : self.fill_field(0))
            self.field_menu.add_command(label="One", command=lambda : self.fill_field(1))
            self.field_menu.add_command(label="Two", command=lambda : self.fill_field(2))
            self.field_menu.add_command(label="Three", command=lambda : self.fill_field(3))
            self.field_menu.add_command(label="Four", command=lambda : self.fill_field(4))
            self.field_menu.add_command(label="Five", command=lambda : self.fill_field(5))
            self.field_menu.add_command(label="Six", command=lambda : self.fill_field(6))
            self.field_menu.add_command(label="Seven", command=lambda : self.fill_field(7))
            self.field_menu.add_command(label="Eight", command=lambda : self.fill_field(8))
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
        
    def __events__(self):
        self.mine_face.bind("<ButtonPress-1>", self.mine_face_click)
        self.mine_face.bind("<ButtonRelease-1>", self.mine_face_release)
        
    def set_mine_face(self, face="smile"):
        """Faces:
            - smile_face
            - smile_face_pressed
            - wow_face
            - lose_face
            - win_face
        """
        
        if face == "smile":
            self.mine_face.config(image=self.smile_face)
            
        elif face == "pressed":
            self.mine_face.config(image=self.smile_face_pressed)
            
        elif face == "wow":
            self.mine_face.config(image=self.wow_face)
            
        elif face == "lose":
            self.mine_face.config(image=self.lose_face)
            
        elif face == "win":
            self.mine_face.config(image=self.win_face)
    
    def mine_face_click(self, event):
        self.set_mine_face("pressed")
        self.mine_timer_bool = False
    
    def mine_face_release(self, event):
        #print(f"DEBUG: mine_face_release: PRE: \n{self.print_field()}")
        
        self.clear_blocks()
        self.draw_blocks()

        self.gen_field_matrix(self.mines)
        self.gen_mines()
        self.analyze_field()
        self.draw_field()

        self.set_mine_count()
        self.set_time(0)

        self.set_mine_face("smile")

        #print(f"DEBUG: mine_face_release: POST: \n{self.print_field()}")
        
    def field_click(self, event):
        btn = self.field_btns[event.widget.id]
        
        # Start timer
        if not self.mine_timer_bool:
            self.mine_timer_bool = True
            self.timer_handle()
        
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
            # draw_blocks_new dev feature
            #self.field[event.widget.y_coord][event.widget.x_coord][1] = True
            self.set_mine_count(-1)

        elif event.widget.flag == 2:
            event.widget.config(image=self.question_block)
            #self.field[event.widget.y_coord][event.widget.x_coord][1] = False
            self.set_mine_count(1)
            
        else:
            print("ERROR: field_flag_click(): unhandled exception")

    def mine_click(self, event=None):
        """
        - show wrong flags
        - show mines
        - change face
        """
        event.widget.destroy()
        print("GAME OVER")
        
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
            
    def draw_blocks(self):
        # Cover mine field with blocks
        self.field_btns = [n for n in range(self.field_size * self.field_size)]
        # Canvas/Button place offset
        field_x, field_y = 0, 0
        step=0
        
        for y in range(self.field_size):
            for x in range(self.field_size):
                # Create blank img button
                self.field_btns[step] = tk.Label(self.minefield, 
                    image=self.blank_block, highlightthickness=0, bd=0)
                    
                self.field_btns[step].id = step
                # Choose handler for what's under the clicked block
                if self.field[y][x][0] == 'x':
                    self.field_btns[step].bind("<Button-1>", self.mine_click)
                else:
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
                
    def clear_blocks(self):
        # TODO: What is the best way to incorporate this functionality?
        for block in self.field_btns:
            block.destroy()
        
    def draw_blocks_new(self):
        # Canvas/Button place offset
        field_x, field_y = 0, 0
        # step=0
        
        for y in range(self.field_size):
            for x in range(self.field_size):
                # Create blank img button
                btn = tk.Label(self.minefield, 
                    image = self.blank_block, highlightthickness=0, bd=0)
                    
                #self.field_btns[step].id = step
                btn.x_coord = x
                btn.y_coord = y
                btn.flag = 0

                # flag bomb status to object
                if self.field[y][x][0] == 'x':
                    btn.bind("<Button-1>", self.mine_clicked)
                else:
                    btn.bind("<Button-1>", self.field_click)
                    
                btn.bind("<Button-3>", self.field_flag_click)
                
                btn.place(x=field_x, 
                    y=field_y)
                # Offset x
                field_x += self.mine_pxs
                #step += 1
                
            field_x = 0
            field_y += self.mine_pxs
        
    def gen_field_matrix(self, size):
        """
        field = [[[0, None], [0, None], [0, None],
                 [[0, None], [0, None], [0, None],
                 [[0, None], [0, None], [0, None]
                ]
        
        field[y][x][0] = 0 - Minefield Element (Mine or number)
        field[y][x][1] = None - Accessory Place holder for mine_flags, img id   
                            of respective grid image with flag
                            
        0 - Blank
        x - Mine
        1-8 - Analysis
        """
        self.field = []
        
        for i in range(size):
            fld = [[0, None] for x in range(size)]
            self.field.append(fld)
    
        return self.field
    
    def place_mine(self):
        x = random.randrange(0, self.field_size)
        y = random.randrange(0, self.field_size)
        
        return [x, y]
        
    def gen_mines(self, qty=10):
        self.clear_field()
        
        for n in range(qty):
            x, y = self.place_mine()
            
            if self.field[y][x] != 'x':
                self.field[y][x][0] = 'x'

    def is_mine(self, x, y):
        """ If x in grid and is 'x' return True, False otherwise"""
        try:
            if self.field[y][x][0] == 'x':
                return True
            else:
                return False
        except IndexError:
            return False
            
    def in_field(self, x, y):
        """ Is [x,y] a valid position in the field grid"""
        # Only check positive numbers to prevent grid runoff
        if x < 0 or y < 0:
            return False
        
        # Ensure locations is within grid area
        try:
            self.field[y][x][0]
        except IndexError:
            return False
        else:
            return True
            
    def analyze_field(self):
        for y in range(len(self.field)):
            for x in range(len(self.field)):
                if self.is_mine(x, y):
                    if debug:
                        print(f"DEBUG: analyze_field(): x:{x} y:{y} is_mine: {self.is_mine(x, y)}")

                    ## Previous Row
                    # Up and Left
                    if not self.is_mine(x-1, y-1) and self.in_field(x-1, y-1):
                        self.field[y-1][x-1][0] += 1
                        
                    # Up
                    if not self.is_mine(x, y-1) and self.in_field(x, y-1):
                        self.field[y-1][x][0] += 1
                 
                    # Up and Right
                    if not self.is_mine(x+1, y-1) and self.in_field(x+1, y-1):
                        self.field[y-1][x+1][0] += 1
                    
                    ## Mine Row
                    # Left
                    if not self.is_mine(x-1, y) and self.in_field(x-1, y):
                        self.field[y][x-1][0] += 1
                        
                    # Right
                    if not self.is_mine(x+1, y) and self.in_field(x+1, y):
                        self.field[y][x+1][0] += 1
                    
                    ## Next Row
                    # Down and Left
                    if not self.is_mine(x-1, y+1) and self.in_field(x-1, y+1):
                        self.field[y+1][x-1][0] += 1
                        
                    # Down
                    if not self.is_mine(x, y+1) and self.in_field(x, y+1):
                        self.field[y+1][x][0] += 1
                        
                    # Down and Right
                    if not self.is_mine(x+1, y+1) and self.in_field(x+1, y+1):
                        self.field[y+1][x+1][0] += 1

    def sweep_analyze(self):
        pass
        
    def clear_field_imgs(self):
        """ Clear all images from the field"""
        for id in self.field_imgs:
            self.minefield.delete(id)
            
        self.field_imgs = []
        
    def clear_field(self):
        """ Clear the field and image objects"""
        self.clear_field_imgs()
        self.field = self.gen_field_matrix(self.field_size)
        
    def draw_field(self):
        # TODO: Manage drew images to prevent memory overflow
        img_src = None
        # TODO: Why does this require 8px offset?
        field_x, field_y = 8, 8
        
        self.clear_field_imgs()
        
        # Set what image needs drew
        for y in range(self.field_size):
            for x in range(self.field_size):
            
                if self.field[y][x][0] == 'x':
                    img_src = self.mine
                    
                elif self.field[y][x][0] == 1:
                    img_src = self.mine_nums[1]
                    
                elif self.field[y][x][0] == 2:
                    img_src = self.mine_nums[2]
                    
                elif self.field[y][x][0] == 3:
                    img_src = self.mine_nums[3]
                    
                elif self.field[y][x][0] == 4:
                    img_src = self.mine_nums[4]
                    
                elif self.field[y][x][0] == 5:
                    img_src = self.mine_nums[5]
                    
                elif self.field[y][x][0] == 6:
                    img_src = self.mine_nums[6]
                    
                elif self.field[y][x][0] == 7:
                    img_src = self.mine_nums[7]
                    
                elif self.field[y][x][0] == 8:
                    img_src = self.mine_nums[8]
                    
                else:
                    img_src = self.mine_nums[0]
                    
                # Track our image ID's
                self.field_imgs.append(
                    self.minefield.create_image(field_x, field_y, image=img_src))

                # Offset x
                field_x += self.mine_pxs
            
            # Reset x and offset y
            field_x = 8
            field_y += self.mine_pxs
        
    def mainloop(self):
        self.root.mainloop()
        
    """ DEBUG METHODS """
    def toggle_buttons(self):
        self.mines_remaining = self.mines
        self.set_mine_count(0)
        
        try:
            self.toggle_buttons_debug_flip
        except:
            self.toggle_buttons_debug_flip = False
            
        if self.toggle_buttons_debug_flip:
            self.draw_blocks()
            self.toggle_buttons_debug_flip = False
            return
        
        for obj in self.field_btns:
            obj.destroy()
        
        self.toggle_buttons_debug_flip = True
        
    def flag_all(self):
        try:
            self.debug_flag_all_flagged
        except:
            self.debug_flag_all_flagged = False
        finally:
            if self.debug_flag_all_flagged:
                for obj in self.field_btns:
                    self.field_flag_click(obj)
                self.debug_flag_all_flagged = False
            else:
                self.debug_flag_all_flagged = True
                
        for obj in self.field_btns:
            self.field_flag_click(obj)
        
    def question_all(self):
        None    
        
    def wildcard_debug(self):
        None
        
    def fill_field(self, fill='x'):
        self.clear_field()
        
        for y in range(len(self.field)):
            for x in range(len(self.field)):
                self.field[y][x][0] = fill
            
        self.draw_field()

    def print_field(self):
        for y in range(len(self.field)):
            for x in range(len(self.field)):
                print(f"{self.field[y][x][0]} ", end="")
            print()
            
        print("---------------------------------------------------------------")
    
    def print_field_imgs(self):
        print(f"DEBUG: print_field_imgs(): {self.field_imgs}")
        
    def debug_analyze_field(self):
        self.analyze_field()
        self.draw_field()
        
    def debug_field(self):
        self.field = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 'x', 'x', 0, 'x'],
                      ['x', 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 'x', 0, 'x'],
                      [0, 0, 'x', 0, 'x', 0, 0, 0, 0],
                      [0, 0, 0, 0, 'x', 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 'x', 0, 0, 0, 0, 0]]
    
        for y in range(len(self.field)):
            for x in range(len(self.field)):
                self.field[y][x] = [self.field[y][x], None]
                
        self.draw_field()
                
    def debug_field_nums(self):
        self.field = [[ 0,  0,  0,  0,  0,  0,   0,  0,  0],
                      [ 0,  0,  0,  0,  1,  2,   2,  2,  1],
                      [ 1,  1,  0,  0,  1, 'x', 'x', 2, 'x'],
                      ['x', 1,  0,  0,  1,  3,   3,  4,  2],
                      [ 1,  2,  1,  2,  1,  2,  'x', 2, 'x'],
                      [ 0,  1, 'x', 3, 'x', 3,   1,  2,  1],
                      [ 0,  1,  1,  3, 'x', 2,   0,  0,  0],
                      [ 0,  0,  1,  2,  2,  1,   0,  0,  0],
                      [ 0,  0,  1, 'x', 1,  0,   0,  0,  0]]
    
        for y in range(len(self.field)):
            for x in range(len(self.field)):
                if self.field[y][x] == 9:
                    self.field[y][x] = ['x', None]
                else:
                    self.field[y][x] = [self.field[y][x], None]
                    
        self.draw_field()
                
    def draw_field_debug(self):
        self.draw_field()
        
    def debug_proof_wildcard(self):
        """[[0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        """
        self.field = [[1, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
        for y in range(len(self.field)):
            for x in range(len(self.field)):
                if self.field[y][x] == 1:
                    self.field[y][x] = ['x', None]
                else:
                    self.field[y][x] = [self.field[y][x], None]
                    
        self.draw_field()
        
    def debug_proof_1(self):
        self.field = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 0, 1, 1],
                      [0, 0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 1, 0, 0, 0, 0, 0, 0, 0],
                      [1, 1, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
        for y in range(len(self.field)):
            for x in range(len(self.field)):
                if self.field[y][x] == 1:
                    self.field[y][x] = ['x', None]
                else:
                    self.field[y][x] = [self.field[y][x], None]
                    
        self.draw_field()

    def debug_proof_2(self):
        self.field = [[1, 1, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 1, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 1, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
        for y in range(len(self.field)):
            for x in range(len(self.field)):
                if self.field[y][x] == 1:
                    self.field[y][x] = ['x', None]
                else:
                    self.field[y][x] = [self.field[y][x], None]
                    
        self.draw_field()
        
    def debug_proof_3(self):
        self.field = [[1, 1, 0, 0, 1, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 1, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 1, 0, 1, 0, 0]]
    
        for y in range(len(self.field)):
            for x in range(len(self.field)):
                if self.field[y][x] == 1:
                    self.field[y][x] = ['x', None]
                else:
                    self.field[y][x] = [self.field[y][x], None]
                    
        self.draw_field()


if __name__ == "__main__":
    ms = MineSweeper()