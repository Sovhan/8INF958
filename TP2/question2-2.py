# encoding : utf-8
import xmlrpclib
from ldtp import *

proxy = xmlrpclib.ServerProxy("http://localhost:4118")

# Nom des fenetre de travail.
nameWindowsPrincipale = "Untitled 1 - LibreOffice Writer"
# permet de chercher si la fenetre que je viens d'ouvrir existe.
if not guiexist(nameWindowsPrincipale):
    proxy.launchapp("libreoffice", ['--writer'])
waittillguiexist(nameWindowsPrincipale)

print("Test existence de la fenetre.")
result = guiexist(nameWindowsPrincipale)
print(result)

for _ in range(10):
    proxy.generatekeyevent('f')
    proxy.generatekeyevent('<ctrl><enter>')

proxy.generatekeyevent('<ctrl>f')
wait(1)
proxy.generatekeyevent('f')
print(proxy.getchild(nameWindowsPrincipale, 'Find Next'))
proxy.mousemove(nameWindowsPrincipale, 'btnFindNext')
proxy.mouseleftclick(nameWindowsPrincipale, 'btnFindNext')
wait(1)
proxy.generatekeyevent('<enter>')
proxy.generatekeyevent('<ctrl>f')
proxy.generatekeyevent('<ctrl>f')
proxy.generatekeyevent('<ctrl>f')

