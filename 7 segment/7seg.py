import tkinter as tk
import time



class seg:
    def __init__(self):
        self.root = tk.Tk()
        
        self.img = [0 for i in range(10)]
        self.img[0] = tk.PhotoImage(file=r".\7_segment\0.gif")
        self.img[1] = tk.PhotoImage(file=r".\7_segment\1.gif")
        self.img[2] = tk.PhotoImage(file=r".\7_segment\2.gif")
        self.img[3] = tk.PhotoImage(file=r".\7_segment\3.gif")
        self.img[4] = tk.PhotoImage(file=r".\7_segment\4.gif")
        self.img[5] = tk.PhotoImage(file=r".\7_segment\5.gif")
        self.img[6] = tk.PhotoImage(file=r".\7_segment\6.gif")
        self.img[7] = tk.PhotoImage(file=r".\7_segment\7.gif")
        self.img[8] = tk.PhotoImage(file=r".\7_segment\8.gif")
        self.img[9] = tk.PhotoImage(file=r".\7_segment\9.gif")
        
        
        
        
        self.__gui__()

    def __gui__(self):
        self.frame = tk.Frame(self.root, background="#000000")
        self.frame.pack(side="bottom")
    
        self.display = tk.Canvas(self.frame, width=100, height=100,
            highlightthickness=0, borderwidth=0, bd=0, background="#ffffff")
        self.display.pack(side="bottom")
        
        
        self.left =  self.display.create_image(0, 1, image=self.img[1])
        self.middle = self.display.create_image(13, 0, image=self.img[1])
        self.right = self.display.create_image(26, 0, image=self.img[2])
        
        self.update_display(100)
        
    def update_display(self, num):
        try:
            int(num)
        except ValueError:
            raise ValueError("update_display only accepts int type")
            
        if len(str(num)) > 999:
            num = 999
            
        num_str = str(num)
        num_slice = [int(num_str[0]), int(num_str[1]), int(num_str[2])]
        
        self.display.delete(self.left)
        self.left = self.display.create_image(10, 20, image=self.img[num_slice[0]])
        
        self.display.delete(self.middle)
        self.middle = self.display.create_image(23, 20, image=self.img[num_slice[1]])
        
        self.display.delete(self.right)
        self.right = self.display.create_image(36, 20, image=self.img[num_slice[2]])
        
        

if __name__ == "__main__":
    ss = seg()
    ss.root.mainloop()