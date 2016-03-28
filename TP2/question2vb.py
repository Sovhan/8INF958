#encoding : utf-8
import xmlrpclib
from ldtp import *

proxy = xmlrpclib.ServerProxy("http://localhost:4118")


# Nom des fenetre de travail.
nameWindowsPrincipale = "docPourBug1.ods - LibreOffice Calc"
namePaneSecurity = "LibreOffice - Security Warning"

# permet de chercher si la fenetre que je viens d'ouvrir existe.
if not guiexist(nameWindowsPrincipale):
    proxy.launchapp("libreoffice", ['-o', 'Documents/8INF958/TP2/docPourBug1.ods'] )
    waittillguiexist(namePaneSecurity)
    try:
        proxy.click(namePaneSecurity, 'Enable Macros')
    except Exception:
        proxy.generatekeyevent('<enter>')
#waittillguiexist(nameWindowsPrincipale)



print("Test existence de la fenetre.")
result = guiexist(nameWindowsPrincipale)
print(result)

print("Test existence bouton.")
r = proxy.click(nameWindowsPrincipale, 'btnmacroBug1')

