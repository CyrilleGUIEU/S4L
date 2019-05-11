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
app.attributes('-topmost', True)
app.attributes('-fullscreen', 1)


isCapturing=False


print("""S4L is now running ...
1. Reduce the window
2. Press '"""+KEYNAME+"'"+
"""
3. Select a rectangle in the frozen screen
4. Paste the paper clip in your Latex code editor
5. Go back to step 2 if necessary
      """)
          

def hideWindow(event):
    global isCapturing,Ax,Ay
    app.state('withdrawn')
    app.quit()
    isCapturing=False
    Ax,Bx=min(Ax,event.x),max(Ax,event.x)
    Ay,By=min(Ay,event.y),max(Ay,event.y)
    capture=image.crop((Ax,Ay,Bx,By))
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
def createRectangle(event):
    global Ax,Ay,nRectangle,nHLine,nVLine
    Ax,Ay=event.x,event.y
    nHLine=canvas.create_line(0,Ay,WIDTH,Ay,dash=(4, 4),fill="red")
    nVLine=canvas.create_line(Ax,0,Ax,HEIGHT,dash=(4, 4),fill="red")
    nRectangle=canvas.create_rectangle(Ax,Ay,Ax+1,Ay+1)

def modifyRectangle(event):
    global nRectangle,nHLine,nVLine
    canvas.delete(nRectangle)
    canvas.delete(nHLine)
    canvas.delete(nVLine)
    nHLine=canvas.create_line(0,event.y,WIDTH,event.y,dash=(4, 4),fill="red")
    nVLine=canvas.create_line(event.x,0,event.x,HEIGHT,dash=(4, 4),fill="red")
    nRectangle=canvas.create_rectangle(Ax,Ay,event.x,event.y)
    
app.bind_all('<ButtonRelease-1>', hideWindow)
app.bind_all('<Button-1>', createRectangle)
app.bind_all('<B1-Motion>', modifyRectangle)

while True:
    if keyboard.is_pressed(KEYNAME) and isCapturing==False:
        isCapturing=True
        capture=mss.mss()
        capture.shot(output=IMAGETEMP)
        capture.close()
        image = Image.open(IMAGETEMP)
        photo = ImageTk.PhotoImage(image)
        canvas = tk.Canvas(width=WIDTH, height=HEIGHT, bg='black',cursor='crosshair')
        canvas.pack(expand=tk.YES, fill=tk.BOTH)
        canvas.create_image(00, 00, image=photo, anchor=tk.NW)
        app.state('normal')
        app.mainloop()
        try:
            canvas.destroy()
        except NameError:
            pass
        
