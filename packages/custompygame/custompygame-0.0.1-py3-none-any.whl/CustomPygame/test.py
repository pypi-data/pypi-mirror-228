from screen import Screen
from Widgets.button import Button
from Widgets.label import Label
from Widgets.check_box import Check_Box
from Widgets.combo_box import Combo_Box

sc = Screen()
btn1 = Button(size=(150, 50), pos=(20, 20), radius=10, frame=2)
cob1 = Combo_Box(size=(100, 25), pos=(200, 20), radius=10)
lbl1 = Label(size=(100, 100), pos=(20, 100), frame=2)
cb1 = Check_Box(pos=(200, 100))
sc.add_figure(btn1)
sc.add_figure(cob1)
sc.add_figure(lbl1)
sc.add_figure(cb1)

while True:
    sc.update()
