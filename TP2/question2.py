#encoding : utf-8
import xmlrpclib
from ldtp import *

proxy = xmlrpclib.ServerProxy("http://localhost:4118")
#proxy.launchapp("libreoffice", ['--calc'])

#Nom des fenetre de travail.
nameWindowsPrincipale = "Untitled 1 - Libre Office Calc"
nameSpreadsheet = "Untitled1 - LibreOffice Spreadsheets"
#permet de chercher si la fenetre que je viens d'ouvrir existe.

waittillguiexist(nameWindowsPrincipale)
result = guiexist(nameWindowsPrincipale)
print(result)
selectmenuitem('*-LibreOffice Calc', 'Undo')
#Commande pour clicker sur le bouton open.
#checkrow(nameFile, 'Sheet1', 1)


