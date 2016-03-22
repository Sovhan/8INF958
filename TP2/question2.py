#encoding : utf-8
import xmlrpclib
from ldtp import *

proxy = xmlrpclib.ServerProxy("http://localhost:4118")


#Nom des fenetre de travail.
nameWindowsPrincipale = "Untitled 1 - LibreOffice Calc"
#permet de chercher si la fenetre que je viens d'ouvrir existe.
#proxy.launchapp("libreoffice", ['--calc'])
#waittillguiexist(nameWindowsPrincipale)

print("Test existence de la fenetre.")
result = guiexist(nameWindowsPrincipale)
print(result)

#proxy.generatemouseevent(400, 0)
print("Test existence bouton.")
#proxy.selectmenuitem('*Calc', 'mnuFile;mnuNew')
r = proxy.doesmenuitemexist(nameWindowsPrincipale, 'mnuFile;mnuNew')
print(r)
#s = proxy.doesmenuitemexist(nameWindowsPrincipale, 'Libre Office Calc btnTools;Solver...')
#print(s)
#t = proxy.doesmenuitemexist(nameWindowsPrincipale, 'Libre Office Calc mbarTools;Solver...')
#print(t)

#proxy.invokemenu(nameWindowsPrincipale, 'Tools')



#Test des 4 possibilite.
#proxy.selectmenuitem(nameWindowsPrincipale, 'mnuEdit')
#proxy.click(nameWindowsPrincipale, 'mnuEdit')
#proxy.selectmenuitem(nameWindowsPrincipale, 'Edit')
#proxy.click(nameWindowsPrincipale, 'Edit')

#Commande pour clicker sur le bouton open.
#checkrow(nameFile, 'Sheet1', 1)


