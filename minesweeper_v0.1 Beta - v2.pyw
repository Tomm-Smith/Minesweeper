"""
TODO:
- are Minefield_Obj['mine_coords'] used for anything or excessive?
- Make certain all img's are properly removed!
- Only mask occupied slots on field in mask_field()
- Are the Canvas element of the proper attributes and decendance? 
    - Why do some elements have 1 px (draw_field()) offsets
- Fix white ghost on W side of block only when Button-1 is held between block
    click.
"""


import tkinter as tk
import os
import random

global debug
debug = True


class Minefield_Obj:
    """ Object for handling minefield organization. 

    Class Arguments:
        field_size (int) - Size of the minefield matrix

    Block Element Structure:
    dict - {'mine': 0, 
            'mine_coords': [0, 0], (y, x)
            'img_id' : None,
            'mask_id': None,
            'block_wdgt': None,
            'block_state': None}


    Structure Reference:
        mine:        - 9   - mine
                     - 0   - Empty
                     - 1-8 - Mine Proximity
        mine_coords: - [x, y] coordinates for mine location on field
        img_id:      - Image id of item on the minefield, None otherwise
        mask_id:     - Numeric ID of instantiated mask image hiding the mines 
                       until click_release, None otherwise
        block_wdgt:  - Individual Widget of block covering minefield, None otherwise
        block_state: - State of Field Block, EG. 'blank', 'flag', 'question'


    3x3 Matrix Default Reference
    field = [
             [
              {'mine': 0, 'mine_coords': [0, 0], 'img_id' : None, 'mask_id': None, 'block_wdgt': None, 'block_state': None},
              {'mine': 0, 'mine_coords': [0, 0], 'img_id' : None, 'mask_id': None, 'block_wdgt': None, 'block_state': None},
              {'mine': 0, 'mine_coords': [0, 0], 'img_id' : None, 'mask_id': None, 'block_wdgt': None, 'block_state': None}
             ],
             [
              {'mine': 0, 'mine_coords': [0, 0], 'img_id' : None, 'mask_id': None, 'block_wdgt': None, 'block_state': None},
              {'mine': 0, 'mine_coords': [0, 0], 'img_id' : None, 'mask_id': None, 'block_wdgt': None, 'block_state': None},
              {'mine': 0, 'mine_coords': [0, 0], 'img_id' : None, 'mask_id': None, 'block_wdgt': None, 'block_state': None}
             ],
             [
              {'mine': 0, 'mine_coords': [0, 0], 'img_id' : None, 'mask_id': None, 'block_wdgt': None, 'block_state': None},
              {'mine': 0, 'mine_coords': [0, 0], 'img_id' : None, 'mask_id': None, 'block_wdgt': None, 'block_state': None},
              {'mine': 0, 'mine_coords': [0, 0], 'img_id' : None, 'mask_id': None, 'block_wdgt': None, 'block_state': None}
             ]
            ]
    """
    def __init__(self, field_size):
        self.field_size = field_size
        self.field = self.generate_field(self.field_size)

    def generate_field(self, size=None):
        """generate_field() - Generate a clean field data structure"""
        # Set default field size
        if not size:
            size = self.field_size
        
        self.field = []
        row = []
        for y in range(size):
            for x in range(size):
                row.append({'mine': 0, 
                    'mine_coords': [0, 0], 
                    'img_id' : None, 
                    'mask_id': None, 
                    'block_wdgt': None, 
                    'block_state': None})
            self.field.append(row)
            row = []
        
        return self.field

    def reset_field(self):
        self.generate_field()
        
        return True

    def place_mine(self, x, y):
        """ Place a single mine in the provided field area"""
        try:
            # Attempt mine assignment, IndexError on issue
            self.field[y][x]['mine'] = 9
            # Update coordinates
            self.field[y][x]['mine_coords'] = [y, x]
            
        except IndexError:
            raise IndexError("Minefield_Obj -> place_mine(): list index out of range")
            
        return True

    def in_field(self, x, y):
        """ If the coords are within the field matrix, True; False otherwise"""
        if y < 0 or y > len(self.field):
            return False
            
        if x < 0 or x > len(self.field[0]):
            return False
            
        return True

    def is_mine(self, x, y):
        if self.field[y][x]['mine'] == 9:
            return True
        else:
            return False

    def is_blank(self, x, y):
        if self.field[y][x]['block_state'] == 'blank':
            return True
        else:
            return False

    def is_flag(self, x, y):
        if self.field[y][x]['block_state'] == 'flag':
            return True
        else:
            return False

    def is_question(self, x, y):
        if self.field[y][x]['block_state'] == 'question':
            return True
        else:
            return False


