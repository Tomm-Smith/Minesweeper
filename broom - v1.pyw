"""
Minesweeper - A game for mine janitors.
"""


import tkinter as tk
import os
import random
import math

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
            'tag_id': None,
            'mask': None,
            'block_state': None}


    Structure Reference:
        mine:        - 9   - mine
                     - 0   - Empty
                     - 1-8 - Mine Proximity
        mine_coords: - [x, y] coordinates for mine location on field
        img_id:      - Image id of item on the minefield, None otherwise
        tag_id:     - Numeric ID of instantiated mask image hiding the mines
                       until click_release, None otherwise
        mask:       - iid of mask image, None otherwise
        block_state: - State of Field Block, EG. 'blank', 'flag', 'question'
        
     TODO: - Restructure data structure so that referencing is done by [x][y] 
            not [y][x]
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
                    'tag_id': None, 
                    'block_wdgt': None, 
                    'block_state': 'blank'})
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
        self.root.geometry("164x160+186+725")
        
        if debug:
            self.root.attributes('-alpha', 1)



        """ 
        Image objects
        """
        path = os.getcwd()

        # Mine cover blocks
        self.blank_block = tk.PhotoImage(file=fr"{path}\img\blank_block.gif")
        self.flag_block = tk.PhotoImage(file=fr"{path}\img\flag.gif")
        self.question_block = tk.PhotoImage(file=fr"{path}\img\question.gif")
        
        # Mine blocks. ...not yours!
        self.mine = tk.PhotoImage(file=fr"{path}\img\bomb.gif")
        self.mine_clicked = tk.PhotoImage(file=fr"{path}\img\bomb_clicked.gif")
        self.mine_wrong = tk.PhotoImage(file=fr"{path}\img\bomb_wrong.gif")
        
        # Mask
        self.mask = tk.PhotoImage(file=fr"{path}\img\field_numbers\mask.gif")
        
        # MineField numbers
        self.mine_nums = [n for n in range(10)]
        self.mine_nums[0] = tk.PhotoImage(file=fr"{path}\img\field_numbers\0.gif")
        self.mine_nums[1] = tk.PhotoImage(file=fr"{path}\img\field_numbers\1.gif")
        self.mine_nums[2] = tk.PhotoImage(file=fr"{path}\img\field_numbers\2.gif")
        self.mine_nums[3] = tk.PhotoImage(file=fr"{path}\img\field_numbers\3.gif")
        self.mine_nums[4] = tk.PhotoImage(file=fr"{path}\img\field_numbers\4.gif")
        self.mine_nums[5] = tk.PhotoImage(file=fr"{path}\img\field_numbers\5.gif")
        self.mine_nums[6] = tk.PhotoImage(file=fr"{path}\img\field_numbers\6.gif")
        self.mine_nums[7] = tk.PhotoImage(file=fr"{path}\img\field_numbers\7.gif")
        self.mine_nums[8] = tk.PhotoImage(file=fr"{path}\img\field_numbers\8.gif")
        self.mine_nums[9] = tk.PhotoImage(file=fr"{path}\img\field_numbers\marker.gif")
        
        """
        sweep_field() Elements
        """
        self.block_click = [None, None]
        self.field_tag = []
        
        """
        Environment elements
        """
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
            self.help.add_command(label="About Minesweeper...", command="")
            self.menubar.add_cascade(label="Help", menu=self.help)
            """ Help Dialog:
                - EasterEgg?
                - It aslways seems impossible until it's done. - Nelson Mandela
            """
        
        if debug:
            self.debug = tk.Menu(self.menubar, tearoff=0)
            self.debug.add_command(label="analyze_sweep()", command=self.analyze_sweep)
            self.debug.add_separator()
            self.debug.add_command(label="reset_game()", command=self.reset_game)

            self.menubar.add_cascade(label="Debug", menu=self.debug)
            
            self.field_obj_menu = tk.Menu(self.menubar, tearoff=0)
            self.field_obj_menu.add_command(label="print_fieldObj_info()", command=self.print_fieldObj_info)
            self.field_obj_menu.add_command(label="print_fieldObj()", command=self.print_fieldObj)
            self.menubar.add_cascade(label="Field Obj", menu=self.field_obj_menu)
            
            self.field_menu = tk.Menu(self.menubar, tearoff=0)
            self.field_menu.add_command(label="place_mines()", command=self.place_mines)
            self.field_menu.add_command(label="analyze_field()", command=self.analyze_field)
            self.field_menu.add_separator()
            self.field_menu.add_command(label="draw_field()", command=self.draw_field)
            self.field_menu.add_command(label="clear_field()", command=self.clear_field)
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

    """ Event Handling Methods """
    def __events__(self):
        self.minefield.bind("<Button-1>", self.minefield_Button1)
        self.minefield.bind("<Control-Button-1>", self.minefield_ctrl_Button1)
        self.minefield.bind("<Button-3>", self.minefield_tag)
        
    def minefield_tag(self, event=None):
        """ Add a tag identifier to the minefield for analyze_sweep() debug
        routines. Gist is, you right click a field slot and it lays an 
        identifier that analyse_sweep() will begin from. Allowing for viewing
        of the sweep pattern.
        
        #TODO: Break this up into methods as to simplify code"""
        print(f"minefield_tag(): x{event.x} y{event.y}")
        
        # Calculate the click area on Minefield canvas down to the array
        # coordinates and round down to whole number
        x = math.floor(event.x / self.mine_pxs)
        y = math.floor(event.y / self.mine_pxs)
        
        # Calculate the relative 0,0 position for the image placement 
        # withing the grid layout
        gx = self.mine_pxs * x + 1
        gy = self.mine_pxs * y + 1
        
        # Create tag
        if self.field_tag == []:
            iid = self.minefield.create_image(gx, gy, image=self.mine_nums[9], 
                anchor="nw")
            self.mf.field[y][x]['tag_id'] = iid
            self.field_tag = [x, y]
        
        # Delete old tag and create new one
        elif self.field_tag != [x,y]:
            self.minefield.delete(self.mf.field[self.field_tag[1]]
                                               [self.field_tag[0]]['tag_id'])
            iid = self.minefield.create_image(gx, gy, image=self.mine_nums[9], 
                anchor="nw")
            self.mf.field[y][x]['tag_id'] = iid
            self.field_tag = [x, y]
        
        # Remove tag
        else:
            self.minefield.delete(self.mf.field[y][x]['tag_id'])
            self.mf.field[y][x]['tag_id'] = None
            self.field_tag = []
    
    def minefield_Button1(self, event=None):
        """ Place analysis number on the field and allow for 
        left clicking through the number array, 0-9
        
        TODO: Disperse this method and minefield_ctrl_Button1()
        into a single coord method, then specific image manipulation"""
        
        # Turn field click area into mf.field[yx]
        fld_xy = self.field_click_grid_xy(event.x, event.y)
        print(f"fld_xy: {fld_xy}")
        # Get image 0,0 for relative top let corner placement
        img_xy = self.field_click_img_xy(event.x, event.y)
        print(f"img_xy: {img_xy}")
        # Keep every click on a series of rolling 8, increment by 1
        mine = self.mf.field[fld_xy[1]][fld_xy[0]]['mine']
        mine = (mine + 1) % 9
        
        # Assign our increment
        self.mf.field[fld_xy[1]][fld_xy[0]]['mine'] = mine
        
        # Delete existing image
        self.minefield.delete(self.mf.field[fld_xy[1]][fld_xy[0]]['img_id'])
        
        # Draw new
        iid = self.minefield.create_image(img_xy[0], img_xy[1], 
            image=self.mine_nums[mine], anchor="nw")
        self.mf.field[fld_xy[1]][fld_xy[0]]['img_id'] = iid
        
    def minefield_ctrl_Button1(self, event=None):
        """ Place mine on selected field slot
        
        TODO: Disperse this method and minefield_Button1_Press()
        into a single coord method, then specific image manipulation"""
        
        # Turn field click area into mf.field[yx]
        fld_xy = self.field_click_grid_xy(event.x, event.y)
        print(f"fld_xy: {fld_xy}")
        # Get image 0,0 for relative top let corner placement
        img_xy = self.field_click_img_xy(event.x, event.y)
        print(f"img_xy: {img_xy}")

        
        # Place mine in field object
        if self.mf.field[fld_xy[1]][fld_xy[0]]['mine'] == 9:
            self.mf.field[fld_xy[1]][fld_xy[0]]['mine'] = 0
            img = self.mine_nums[0]
        else:
            self.mf.field[fld_xy[1]][fld_xy[0]]['mine'] = 9
            img = self.mine
            
        # Delete existing image
        self.minefield.delete(self.mf.field[fld_xy[1]][fld_xy[0]]['img_id'])
        
        # Draw new
        iid = self.minefield.create_image(img_xy[0], img_xy[1], 
            image=img, anchor="nw")
        self.mf.field[fld_xy[1]][fld_xy[0]]['img_id'] = iid
    
    """ UI Coordinate Methods """
    def field_click_grid_xy(self, x, y):
        """ Convert field click coordinates into the respective array slots 
        in Minefield_Obj"""
        x_ = math.floor(x / self.mine_pxs)
        y_ = math.floor(y / self.mine_pxs)
        
        return [x_, y_]
        
    def field_click_img_xy(self, x, y):
        """ Convert a click point into a relative 0,0 coordinate 
        of the top left corner in our destination field grid.
        Used for placement of image in a specific field slot"""
        xy = self.field_click_grid_xy(x, y)
        
        # Multiple the array numerics by the field block pixel size to get
        # the 0,0 index of the top left corner of area
        x_ = xy[0] * self.mine_pxs + 1
        y_ = xy[1] * self.mine_pxs + 1
        
        return [x_, y_]
    
    """ Drawing Methods """
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

    """ Field Methods """
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
                
                # Clear minefield tags
                if self.mf.field[y][x]['tag_id'] != None:
                    self.minefield.delete(self.mf.field[y][x]['tag_id'])
                
                # Destroy block elements
                if self.mf.field[y][x]['block_wdgt'] != None:
                    self.mf.field[y][x]['block_wdgt'].destroy()
                    self.mf.field[y][x]['block_wdgt'] = None
        
        # Reset minefield matrix
        self.mf.reset_field()
        
        return True

    """ Field Sweep Methods """
    def set_mask(self, x, y):
        """ Set a mask overlay on a swept block for diagnostic troubleshooting
        
        Pretty crude, this method infers first run on a clean field with no 
        prior sweep masks. TODO: Fix this.
        """
        iid = self.minefield.create_image(x, y, self.mask)
        self.mf.field[y][x]['mask'] = iid
    
    def analyze_sweep(self):
        if self.field_tag == []:
            print("DEBUG: analyze_sweep(): tag bit coordinates are not set.")
            return False
        
        # The list that will be swept after analysis, all entrys are stored 
        # as coordinate list's in the form .append([x, ])
        sweep_list = []
        
        # The current float position of sweeping through field
        x, y = self.field_tag[0], self.field_tag[1]
        
        # Ensure the field is empty
        if self.mf.field[y][x]['mine'] != None:
            print("DEBUG: analyq_sweep(): field slot not empty, nothing to sweep")
            return False
        
        
        # Begin our sweeping steps through the field, revealing the analysis 
        # numerics as our field continent (surrounding the blank ocean)
        if self.mf.field[y-1][x-1] != None:
            pass
            # reveal
        
        
        
        
    def sweep_field(self):
        pass

    def reset_game(self):
        """ Reset the game"""
        self.clear_field()
        
        
        ## DO NOT CHANGE ORDER ##
        # Order is specific for the purpose of image layers and which is 
        # on top/bottom
        self.place_mines()
        self.analyze_field()
        self.draw_field()
        #self.draw_blocks()

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
        print("    0  1  2  3  4  5  6  7  8")
        for y in range(len(self.mf.field)):
            print(f" {y} ", end="")
            
            for x in range(len(self.mf.field[y])):
                # HiLight tag block brackets red
                if self.mf.field[y][x]['tag_id'] != None:
                    print(f"{red}[\33[0m", end="")
                else:
                    print("[", end="")
                
                # Replace mine with 'x' and colorize red
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
                    elif num == 9:
                        color = red
                    else:
                        color = ""
                    
                    # Display the grid element
                    print(f"{color}{self.mf.field[y][x]['mine']}\33[0m", end="")
                
                # Hilight tag block brackets red
                if self.mf.field[y][x]['tag_id'] != None:
                    print(f"{red}]\33[0m", end="")
                else:
                    print("]", end="")
                
            print()
            
    def print_fieldObj(self):
        for y in range(len(self.mf.field)):
            print(f"Row: {y}")
            for x in range(len(self.mf.field)):
                print(f"Column: {x} - {self.mf.field[y][x]}")
            
            print()


if __name__ == "__main__":
    ms = MineSweeper()