# Source http://inventwithpython.com/pyperclip.py
# Versie 1.0
# Importeren van modules
import pyperclip

# Auteur
__author__ = 'Chester'

# Output schrijven naar 'spam'
spam = pyperclip.paste()

# Aanmaken en schrijven naar bestand
text_file = open("clipboard.txt", "w")
text_file.write(spam)
text_file.close()

# Bestand is aangemaakt
print("File clipboard.txt has been created")
