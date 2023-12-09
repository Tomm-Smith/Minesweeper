import tkinter as tk


class test:
    def __init__(self):
        self.root = tk.Tk()
       
        self.__gui__()
        
    def __gui__(self):
        ### ScoreBoard ###
        self.scoreboard_frm = tk.Frame(self.root, highlightthickness=0)
        self.scoreboard_frm.pack(side="bottom")
        
        self.scoreboard = tk.Canvas(self.scoreboard_frm, width=150,
            height=150, highlightthickness=0, background="orange")
        self.scoreboard.pack()
        
        # Proper offset x19 y11
        self.mine_cnt = tk.Canvas(self.scoreboard, height=23, width=39,
            highlightthickness=0, background="yellow")
        self.scoreboard.create_window(1, 1, anchor="nw", window=self.mine_cnt)
        
    def mainloop(self):
        self.root.mainloop()
        
        
if __name__ == "__main__":
    t = test()
    t.mainloop()