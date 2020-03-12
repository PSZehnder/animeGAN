import tkinter as tk
from PIL import Image, ImageTk
import io
import numpy as np
import cyclegan as cg
import cv2

class DrawableCanvas(tk.Canvas):

    def __init__(self, root, parent=None, **args):
        self.size = (args['width'], args['height'])
        self.root = root
        if not parent:
            self.parent = self.root
        else:
            self.parent = parent
        super(DrawableCanvas, self).__init__(parent, **args)

        # can add more bindings by adding to this table
        self.events = {
            '<B1-Motion>'       : self.draw,
            '<ButtonRelease-1>' : self.lift,
        }

        self._bind_events()
        self.mouse_coords = None

    def _bind_events(self):
        for event, func in self.events.items():
            self.root.bind(event, func)

    def draw(self, event):
        if self._mouseon():
            x, y = event.x, event.y
            if self.mouse_coords:
                self.create_line(x, y, *self.mouse_coords)
            self.mouse_coords = x, y

    def lift(self, event):
        self.mouse_coords = None

    def getImage(self):
        image = self.postscript(colormode = 'color')
        image = Image.open(io.BytesIO(image.encode('utf-8')))
        return image

    def _mouseon(self):
        x, y = self.root.winfo_pointerxy()
        widget = self.root.winfo_containing(x, y)
        return widget is self


class App:

    def __init__(self, modelpath=cg.default_path):
        self.canv_height = 512
        self.canv_width = 512
        self.base = tk.Tk()
        self.base.title('DrawMyWaifu!')

        self.mainframe = tk.Frame(self.base, padx=3, pady=12)
        self.mainframe.grid(column=0, row=0)

        self.draw_canvas = DrawableCanvas(self.base, parent=self.mainframe, height=self.canv_height,
                                          width=self.canv_width, bg='white')
        self.draw_canvas.grid(column=0, row=1)

        self.buttons_frame = tk.Frame(self.mainframe, padx=3, pady=3)
        self.but_clear = tk.Button(self.buttons_frame, text='Clear', command=self.clear)
        self.but_draw = tk.Button(self.buttons_frame, text='Generate Waifu', command=self.generateWaifu)

        self.but_clear.grid(column=0, row=0)
        self.but_draw.grid(column=1, row=0)

        self.buttons_frame.grid(column=0, row=2)

        self.display = tk.Canvas(self.mainframe, height=self.canv_height, width=self.canv_width, bg='white')
        self.display.grid(row=1, column=1)

        # add here later maybe
        self.events = {}
        self._bind_events()

        # save the model path to load later
        self.loaded = False
        self.modelpath = modelpath

    def _bind_events(self):
        for event, func in self.events.items():
            self.base.bind(event, func)

    def clear(self):
        self.draw_canvas.delete('all')

    def generateWaifu(self):
        if not self.loaded:
            self.model = cg.load_model(self.modelpath)
            self.loaded = True
        image = self.draw_canvas.getImage()
        waifu = self.model.forward(cg.im2torch(image))
        waifu = cg.torch2im(waifu, size=(self.canv_height, self.canv_width))
        print(waifu.size)
        image = ImageTk.PhotoImage(waifu)
        self.image = image
        self.display.create_image(0, 0, image=self.image, anchor='nw')

    def run(self):
        self.base.mainloop()

if __name__ == '__main__':
    app = App()
    app.run()
