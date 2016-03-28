#coding : utf-8
import xmlrpclib
from ldtp import *
wait(1)
proxy = xmlrpclib.ServerProxy("http://localhost:4118")

print(proxy.getwindowlist())
# Nom des fenetre de travail.
nameWindowsPrincipale = "*Calc"
namePaneSecurity = "LibreOffice - Security Warning"

waittillguiexist(namePaneSecurity)
try:
    proxy.click(namePaneSecurity, 'Enable Macros')
except Exception:
    proxy.generatekeyevent('<enter>')

print(proxy.getwindowlist())
proxy.generatemouseevent(500, 500)

if guiexist(nameWindowsPrincipale):
    r = proxy.click(nameWindowsPrincipale, 'btnmacroBug1')
    wait(5)
    if guiexist(nameWindowsPrincipale):
        print("Pas de bug dans cette version")
    elif guiexist('frm0'):
        print("erreur Calc s est ferme")
elif guiexist('frm0'):
    r = proxy.click('frm0', 'btnmacroBug1')
    wait(5)
    if guiexist('frm0'):
        print("Pas de bug dans cette version")
    elif guiexist('frm0'):
        print("erreur Calc s est ferme")
else:
    print("BUG LIBRE OFFICE")
print('Calc est cense avoir crashe')