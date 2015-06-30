# Source http://stackoverflow.com/questions/415511/how-to-get-current-time-in-python
# Versie 1.0
# Importeren van modules
from time import gmtime, strftime
from datetime import datetime

# Auteur
__author__ = 'Chester'

# Print van datum, tijd en tijdzone
print ("De datum en tijd van het systeem is: " + str(datetime.now()))
print ("De tijdzone van het systeem is: " + strftime("%z", gmtime()))
