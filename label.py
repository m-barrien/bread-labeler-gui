#Python 3
import tkinter as tk
from PIL import Image, ImageTk
from os import listdir, rename
from os.path import isfile, join

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		"""Fixed window size"""
		master.minsize(width=630, height=300)
		master.maxsize(width=630, height=300)
		master.title("Bread bin classifier")

		self.img_list=[]
		self.img_frame = tk.Frame(self)
		self.btn_frame = tk.Frame(self)

		self.pack(fill="both")
		self.create_widgets()

		[self.append_img() for i in range(5)]
		self.destroy_img()


	def create_widgets(self):
		img_frame = tk.Frame(self,width=630, height=200, bg="white", colormap="new")
		img_frame.pack(side="top",fill="both")
		self.img_frame=img_frame

		btn_frame = tk.Frame(self,width=630, height=100, bg="white", colormap="new")

		self.btn_class_empty = tk.Button(btn_frame, width=17, height=8)
		self.btn_class_empty["text"] = "Falta pan"
		self.btn_class_empty["command"] = self.classify_empty
		self.btn_class_empty.pack(side="left", padx=2, pady=2)

		self.btn_class_full = tk.Button(btn_frame, width=17, height=8)
		self.btn_class_full["text"] = "Todo pan"
		self.btn_class_full["command"] = self.classify_full
		self.btn_class_full.pack(side="left", padx=2, pady=2)

		self.btn_class_covered = tk.Button(btn_frame, width=17, height=8)
		self.btn_class_covered["text"] = "Muy cubierto"
		self.btn_class_covered["command"] = self.classify_covered
		self.btn_class_covered.pack(side="left", padx=2, pady=2)

		self.btn_class_covered = tk.Button(btn_frame, width=17, height=8)
		self.btn_class_covered["text"] = "???\nGente etc"
		self.btn_class_covered["command"] = self.classify_unknown
		self.btn_class_covered.pack(side="left", padx=2, pady=2)

		btn_frame.pack(side="bottom",fill="both")

	def append_img(self):
		image,img_path = imgManager.get_img()
		photo = ImageTk.PhotoImage(image)
		label = tk.Label(self.img_frame,image=photo)
		label.image = photo # keep a reference!
		label.pack(side="left")

		self.img_list.append((label,img_path))

	def destroy_img(self):
		#destroy old img label in display
		label,img_path = self.img_list.pop(0)
		label.pack_forget()
		#resize second place img to first place
		label,img_path = self.img_list[0]
		
		image = imgManager.get_img_path(img_path,200)
		photo = ImageTk.PhotoImage(image)

		label.config(height=200, width=200,image=photo)
		label.image = photo # keep a reference!
		label.bind("<Key>", classify_shortcut)
		label.pack(side="left")
		label.focus_set()

		self.append_img()

	def classify_full(self):
		label,img_path = self.img_list[0]
		imgManager.classify_full(img_path)
		self.destroy_img()

	def classify_empty(self):
		label,img_path = self.img_list[0]
		imgManager.classify_empty(img_path)
		self.destroy_img()

	def classify_covered(self):
		label,img_path = self.img_list[0]
		imgManager.classify_covered(img_path)
		self.destroy_img()

	def classify_unknown(self):
		label,img_path = self.img_list[0]
		imgManager.classify_unknown(img_path)
		self.destroy_img()

class ImageDataset(object):
	"""docstring for ImageDataset"""
	"""Images path"""
	in_path="./output/"
	out_path="./labeling/"
	def __init__(self):
		super(ImageDataset, self).__init__()
		self.files=[f for f in listdir(self.in_path) if isfile(join(self.in_path, f))]
		print ("%d Images found " % (len(self.files)))

	def get_img(self, qty=1):
		full_path=self.in_path + self.files.pop(0)
		img= Image.open(full_path)
		return (img,full_path)
	def get_img_path(self, full_path, size=200):
		img= Image.open(full_path)
		img= img.resize((size, size), Image.ANTIALIAS)
		return img
	def classify_full(self,full_path):
		filename = full_path.split('/')[-1]
		rename(full_path, self.out_path + "full/" + filename)
	def classify_empty(self,full_path):
		filename = full_path.split('/')[-1]
		rename(full_path, self.out_path + "empty/" + filename)
	def classify_covered(self,full_path):
		filename = full_path.split('/')[-1]
		rename(full_path, self.out_path + "covered/" + filename)
	def classify_unknown(self,full_path):
		filename = full_path.split('/')[-1]
		rename(full_path, self.out_path + "unknown/" + filename)


def classify_shortcut(event):
	keystroke=repr(event.char)
	if 'a' in keystroke:
		app.classify_empty()
		print("empty")
	elif 's' in keystroke:
		app.classify_full()
		print("full")
	elif 'd' in keystroke:
		app.classify_covered()
		print("covered")
	elif 'f' in keystroke:
		app.classify_unknown()
		print("unknown")

imgManager=ImageDataset()
root = tk.Tk()
app = Application(master=root)

app.bind("<1>", lambda event: app.focus_set())
app.bind("<Key>", classify_shortcut)

app.mainloop()