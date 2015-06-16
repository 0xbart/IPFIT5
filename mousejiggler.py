#Source http://pyautogui.readthedocs.org/en/latest/mouse.html
#Quartz installeren: pyobjc-framework-Quartz
#Versie 1.0

#Auteur
__author__ = 'Chester'

#Importeren van modules
import pyautogui, sys

while True:
    pxl = raw_input("Vul het aantal pixels in dat de muis moet bewegen: ")
    try:
        val = int(pxl)
        print("Het programma is gestart. Druk op crtl+c om de mousejiggler te beeindigen.")
        break
    except ValueError:
        print("Er is een ander karakter dan een getal ingevuld. Probeer het opnieuw.")


try:
    count = 0
    while True:
        x, y = pyautogui.position()
        if count % 2 == 1:
            pyautogui.moveTo(int(x)+int(pxl), None)
        else:
            pyautogui.moveTo(int(x)-int(pxl), None)
        count = count + 1
except KeyboardInterrupt:
    print '\n'

print ("Het programma is beeindigd.")



#to-do
#escape chars inbouwen
