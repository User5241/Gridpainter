from customtkinter import *
from rich.traceback import install; install(show_locals=True)
import json
import time
from functools import wraps

class Timer(object):
    """docstring for Timer"""
    def __init__(self):
        super(Timer, self).__init__()
        self.start = None
        self.stop = None

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, *args, **kwargs):
        print(f" done in: {time.perf_counter() - self.start}")

class GridMarker(CTkFrame):
    def __init__(self, cls, *args, **kwargs):
        if 'width' not in kwargs:
            kwargs['width'] = 30
        if 'height' not in kwargs:
            kwargs['height'] = 30
        if 'fg_color' not in kwargs:
            kwargs['fg_color'] = "black"
        if 'bg_color' not in kwargs:
            kwargs['bg_color'] = "black"
        kwargs['master'] = cls
        super().__init__(*args, **kwargs)
    

class Grid(CTk):
    def __init__(self, rows, columns, scale, *args, **kwargs):
        super().__init__(*args)
        self.title(kwargs.get('title', "Gridpainter"))
        self.geometry(kwargs.get("geometry", f"{scale}x{scale}"))
        self.rows = rows
        self.columns = columns
        self.grid = {
            'pixels': {},
            'markers': {},
            'vlines': {},
            'hlines': {},
        }
        self.create_grid()
    
    def create_grid(self):
        # Don't create markers unless debugging
        if __debug__:
            for x in range(self.columns):
                for y in range(self.rows):
                    marker = CTkLabel(master=self, width=30, height=30, fg_color="white", bg_color="transparent", text=str(x)+","+str(y), font=("Arial", 9), justify=CENTER, text_color="white", anchor=CENTER)
                    marker.place(y=(y*30)+2,x=(x*30)+4)
                    self.grid['markers'][f"{x}:{y}"] = marker

        for x in range(self.columns):
            vertical_line = GridMarker(self, width=4, height=scale)
            vertical_line.place(y=0,x=x*30)
            self.grid['vlines'][f"{x}:0"] = vertical_line

        for y in range(self.rows):
            horizontal_line = GridMarker(self, width=scale, height=4)
            horizontal_line.place(y=y*30,x=0)
            self.grid['hlines'][f"0:{y}"] = horizontal_line

    def setPixel(self, x, y, color="white"):
        iterx = x if hasattr(x, '__iter__') else [x]
        itery = y if hasattr(y, '__iter__') else [y]
        for x in iterx:
            for y in itery:
                pixel = GridMarker(self, fg_color=color)
                pixel.place(y=y*30+2,x=x*30+2)
                self.grid['pixels'][f"{x}:{y}"] = pixel

    @classmethod
    def load_screen(fp):
        grid = json.loads(fp)
        rows = grid.get('rows')
        col = grid.get('col')
        scale = grid.get('scale')
        return Grid(rows, col, scale)
                
gridsize=24 #Change this for the size of the grid
scale=(gridsize*30)+4
with Timer():
    root = Grid(gridsize, gridsize, title="Gridpainter", scale=scale)

with Timer():
    for x, y in zip(range(10), range(10)):
        root.setPixel(x,y, 'black')
with Timer():
    root.setPixel(range(1,10,2), range(4), 'blue')

with Timer():
    root.setPixel([1,3,5,7,9,11,13,15,17,19], [1,3,5,7,9,11,13,15,17,19], "green")

root.resizable(False, False)
root.mainloop()
