
import tkinter as tk



class MineSweeper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.columnconfigure(0, weight=1)
        
        self.__gui__()
        
    def __gui__(self):
        top_area = tk.Frame(self.root, bg="#c0c0c0", relief=tk.SUNKEN, borderwidth=2)
        top_area.pack(side="top", fill=tk.X, expand=False)
        
        #mine_frm = tk.Frame(top_area)
        #mine_frm.pack(side="left")
        
        mine_cnt = tk.Canvas(top_area, width=39, height=23, 
                             background="#000000", borderwidth=2, relief=tk.SUNKEN)
        mine_cnt.pack(side="left", anchor="center")
        
        #smile_frm = tk.Frame(top_area)
        #smile_frm.pack()
        
        btn = tk.Button(top_area, text="   ")
        btn.pack(anchor="center")
        
        #timer_frm = tk.Frame(top_area)
        #timer_frm.pack(side="right")
        
        timer = tk.Canvas(top_area, width=39, height=23, 
                     background="#000000", borderwidth=2, relief=tk.SUNKEN)
        timer.pack(side="right", anchor="center")
        
#def __events__(self):
    
    
    
if __name__ == "__main__":
    MineSweep = MineSweeper()
    MineSweep.root.mainloop()