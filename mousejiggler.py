# Source http://pyautogui.readthedocs.org/en/latest/mouse.html
# Quartz installeren: pyobjc-framework-Quartz
# Versie 1.0
# Importeren van modules
import pyautogui
import sys

# Auteur
__author__ = 'Chester'


while True:
    # Aantal pixels opvragen bij gebruiker.
    pxl = raw_input("Vul het aantal pixels in dat de muis moet bewegen: ")
    try:
        # Controle of het ingevulde karakter een getal is.
        val = int(pxl)
        print("Het programma is gestart. \
        Druk op crtl+c om de mousejiggler te beeindigen.")
        break
    except ValueError:
        # Wanneer er geen getal is ingevuld, verschijnt de volgende foutmelding
        print("Er is een ander karakter dan een getal ingevuld. \
        Probeer het opnieuw.")


try:
    # Voor loop
    count = 0
    while True:
        # Bepalen huidige positie van de muis
        x, y = pyautogui.position()
        if count % 2 == 1:
            # Bwegen van muis naar rechts
            pyautogui.moveTo(int(x)+int(pxl), None)
        else:
            # Bewegen van muis naar links
            pyautogui.moveTo(int(x)-int(pxl), None)
        count = count + 1
except KeyboardInterrupt:
    print '\n'

print ("Het programma is beeindigd.")
