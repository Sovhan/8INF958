# encoding : utf-8
import xmlrpclib
from ldtp import *

proxy = xmlrpclib.ServerProxy("http://localhost:4118")

# Nom des fenetre de travail.
nameWindowsPrincipale = "Untitled 1 - LibreOffice Writer"
# permet de chercher si la fenetre que je viens d'ouvrir existe.
if not guiexist(nameWindowsPrincipale):
    proxy.launchapp("libreoffice4.3", ['--writer'])
waittillguiexist(nameWindowsPrincipale)

print("Test existence de la fenetre.")
result = guiexist(nameWindowsPrincipale)
print(result)
if result:
    proxy.activatewindow(nameWindowsPrincipale)
for _ in range(10):
    proxy.generatekeyevent('f')
    wait(0.05)
    proxy.generatekeyevent('<ctrl><enter>')

proxy.generatekeyevent('<ctrl>f')
wait(0.3)
proxy.generatekeyevent('f')
proxy.mousemove(nameWindowsPrincipale, 'btnFindNext')
proxy.mouseleftclick(nameWindowsPrincipale, 'btnFindNext')

proxy.mousemove(nameWindowsPrincipale, 'btnFindNext')
wait(1)
proxy.generatekeyevent('<ctrl>f')
proxy.keypress('<ctrl>')
proxy.keypress('f')
proxy.keyrelease('f')
proxy.keyrelease('<ctrl>')
