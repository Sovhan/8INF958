bug 1 (# sur la plateforme calc):
- réglages serveur du cours :
	- activation ldtp
	- activation toolkit d'accessibilité 
- réglages libre office : il faut modifier la sécurité des macros
Nous exploitons le bug via une macro dans libre office calc, il faut donc modifier la sécurité afin de pouvoir l'exécuter
	- ouvrir libre office calc
	- dans tools -> options -> security -> macro security -> cocher la case "Medium" puis fermer libre office
déroulement de la macro, fonctionnelle sur nos VM : 
	- insertion d'un commentaire dans la case A1, 
	- drag & drop dans la case A2
	- drag & drop dans la case A3
	- Ctrl + Z
	- Ctrl + Z
	- Ctrl + Y
	-> crash de libre office
Ce bug est présent sur libre office 3, 4 et la macro permet aussi de révéler le bug sur libre office 5 (il est censé avoir été corrigé, il a donc a priori juste été contourné)

bug 2 (#83626 sur plateforme writer) :
- ldtp doit être activé
- il y a un problème d'input avec les combinaisons de touches dans ldtp :
	- le Ctrl + F fonctionne une fois mais ne peut plus être réitéré pour désactiver les fenêtres de recherche (rendant l'implémentation du bug incomplête)

