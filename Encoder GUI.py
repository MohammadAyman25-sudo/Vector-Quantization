from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import Encoder
from  PIL import Image
import numpy as np

root = Tk()
root.title("Vector Quantization Compression")
root.resizable(False, False)

style = ttk.Style()
style.configure('TLabel', font=('Arial', 14, 'bold'))
style.configure('TButton', font=('Arial', 14, 'bold'))

width_label = ttk.Label(root, text="Width: ")
width_label.grid(row=0, column=0, padx=10, pady=10)

width_input = ttk.Entry(root, width=30)
width_input.grid(row=0, column=1, pady=10, padx=10)
width_input.config(font=('Arial', 14, 'bold'))

height_label = ttk.Label(root, text='Height: ')
height_label.grid(row=1, column=0, padx=10, pady=10)

height_input = ttk.Entry(root, width=30)
height_input.grid(row=1, column=1, padx=10, pady=10)
height_input.config(font=('Arial', 14, 'bold'))

code_book_count_label = ttk.Label(root, text='number of vectors')
code_book_count_label.grid(row=2, column=0, padx=10, pady=10)

code_book_count_input = ttk.Entry(root, width=30)
code_book_count_input.grid(row=2, column=1, padx=10, pady=10)
code_book_count_input.config(font=('Arial', 14, 'bold'))

image_label = ttk.Label(root, text="Image: ")
image_label.grid(row=3, column=0, padx=10, pady=10)

img_path = ttk.Button(root, text="choose an image...")
img_path.grid(row=3, column=1, padx=10, pady=10)

img_path_label = ttk.Label(root, text='')
img_path_label.grid(row=3, column=2, padx=10, pady=10)

compression = ttk.Button(root, text='Compress')
compression.grid(row=4, column=0, padx=10, pady=10)

decompression = ttk.Button(root, text='Decompress')
decompression.grid(row=4, column=1, pady=10, padx=10)


path = None


def choose_image():
    global path
    path = filedialog.askopenfilename()
    img_path_label.config(text=str(path))


def compress():
    Encoder.run_encoder(width_input.get(), height_input.get(), code_book_count_input.get(), path)
    messagebox.showinfo('Congrats', 'Compression Done Successfully')


def decompress():
    print(Encoder.get_codes())
    Encoder.decode(int(width_input.get()), int(height_input.get()), np.array(Image.open('compressed.png').convert('L')),
                   Encoder.get_codes())
    messagebox.showinfo('Congrats', 'Decompression Done Successfully')


img_path.config(command=choose_image)
compression.config(command=compress)
decompression.config(command=decompress)

root.mainloop()
