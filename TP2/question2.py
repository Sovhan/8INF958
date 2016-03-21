# coding : utf-8
import xmlrpclib
proxy = xmlrpclib.ServerProxy("http://localhost:4118")

proxy.launchapp("libreoffice", ["--calc"])
from ldtp import *
#permet de chercher si la fenetre que je viens d'ouvrir existe.
result = guiexist('Untitled 1 - Libre Office Calc')
print(result)

#Commande pour clicker sur le bouton open.
click('*-LibreOffice Calc', 'btnOpen')

