from customtkinter import *
from utils import *
import json
from rich.traceback import install; install(show_locals=True)


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
    # TODO get working
    @classmethod
    def load_screen(self, grid: dict):
        """
        The grid file is a json formatted file structured like:
        {
            "rows": int,
            "col": int,
            "scale": int,
            "pixels": {
                "x:y": "color",
            },
        }
        """
        pixels = grid.pop('pixels')
        g = Grid(grid.pop('rows'), grid.pop('col'), (grid.pop('scale')*30)+4)
        for pixel in pixels:
            x, y = pixel.split(':')
            g.setPixel(int(x), int(y), color=pixels.get(pixel))
        return g
                
gridsize=25 #Change this for the size of the grid
scale=(gridsize*30)+4

with Timer():
    with open("grid.json") as fp:
        root = Grid.load_screen(json.load(fp))

root.resizable(False, False)
root.mainloop()
