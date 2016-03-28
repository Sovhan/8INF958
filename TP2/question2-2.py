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

proxy.generatekeyevent('<ctrl>f')
proxy.generatekeyevent('<ctrl>f')
proxy.generatekeyevent('<esc><esc>')
