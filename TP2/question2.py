#encoding : utf-8
import xmlrpclib
from ldtp import *

proxy = xmlrpclib.ServerProxy("http://localhost:4118")


# Nom des fenetre de travail.
nameWindowsPrincipale = "Untitled 1 - LibreOffice Calc"
# permet de chercher si la fenetre que je viens d'ouvrir existe.
if not guiexist(nameWindowsPrincipale):
    proxy.launchapp("libreoffice", ['--calc'])
waittillguiexist(nameWindowsPrincipale)

print("Test existence de la fenetre.")
result = guiexist(nameWindowsPrincipale)
print(result)

print("Test existence bouton.")
r = proxy.doesmenuitemexist(nameWindowsPrincipale, 'mnuFile;'
                                                   'mnuNew;'
                                                   'mnuText Document')
print(r)
pane = 'Macro Selector'
if r and not guiexist(pane):
    proxy.selectmenuitem(nameWindowsPrincipale, 'mnuTools;mnuMacros')
    proxy.click(nameWindowsPrincipale, 'mnuRun Macro...')
    print(proxy.doesrowexist(pane, 'treeLibrary', 'Untitled 1'))
    l = proxy.getobjectinfo(pane, 'treeLibrary')
    for info in l:
        print(info, " = ", proxy.getobjectproperty('Macro Selector', 'treeLibrary', info))

    proxy.selectrow(pane, 'Library', 'Untitled 1')