class MineSweeper:
    """ MineSweeper - GUI / Game Logic Class
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

        # The Minefield 
        self.mf = Minefield_Obj(self.field_size)

        # Mine Border Calc - DO NOT CHANGE
        self.mine_border = 4
        
        # Field dimensions
        self.field_width = self.mine_pxs * self.field_size
        self.field_height = self.field_width
        
        # Field adjusted border
        self.field_width_bd = self.field_width + (self.mine_border * 2)
        self.field_height_bd = self.field_width_bd
        
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
            
            self.field_obj_menu = tk.Menu(self.menubar, tearoff=0)
            self.field_obj_menu.add_command(label="print_fieldObj_info()", command=self.print_fieldObj_info)
            self.field_obj_menu.add_command(label="print_fieldObj()", command=self.print_fieldObj)
            self.field_obj_menu.add_command(label="generate_field()", command=self.mf.generate_field)
            self.field_obj_menu.add_command(label="reset_field()", command=self.mf.reset_field)
            self.field_obj_menu.add_command(label="delete_thing()", command=self.delete_thing)
            self.field_obj_menu.add_command(label="is_thing()", command=self.is_thing)
            self.menubar.add_cascade(label="Field Obj", menu=self.field_obj_menu)
            
            self.field_menu = tk.Menu(self.menubar, tearoff=0)
            self.field_menu.add_command(label="place_mines()", command=self.place_mines)
            self.field_menu.add_command(label="place_mines() loop", command=self.gen_loop)
            self.field_menu.add_separator()
            self.field_menu.add_command(label="analyze_field()", command=self.analyze_field)
            self.field_menu.add_command(label="draw_field()", command=self.draw_field)
            self.field_menu.add_command(label="mask_field()", command=self.mask_field)
            self.field_menu.add_command(label="draw_blocks()", command=self.draw_blocks)
            self.field_menu.add_command(label="clear_field()", command=self.clear_field)

            self.field_menu.add_separator()
            self.field_menu.add_command(label="clear_img_ids()", command=self.clear_img_ids)
            self.field_menu.add_command(label="clear_mask_ids()", command=self.clear_mask_ids)
            self.field_menu.add_command(label="clear_blocks()", command=self.clear_blocks)
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
        self.mine_face.bind("<ButtonPress-1>", self.mine_face_press)
        self.mine_face.bind("<ButtonRelease-1>", self.mine_face_release)

    def mine_face_press(self, event=None):
        self.mine_face.config(image=self.smile_face_pressed)
        pass

    def mine_face_release(self, event=None):
        self.mine_face.config(image=self.smile_face)
        pass

    def minefield_btn1_press(self, event=None):
        if debug:
            print("btn1_press")
        
        event.widget.config(image="")

        self.mine_face.config(image=self.wow_face)

    def minefield_btn1_release(self, event=None):
        if debug:
            print("btn1_release")
        
        # Delete the field mask
        # TODO: Branch this to its own method?
        yx = event.widget.yx_strap
        self.minefield.delete(self.mf.field[yx[0]][yx[1]]['mask_id'])
        event.widget.destroy()
        
        self.mine_face.config(image=self.smile_face)

    def minefield_btn3_press(self, event=None):
        if debug:
            print("btn3_press")
        
    def minefield_btn3_release(self, event=None):
        if debug:
            print("btn3_release")
        
    def right_press(self, event=None):
        pass

    def right_release(self, event=None):
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
    def place_blocks(self):
        pass

    def mask_field(self):
        """ Overlay 0.gif #C0C0C0 block image over every field element that has
            space occupied. That way the field element won't be visible until 
            mouse click is _released. Removed in minefield_release"""
        # Offset image by 16px
        x_offset, y_offset = 1, 1
        
        # Iterate, create, and assign our mask img's / id's
        for y in range(len(self.mf.field)):
            for x in range(len(self.mf.field[y])):
                iid = self.minefield.create_image(x_offset, y_offset, 
                    image=self.mine_nums[0], anchor="nw")
                self.mf.field[y][x]['mask_id'] = iid
                
                x_offset += self.mine_pxs
               
            x_offset = 1
            y_offset += self.mine_pxs

        return True
        
    def place_mines(self):
        """ place_mines() - Randomly generate and assing mines to the field""" 
        # Iterate over the required mine quantity
        for i in range(self.mines):
            # Generate random mine location
            y = random.randrange(0, self.field_size - 1)
            x = random.randrange(0, self.field_size - 1)
            # If duplicate location, regenerate until not
            while self.mf.is_mine(x, y):
                y = random.randrange(0, self.field_size - 1)
                x = random.randrange(0, self.field_size - 1)

            # Place the generated mine
            self.mf.place_mine(x, y)
            
        return True

    def analyze_field(self):
        for y in range(len(self.mf.field)):
            for x in range(len(self.mf.field)):
                if self.mf.is_mine(x, y):
                    if debug:
                        print(f"DEBUG: analyze_field(): x:{x} y:{y} is_mine: {self.mf.is_mine(x, y)}")

                    ## Previous Row
                    # Up and Left
                    if not self.mf.is_mine(x-1, y-1) and self.mf.in_field(x-1, y-1):
                        self.mf.field[y-1][x-1]['mine'] += 1
                        
                    # Up
                    if not self.mf.is_mine(x, y-1) and self.mf.in_field(x, y-1):
                        self.mf.field[y-1][x]['mine'] += 1
                 
                    # Up and Right
                    if not self.mf.is_mine(x+1, y-1) and self.mf.in_field(x+1, y-1):
                        self.mf.field[y-1][x+1]['mine'] += 1
                    
                    ## Mine Row
                    # Left
                    if not self.mf.is_mine(x-1, y) and self.mf.in_field(x-1, y):
                        self.mf.field[y][x-1]['mine'] += 1
                        
                    # Right
                    if not self.mf.is_mine(x+1, y) and self.mf.in_field(x+1, y):
                        self.mf.field[y][x+1]['mine'] += 1
                    
                    ## Next Row
                    # Down and Left
                    if not self.mf.is_mine(x-1, y+1) and self.mf.in_field(x-1, y+1):
                        self.mf.field[y+1][x-1]['mine'] += 1
                        
                    # Down
                    if not self.mf.is_mine(x, y+1) and self.mf.in_field(x, y+1):
                        self.mf.field[y+1][x]['mine'] += 1
                        
                    # Down and Right
                    if not self.mf.is_mine(x+1, y+1) and self.mf.in_field(x+1, y+1):
                        self.mf.field[y+1][x+1]['mine'] += 1

    def sweep_field(self):
        pass

    def draw_field(self):
        img_src = None
        
        # #C0C0C0 1px border edge only on the NW edge of minefield, offset by 1
        field_x, field_y = 1, 1
        
        # Set what image needs drew
        for y in range(len(self.mf.field)):
            for x in range(len(self.mf.field)):
            
                # Handle proper image assignment per field analysis
                if self.mf.field[y][x]['mine'] == 9:
                    img_src = self.mine
                    
                elif self.mf.field[y][x]['mine'] == 1:
                    img_src = self.mine_nums[1]
                    
                elif self.mf.field[y][x]['mine'] == 2:
                    img_src = self.mine_nums[2]
                    
                elif self.mf.field[y][x]['mine'] == 3:
                    img_src = self.mine_nums[3]
                    
                elif self.mf.field[y][x]['mine'] == 4:
                    img_src = self.mine_nums[4]
                    
                elif self.mf.field[y][x]['mine'] == 5:
                    img_src = self.mine_nums[5]
                    
                elif self.mf.field[y][x]['mine'] == 6:
                    img_src = self.mine_nums[6]
                    
                elif self.mf.field[y][x]['mine'] == 7:
                    img_src = self.mine_nums[7]
                    
                elif self.mf.field[y][x]['mine'] == 8:
                    img_src = self.mine_nums[8]

                # Blank #C0C0C0 background, do nothing
                else:
                    img_src = False
                    
                    
                # If not default, create and assign field image
                if img_src:
                    iid = self.minefield.create_image(field_x, field_y, 
                        image=img_src, anchor="nw")
                    print(iid)
                    self.mf.field[y][x]['img_id'] = iid
                
                # Offset x
                field_x += self.mine_pxs
            
            # Reset x and offset y
            field_x = 1
            field_y += self.mine_pxs

    def clear_field(self):
        """ Reset all values in minefield matrix and draw empty field"""
        for y in range(len(self.mf.field)):
            for x in range(len(self.mf.field[y])):
                # Clear minefield images
                if self.mf.field[y][x]['img_id'] != None:
                    self.minefield.delete(self.mf.field[y][x]['img_id'])
                    self.mf.field[y][x]['img_id'] = None
                
                # Clear mask images
                if self.mf.field[y][x]['mask_id'] != None:
                    self.minefield.delete(self.mf.field[y][x]['mask_id'])
                    self.mf.field[y][x]['mask_id'] = None
                
                # Destroy block elements
                if self.mf.field[y][x]['block_wdgt'] != None:
                    self.mf.field[y][x]['block_wdgt'].destroy()
                    self.mf.field[y][x]['block_wdgt'] = None
        
        # Reset minefield matrix
        self.mf.reset_field()
        
        return True

    def draw_blocks(self):
        ## Blocks overlap minefield border by 1px on NW side, so index by 0
        # Canvas/Button place offset
        field_x, field_y = 0, 0
        
        for y in range(len(self.mf.field)):
            for x in range(len(self.mf.field[y])):
                # Create blank img button and place() it on canvas
                self.mf.field[y][x]['block_wdgt'] = tk.Label(self.minefield, 
                    image=self.blank_block, highlightthickness=0, bd=0)
                self.mf.field[y][x]['block_wdgt'].place(x=field_x, y=field_y)
                
                # Widget-strap our field coordinates 
                self.mf.field[y][x]['block_wdgt'].yx_strap = [y, x]
                
                ## Bind the event handlers
                # Block Left click Press and Release events
                self.mf.field[y][x]['block_wdgt'].bind("<ButtonPress-1>", 
                    self.minefield_btn1_press)
                self.mf.field[y][x]['block_wdgt'].bind("<ButtonRelease-1>", 
                    self.minefield_btn1_release)
                    
                # Block Right click Press and Release events
                self.mf.field[y][x]['block_wdgt'].bind("<ButtonPress-3>", 
                    self.minefield_btn3_press)
                self.mf.field[y][x]['block_wdgt'].bind("<ButtonRelease-3>", 
                    self.minefield_btn3_release)
                
                # Offset x
                field_x += self.mine_pxs
            
            field_x = 0
            field_y += self.mine_pxs

    def mainloop(self):
        self.root.mainloop()

    """ DEBUG METHODS """
    # Field Object Menu
    def print_fieldObj_info(self):
        black = "\33[30m"
        red = "\33[31m"
        green = "\33[32m"
        yellow = "\33[33m"
        blue = "\33[34m"
        magenta = "\33[35m"
        cyan = "\33[36m"
        white = "\33[37m"
        
        # Print clean Field Matrix
        print("Minefield Matrix:")
        for y in range(len(self.mf.field)):
            for x in range(len(self.mf.field[y])):
                print("[", end="")
                if self.mf.field[y][x]['mine'] == 9:
                    print("\33[31m" + "x" + "\33[0m", end="")
                
                # Colorize the numerics
                else:
                    num = self.mf.field[y][x]['mine']
                    if num == 1:
                        color = blue
                    elif num == 2:
                        color = green
                    elif num == 3:
                        color = red
                    elif num == 4:
                        color = yellow
                    elif num == 5:
                        color = magenta
                    elif num == 6:
                        color = cyan
                    elif num == 7:
                        color = black
                    elif num == 8:
                        color = white
                    else:
                        color = ""
                        
                    print(f"{color}{self.mf.field[y][x]['mine']}\33[0m", end="")
                    #print(self.mf.field[y][x]['mine'], end="")
                print("]", end="")
                
            print()
            
    def print_fieldObj(self):
        for y in range(len(self.mf.field)):
            print(f"Column: {y}")
            for x in range(len(self.mf.field)):
                print(f"Row: {x} - {self.mf.field[y][x]}")
            
            print()
        
    def delete_thing(self):
        pass
        
    def is_thing(self):
        pass

    def gen_loop(self):
        self.place_mines()
        self.analyze_field()
        self.print_fieldObj_info()
        self.mf.reset_field()
        
        self.root.after(5000, self.gen_loop)
        
    def clear_img_ids(self):
        for y in range(len(self.mf.field)):
            for x in range(len(self.mf.field[y])):
                self.minefield.delete(self.mf.field[y][x]['img_id'])
                self.mf.field[y][x]['img_id'] = None
                
        return True

    def clear_mask_ids(self):
        for y in range(len(self.mf.field)):
            for x in range(len(self.mf.field[y])):
                self.minefield.delete(self.mf.field[y][x]['mask_id'])
                self.mf.field[y][x]['mask_id'] = None
                
        return True
        
    def clear_blocks(self):
        for y in range(len(self.mf.field)):
            for x in range(len(self.mf.field[y])):
                self.mf.field[y][x]['block_wdgt'].destroy()
                self.mf.field[y][x]['block_wdgt'] = None
                
        return True


if __name__ == "__main__":
    ms = MineSweeper()