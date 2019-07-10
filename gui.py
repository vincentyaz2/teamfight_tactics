import tkinter as tk
from teamfight_tactics import Basic
from teamfight_tactics import Combined
import re


'''
GUI layout:

8 radio buttons on top - choose component 1
8 radio buttons below - choose component 2

1 normal button to compute the whole thing

Display result in a label


'''

'''
Glossary: 

ad for attack damage
as for attack speed
ap for ability power
mn for mana
ar for armor
mr for magic resist
hp for health points
wi for wildcard

'''

from functools import partial

items = (
	'ad',
	'as',
	'ap',
	'mana',
	'ar', 
	'mr',
	'hp',
	'spatula'
	)

mapper = {
	1:'ad',
	2:'as',
	3:'ap',
	4:'mn',
	5:'ar',
	6:'mr',
	7:'hp',
	8:'wi'
}

# GUI functions



def combine():
	name_1 = mapper[v1.get()]
	name_2 = mapper[v2.get()]

	item1 = Basic(name_1)
	item2 = Basic(name_2)

	combined = item1.combine_fromitemobject(item2)

	# since it won't be obvious for users that wi stands for wildcard
	# we will replace it with spatula
	desc = combined.description()
	desc = re.sub(r'wi', 'spatula', desc)

	label_text.set(desc)


# GUI

window = tk.Tk()
window.title('Item Builder')
window.geometry('575x400')

label_text=tk.StringVar()
label_text.set('Nothing combined yet.')


v1 = tk.IntVar()
v1.set(1) # initializing the choice to 'ad'

v2 = tk.IntVar()
v2.set(1)

def show_choice():
	print(v2.get())

label = tk.Label(text="Choose the two items you're combining.")
label.grid(column=0, row=0, columnspan=8, padx=100, pady=10)


# radio buttons for 
for i,item in enumerate(items, start=1):
	tmp = tk.Radiobutton(text=item, variable=v1, value=i)
	tmp.grid(column=i-1, row=1, sticky=tk.W, padx=10) # sticky to align west

	tmp2 = tk.Radiobutton(text=item, variable=v2, value=i)
	tmp2.grid(column=i-1, row=2, sticky=tk.W, padx=10)


combine = tk.Button(text='Combine!', command=combine)
combine.grid(column=0, row=3, pady=30, columnspan=8)

result = tk.Label(textvariable=label_text)
result.grid(column=0, row=4, pady=30, columnspan=8)


window.mainloop()










































