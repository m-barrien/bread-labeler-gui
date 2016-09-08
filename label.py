#Python 3
import tkinter as tk
from PIL import Image, ImageTk
from os import listdir
from os.path import isfile, join

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		"""Fixed window size"""
		master.minsize(width=630, height=300)
		master.maxsize(width=630, height=300)

		self.img_list=[]
		self.img_frame = tk.Frame(self)
		self.btn_frame = tk.Frame(self)

		self.pack(fill="both")
		self.create_widgets()

		[self.append_img() for i in range(5)]

	def create_widgets(self):
		img_frame = tk.Frame(self,width=630, height=200, bg="white", colormap="new")
		img_frame.pack(side="top",fill="both")
		self.img_frame=img_frame

		btn_frame = tk.Frame(self,width=630, height=100, bg="white", colormap="new")

		self.btn_class_empty = tk.Button(btn_frame, width=10)
		self.btn_class_empty["text"] = "Empty"
		self.btn_class_empty["command"] = self.append_img
		self.btn_class_empty.pack(side="left", padx=2, pady=2)

		self.btn_class_full = tk.Button(btn_frame, width=10)
		self.btn_class_full["text"] = "Full"
		self.btn_class_full["command"] = self.append_img
		self.btn_class_full.pack(side="left", padx=2, pady=2)

		self.btn_class_covered = tk.Button(btn_frame, width=10)
		self.btn_class_covered["text"] = "Covered"
		self.btn_class_covered["command"] = self.destroy_img
		self.btn_class_covered.pack(side="left", padx=2, pady=2)

		self.btn_class_covered = tk.Button(btn_frame, width=10)
		self.btn_class_covered["text"] = "???"
		self.btn_class_covered["command"] = self.destroy_img
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
		label.pack(side="left")

		self.append_img()

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
		os.rename(full_path, out_path + "full/" + filename)
	def classify_empty(self,full_path):
		filename = full_path.split('/')[-1]
		os.rename(full_path, out_path + "empty/" + filename)
	def classify_covered(self,full_path):
		filename = full_path.split('/')[-1]
		os.rename(full_path, out_path + "covered/" + filename)
	def classify_unknown(self,full_path):
		filename = full_path.split('/')[-1]
		os.rename(full_path, out_path + "unknown/" + filename)

imgManager=ImageDataset()
root = tk.Tk()
app = Application(master=root)
app.mainloop()