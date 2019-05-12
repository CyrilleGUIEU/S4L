import tkinter as tk
import os

import pyperclip
import mss
import keyboard 
from PIL import Image, ImageTk

KEYNAME="impr.ecran"
FILEPREFIX="figure"
FILEFORMAT=".png"
NBDIGITS=3
PATHLATEX="images/"
PREFIXLATEX= r"\begin{center}\includegraphics[scale=0.7]{"
SUFFIXLATEX= r"}\end{center}"

IMAGETEMP="cap-temp.png"

WIDTH=mss.mss().monitors[1]['width']
HEIGHT=mss.mss().monitors[1]['height']

app = tk.Tk()

        
class GUI:
    def __init__(self, app):
        self.app = app
        self.app.attributes('-topmost', True)
        self.app.attributes('-fullscreen', 1)


        self.isCapturing=False

        print("""S4L is now running ...
    1. Reduce the window
    2. Press '"""+KEYNAME+"'"+
    """
    3. Select a rectangle in the frozen screen
    4. Paste the paper clip in your Latex code editor
    5. Go back to step 2 if necessary
          """)
        app.bind_all('<ButtonRelease-1>', self.hideWindow)
        self.app.bind_all('<Button-1>', self.createRectangle)
        self.app.bind_all('<B1-Motion>', self.modifyRectangle)

        while True:
            if keyboard.is_pressed(KEYNAME) and self.isCapturing==False:
                self.isCapturing=True
                capture=mss.mss()
                capture.shot(output=IMAGETEMP)
                capture.close()
                self.image = Image.open(IMAGETEMP)
                self.canvas = tk.Canvas(self.app,width=WIDTH, height=HEIGHT, bg='black',cursor='crosshair')
                self.canvas.photo = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(00, 00, image=self.canvas.photo, anchor=tk.NW)
                self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
                self.app.state('normal')
                self.app.mainloop()
                try:
                    self.canvas.destroy()
                except NameError:
                    pass

    def hideWindow(self,event):
        self.app.state('withdrawn')
        self.app.quit()
        self.isCapturing=False
        self.Ax,self.Bx=min(self.Ax,event.x),max(self.Ax,event.x)
        self.Ay,self.By=min(self.Ay,event.y),max(self.Ay,event.y)
        capture=self.image.crop((self.Ax,self.Ay,self.Bx,self.By))
        n=0
        while True:
            try:
                file_name=FILEPREFIX+"0"*(NBDIGITS-len(str(n)))+str(n)+FILEFORMAT
                f=open(file_name)
                f.close()
                n=n+1
            except FileNotFoundError:
                break
        capture.save(file_name)
        capture.close()
        commandLatex=PREFIXLATEX+PATHLATEX+file_name+SUFFIXLATEX    
        pyperclip.copy(commandLatex)
        os.remove(IMAGETEMP)
        print("Screenshot saved in: "+file_name)
        print("Clipboard contains :"+commandLatex)
    def createRectangle(self,event):
        self.Ax,self.Ay=event.x,event.y
        self.nHLine=self.canvas.create_line(0,self.Ay,WIDTH,self.Ay,dash=(4, 4),fill="red")
        self.nVLine=self.canvas.create_line(self.Ax,0,self.Ax,HEIGHT,dash=(4, 4),fill="red")
        self.nRectangle=self.canvas.create_rectangle(self.Ax,self.Ay,self.Ax+1,self.Ay+1)

    def modifyRectangle(self,event):
        self.canvas.delete(self.nRectangle)
        self.canvas.delete(self.nHLine)
        self.canvas.delete(self.nVLine)
        self.nHLine=self.canvas.create_line(0,event.y,WIDTH,event.y,dash=(4, 4),fill="red")
        self.nVLine=self.canvas.create_line(event.x,0,event.x,HEIGHT,dash=(4, 4),fill="red")
        self.nRectangle=self.canvas.create_rectangle(self.Ax,self.Ay,event.x,event.y)


app = tk.Toplevel()
this_app = GUI(app)
