#encoding : utf-8
import xmlrpclib
from dogtail.procedural import focus

from ldtp import *

proxy = xmlrpclib.ServerProxy("http://localhost:4118")


#Nom des fenetre de travail.
nameWindowsPrincipale = "Untitled 1 - Libre Office Calc"
#permet de chercher si la fenetre que je viens d'ouvrir existe.
proxy.launchapp("libreoffice", ['--calc'])
waittillguiexist(nameWindowsPrincipale)
result = guiexist(nameWindowsPrincipale)
print(result)

#proxy.generatemouseevent(400, 0)
proxy.activatewindow(nameWindowsPrincipale)
print("cense etre affiche")

r = proxy.doesmenuitemexist(nameWindowsPrincipale, 'Tools')
print(r)
s = proxy.doesmenuitemexist(nameWindowsPrincipale, 'btnTools')
print(s)
#proxy.invokemenu(nameWindowsPrincipale, 'Tools')



#Test des 4 possibilite.
#proxy.selectmenuitem(nameWindowsPrincipale, 'mnuEdit')
#proxy.click(nameWindowsPrincipale, 'mnuEdit')
#proxy.selectmenuitem(nameWindowsPrincipale, 'Edit')
#proxy.click(nameWindowsPrincipale, 'Edit')

#Commande pour clicker sur le bouton open.
#checkrow(nameFile, 'Sheet1', 1)


