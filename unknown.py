from Tkinter import *
import ttk
from PIL import *
from PIL import Image
import os
root = Tk();

text = Text(root, width = 300, height=300)
text.grid(row=0, column=0)
text.grid_propagate(False)


class ImageLabel:
    def __init__(self, master, img_file):        
        label = Label(master)
        label.img = PhotoImage(file=img_file)
        label.config(image=label.img)
        label.pack(side="bottom")

## Adding images to text widget
width = 300
src = "./downloads/"
my_item_id = 770353540339
count = 0;
file_name = str(my_item_id)+'_'+str(count)+'.jpeg';
full_file_name = os.path.join(src, file_name)

imagelabels = []
while os.path.isfile(full_file_name):
    im = Image.open(full_file_name)
    height = width*im.size[1]/im.size[0]
    im.thumbnail((width, height), Image.ANTIALIAS)
    im.save(str(count),'gif')
    imagelabels.append(ImageLabel(text, str(count)))
    count = count+1;
    file_name = str(my_item_id)+'_'+str(count)+'.jpeg';
    full_file_name = os.path.join(src, file_name)
    print(count)

## Adding scrollbar
scrollbar = Scrollbar(root, orient=VERTICAL, command=text.yview)
scrollbar.grid(row=0,column=1, sticky='ns')
text.config(yscrollcommand=scrollbar.set)

root.mainloop()
 