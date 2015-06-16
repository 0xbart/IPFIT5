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
    pxl = raw_input("Write the amount of pixels the\
     mouse should be jiggling ")
    try:
        # Controle of het ingevulde karakter een getal is.
        val = int(pxl)
        print("The program has been launched. \
        Press CTRL+C to quit.")
        break
    except ValueError:
        # Wanneer er geen getal is ingevuld, verschijnt de volgende foutmelding
        print("An error has occured. Please fill in a number.")


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

print ("The program has been terminated.")
