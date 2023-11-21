
import tkinter as tk



class MineSweeper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.__gui__()
        
    def __gui__(self):
        #display_frm = tk.Frame(self.root, relief=tk.SUNKEN, borderwidth=2)
        #display_frm.pack(side="top", fill=tk.X, expand=False)
    
        display_frm = tk.Canvas(self.root, height=400, width=400, background="#c0c0c0")
        display_frm.grid(row=0, columnspan=3)
    
        cnt_frm = tk.Frame(self.root)
        cnt_frm.grid(row=0, column=0, sticky="nw")
        
        mine_cnt = tk.Canvas(cnt_frm, width=39, height=23, 
                             background="#000000")
        mine_cnt.grid(row=0, column=0, sticky="nw")
        
        btn = tk.Button(self.root, text="   ")
        btn.grid(row=0, column=1, sticky="n")
        
        timer = tk.Canvas(self.root, width=39, height=23, 
                     background="#000000")
        timer.grid(row=0, column=2, sticky="ne")
    
    
    
if __name__ == "__main__":
    MineSweep = MineSweeper()
    MineSweep.root.mainloop()