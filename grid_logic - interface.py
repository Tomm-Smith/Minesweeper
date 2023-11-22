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
    NOTES:
        - Make sure the game reset destroy()'s all the button widgets/bindings
        - What's not your sweep? Minesweeper. 
        - What did the CEO call the janitor? MineSweeper.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        if debug:
            self.root.attributes('-alpha', 1)
        
        """ 
        Image objects
        """
        path = os.getcwd()
        
        # 7 Segment Display
        self.seg_0 = tk.PhotoImage(file=fr"{path}\img\7_segment\0.gif")
        self.seg_1 = tk.PhotoImage(file=fr"{path}\img\7_segment\1.gif")
        self.seg_2 = tk.PhotoImage(file=fr"{path}\img\7_segment\2.gif")
        self.seg_3 = tk.PhotoImage(file=fr"{path}\img\7_segment\3.gif")
        self.seg_4 = tk.PhotoImage(file=fr"{path}\img\7_segment\4.gif")
        self.seg_5 = tk.PhotoImage(file=fr"{path}\img\7_segment\5.gif")
        self.seg_6 = tk.PhotoImage(file=fr"{path}\img\7_segment\6.gif")
        self.seg_7 = tk.PhotoImage(file=fr"{path}\img\7_segment\7.gif")
        self.seg_8 = tk.PhotoImage(file=fr"{path}\img\7_segment\8.gif")
        self.seg_9 = tk.PhotoImage(file=fr"{path}\img\7_segment\9.gif")
        
        # Mine cover blocks
        self.blank_block = tk.PhotoImage(file=fr"{path}\img\blank_block.gif")
        self.flag_block = tk.PhotoImage(file=fr"{path}\img\flag.gif")
        self.question_block = tk.PhotoImage(file=fr"{path}\img\question.gif")
        
        # Mine blocks, not yours!
        self.mine = tk.PhotoImage(file=fr"{path}\img\bomb.gif")
        self.mine_clicked = tk.PhotoImage(file=fr"{path}\img\bomb_clicked.gif")
        self.mine_wrong = tk.PhotoImage(file=fr"{path}\img\bomb_wrong.gif")
        
        # Field numbers
        self.field_0 = tk.PhotoImage(file=fr"{path}\img\field_numbers\0.gif")
        self.field_1 = tk.PhotoImage(file=fr"{path}\img\field_numbers\1.gif")
        self.field_2 = tk.PhotoImage(file=fr"{path}\img\field_numbers\2.gif")
        self.field_3 = tk.PhotoImage(file=fr"{path}\img\field_numbers\3.gif")
        self.field_4 = tk.PhotoImage(file=fr"{path}\img\field_numbers\4.gif")
        self.field_5 = tk.PhotoImage(file=fr"{path}\img\field_numbers\5.gif")
        self.field_6 = tk.PhotoImage(file=fr"{path}\img\field_numbers\6.gif")
        self.field_7 = tk.PhotoImage(file=fr"{path}\img\field_numbers\7.gif")
        self.field_8 = tk.PhotoImage(file=fr"{path}\img\field_numbers\8.gif")
        
        """
        Environment elements
        """
        # TODO: Incorporate border offset for canvas border drawing
        # in canvas area. Is this offset due to inproper geometry()?
        self.minefield_border = 0
        
        self.mine_pxs = 16
        self.grid_size = 9
        
        self.x_padding = 9
        self.y_padding = 8
        
        self.grid_width = self.mine_pxs * self.grid_size
        self.grid_height = self.grid_width
        
        self.sweep_width = self.grid_width + (self.x_padding * 2)
        self.sweep_height = self.grid_height + (self.y_padding * 2)
        
        self.root.geometry(f"{self.sweep_width+self.x_padding}x" \
                           f"{self.sweep_height+self.y_padding}")
        self.root.minsize(self.sweep_width, self.sweep_height)
        
        
        """
        MineSweeper()
        """
        self.__gui__()
        self.draw_grid()
        self.draw_blocks()
        self.gen_field_matrix(9)
        
    def __gui__(self):
        self.stats = tk.Canvas(self.root, width=self.sweep_width, height=33)
        self.minefield = tk.Canvas(self.root, 
            width=self.sweep_width, height=self.sweep_height,
            borderwidth=0, bd=0, highlightthickness=0)
        self.minefield.pack(side="left", fill="none", expand=False)
        
    def __events__(self):
        pass
        
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

    def draw_grid(self):
        # Draw grid
        for n in range(self.grid_size):
            # Horizontal
            self.minefield.create_line(0, n * self.mine_pxs+1, 
                self.sweep_width-1, n * self.mine_pxs+1)
            # Vertical
            self.minefield.create_line(n * self.mine_pxs+1, 0, 
                n * self.mine_pxs+1, self.sweep_height-1)
            
    def draw_blocks(self):
        self.bblock = tk.PhotoImage(file=r"C:\Users\rootp\Documents\Code\Python\GUI\Minesweeper\img\blank_block.gif")
        if debug:
            self.minefield.create_image(9,9, image=self.bblock)
            self.minefield.create_image(25,9, image=self.bblock)
            self.minefield.create_image(27,28, image=self.bblock)
            self.minefield.create_image(36, 36, image=self.bblock)
            
            
        # Cover mine field with blocks
        self.field_btns = [n for n in range(self.grid_size * self.grid_size)]
        # Canvas/Button place offset
        field_x, field_y = self.x_padding+1, self.y_padding+1
        step=0
        
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                # Create blank img button
                self.field_btns[step] = tk.Label(self.root, image=self.bblock, 
                    highlightthickness=0, bd=0)
                    
                self.field_btns[step].id = step
                self.field_btns[step].bind("<Button-1>", self.field_click)
                self.field_btns[step].bind("<Button-3>", self.field_flag_click)
                self.field_btns[step].flag = 0
                                
                
                self.field_btns[step].place(x=field_x, 
                    y=field_y)
                # Offset x
                field_x += self.mine_pxs
                step += 1
                
            field_x = 1
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