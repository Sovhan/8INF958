#encoding : utf-8
import xmlrpclib
from ldtp import *

proxy = xmlrpclib.ServerProxy("http://localhost:4118")


# Nom des fenetre de travail.
nameWindowsPrincipale = "Untitled 1 - docPourBug1.ods"
namePaneSecurity = "LibreOffice - Security Warning"
# permet de chercher si la fenetre que je viens d'ouvrir existe.
if not guiexist(nameWindowsPrincipale):
    proxy.launchapp("libreoffice", ['-o', 'docPourBug1.ods'] )
    waittillguiexist(namePaneSecurity)
    proxy.click(namePaneSecurity, 'Enable Macros')

waittillguiexist(nameWindowsPrincipale)

print("Test existence de la fenetre.")
result = guiexist(nameWindowsPrincipale)
print(result)

print("Test existence bouton.")
r = proxy.doesmenuitemexist(nameWindowsPrincipale, 'mnuTools')

print(r)
pane = 'Macro Selector'
if r:
    proxy.selectmenuitem(nameWindowsPrincipale, 'mnuTools')
    proxy.click(nameWindowsPrincipale, 'mnuRun Macro...')
    proxy.closewindow(pane)
    proxy.selectmenuitem(nameWindowsPrincipale, 'mnuTools')
    proxy.click(nameWindowsPrincipale, 'mnuRun Macro...')

