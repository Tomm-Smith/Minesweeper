import tkinter as tk
import random

global debug
debug = 0


class MineSweeper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("164x222")
        if debug:
            self.root.attributes('-alpha', 1)
        
        # TODO: Incorporate border offset for canvas border drawing
        # in canvas area
        self.minefield_border = 0
        self.canvas_offset = 9
        
        self.mine_pxs = 16
        self.grid_size = 9
        
        self.sweep_width = self.mine_pxs * self.grid_size
        self.sweep_height = self.sweep_width
        
        
        self.__gui__()
        self.draw_grid()
        self.draw_blocks()
        #self.draw_mines(1)
        
    def __gui__(self):
        self.minefield = tk.Canvas(self.root, 
            width=self.sweep_width, height=self.sweep_height,
            borderwidth=self.minefield_border, relief="sunken")
        self.minefield.pack(side="top", fill="none", expand=False)
        
    def __events__(self):
        pass
        
    def field_click(self, indx):
        print(indx)
        self.field_btns[indx].destroy()
        
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
        self.img = tk.PhotoImage(file=r"C:\Users\rootp\Documents\Code\Python\GUI\Minesweeper\img\blank_block.gif")
        if debug:
            self.minefield.create_image(9,9, image=self.img)
            self.minefield.create_image(25,9, image=self.img)
            #self.minefield.create_image(27,28, image=self.img)
            #self.minefield.create_image(36, 36, image=self.img)
            return 0
        
        # Cover mine field with blocks
        self.field_btns = [n for n in range(self.grid_size * self.grid_size)]
        # Canvas/Button place offset
        field_x, field_y = 1, 1
        step=0
        
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                # Create blank img button
                self.field_btns[step] = tk.Button(self.root, image=self.img, 
                    command=lambda step=step: self.field_click(step), 
                    highlightthickness=0, bd=0)
                # Place blank block
                self.field_btns[step].place(x=field_x + self.canvas_offset, 
                    y=field_y)
                # Offset x
                field_x += self.mine_pxs
                step += 1
                
            field_x = 1
            field_y += self.mine_pxs
                
    def place_image(self, img):
        pass
        
    def draw_mines(self, qty):
        self.img = tk.PhotoImage(file=r"C:\Users\rootp\Documents\Code\Python\GUI\Minesweeper\img\bomb.gif")

        if debug:
            lbl = tk.Label(self.root, image=self.img, highlightthickness=0, bd=0)
            lbl.place(x=self.canvas_offset + 1, y=2)
            
            lbl = tk.Label(self.root, image=self.img, highlightthickness=0, bd=0)
            lbl.place(x=self.canvas_offset + 1, y=2)

            pass
        
        #mines = [n for n in range(qty)]
        
        #for i in range(0, qty):
        #    x = random.randrange(0, self.grid_size+1, 1) * self.mine_pxs
        #    y = random.randrange(0, self.grid_size+1, 1) * self.mine_pxs
            
        #    mines[i] = self.img 
        #    mines[i].place
        
        
        
        
    def mainloop(self):
        self.root.mainloop()
        
        
if __name__ == "__main__":
    ms = MineSweeper()
    ms.mainloop()