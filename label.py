#Python 3
import tkinter as tk
from PIL import Image, ImageTk
from os import listdir
from os.path import isfile, join

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")
        
class ImageDataset(object):
	"""docstring for ImageDataset"""
	"""Images path"""
	in_path="./output/"
	out_path="./labeling/"
	def __init__(self):
		super(ImageDataset, self).__init__()
		self.files=[f for f in listdir(self.in_path) if isfile(join(self.in_path, f))]
		print ("%d Images found " % (len(self.files)))
			
imgManager=ImageDataset()
root = tk.Tk()
app = Application(master=root)
app.mainloop()