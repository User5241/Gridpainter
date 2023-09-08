from customtkinter import *
from rich.traceback import install; install(show_locals=True)
import numpy


gridsize=24 #Change this for the size of the grid
scale=(gridsize*30)+4


class Grid(CTk):
    def __init__(self, rows, columns, title="", geometry="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)
        self.geometry(geometry)
        self.rows = rows
        self.columns = columns
        self.pixels = {}
        self.Markers = []
        self.Vertical_Lines = []
        self.Horizontal_Lines = []
        self.create_grid()

    def create_grid(self):
        # Don't create markers unless debugging
        if __debug__:
            for x in range(self.columns):
                for y in range(self.rows):
                    marker = CTkLabel(master=self, width=30, height=30, fg_color="transparent", bg_color="transparent", text=str(x)+","+str(y), font=("Arial", 9), justify=CENTER, text_color="white", anchor=CENTER)
                    marker.place(y=(y*30)+2,x=(x*30)+4)
                    self.Markers.append(marker)

        for x in range(self.columns):
            vertical_line = CTkFrame(master=self, width=4, height=scale, fg_color="black", bg_color="black")
            vertical_line.place(y=0,x=x*30)
            self.Vertical_Lines.append(vertical_line)

        for y in range(self.rows):
            horizontal_line = CTkFrame(master=self, width=scale, height=4, fg_color="black", bg_color="black")
            horizontal_line.place(y=y*30,x=0)
            self.Horizontal_Lines.append(horizontal_line)

    def setPixel(self, x, y, color="white"):
        if hasattr(x, '__iter__'):
            iterx = x
        else:
            iterx = [x]
        if hasattr(y, '__iter__'):
            itery = y
        else:
            itery = [y]
        for x in iterx:
            for y in itery:
                pixel = CTkFrame(master=self, width=30, height=30, fg_color=color, bg_color="black")
                self.pixels[f'{x}:{y}'] = pixel
                self.pixels[f'{x}:{y}'].place(y=y*30+2,x=x*30+2)


root = Grid(gridsize, gridsize, title="Gridpainter", geometry=f"{scale}x{scale}")

root.setPixel(0,0)
root.setPixel(0,0, 'black')
print(len(root.pixels))

root.resizable(False, False)
root.mainloop()
