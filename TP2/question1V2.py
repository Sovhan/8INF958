# classe argument : permet de verifier si un argument est un flag, et quelles valeurs sont possibles
class Argument:

	# constructeur
	def __init__(self,nom,isFlag,values):
		self.nom=nom
		self.isFlag=isFlag
		if (isFlag):
			values=['_on','_off']
		self.values=values
		
	# affichage : utile pour le debug	
	def toString(self):
		print ""
		print "**********"
		print "nom :"
		print self.nom
		print "is flag :"
		print self.isFlag
		print "values :"
		print self.values
		print "**********"
		print ""

# conversion du fichier texte en tableau d'argument
def createListeArg(file):
	# recuperation du fichier d'arguments
	#f = open('arg.txt','r')
        f = open(file,'r')
	lignes  = f.readlines()
	f.close()
	
	# variables utilisees
	listeArg=[]

	for ligne in lignes:
		values = ligne.split()
		nom = values[0]
		values.remove(nom)	
		listeArg.append(Argument(nom,(values==['flag']),values))

        return listeArg;

# conversion du fichier texte en tableau de contraintes 
# mise en forme des contraintes : si la variable est un flag on ajoute sa valeur _on
# au final on aura juste une suite de variable / valeur facile a utiliser
def createListeContraintes(file,listeArg):
	# recuperation du fichier de contraintes
	f = open(file,'r')
	constraints = f.readlines()
	f.close

	# variables utilisees
	listeContraintes=[]
	
	# on traite chaque contrainte puis on l'ajoute a la liste des contraintes
	for constraint in constraints :
		values = constraint.split()
		line=[];
		# on traite chacune des valeurs de la contrainte :
		# - si c'est un flag, on lui ajoute la valeur _on
		# - sinon, on recupere la valeur fournie		
		while (values != []):
			nom=values[0]
			#line.append(nom)
			values.remove(nom)
			val=''
			for e in listeArg :
				if (('-'+nom)==e.nom):
					if e.isFlag :
						#line.append('_on')
						val='_on'
					else :
						val=values[0]
						#line.append(val)
						values.remove(val)
			line.append([nom,val])
		listeContraintes.append(line)
	return listeContraintes;

# compareListeCombListeCont : comparaison entre la liste de combinaisons fournies et la liste des contraintes, renvoie la liste des combinaisons dans celles qui ne satisfaisent pas une contrainte
def compareListeCombListeCont(listeComb, listeCont):
	for comb in listeComb :
		if compareCombListeCont(comb,listeCont) :
			listeComb.remove(comb)
			print "comb non valide retiree"
	return listeComb;

# compareCombListeCont : comparaison entre la combinaison fournie et la liste des contraintes, renvoie false si la combinaison ne satisfait pas l'une des contraintes
def compareCombListeCont(comb,listeCont):
	isInListCont=False
	for cont in listeCont:
		isInListCont=(isInListCont or compareCombCont(comb,cont))
	return isInListCont;

# compareCombCont : comparaison entre une combinaison et une contrainte, renvoie False si tous les elements de la contrainte sont violes
def compareCombCont(comb,cont):
	isTheCont=True
	allChecked=True
	for element in cont :
		checked=False
		for arg in comb :
			if element[0]==arg[0]:
				isTheCont = isTheCont and (element[1]==arg[1])
				checked=True
		allChecked=allChecked and checked
	return (isTheCont and allChecked);

# creation de la liste des arguments
listeArguments = createListeArg('arg.txt')
# affichage
print "\n affichage de la liste des arguments"
for element in listeArguments :
        element.toString()

# creation de la liste des contraintes
listeContraintes = createListeContraintes('contraintes.txt',listeArguments)
# affichage
print "\n affichage de la liste des contraintes"
print listeContraintes

listeComb=[]
for element1 in listeArguments:
	for val1 in element1.values:
		for element2 in listeArguments:
			if element2==element1:
				print "c'est le meme"
			else :
				for val2 in element2.values:
					tab=[]
					tuple=[element1.nom,val1]
					tab.append(tuple)
					tuple=[element2.nom,val2]
					tab.append(tuple)
					listeComb.append(tab)

#print listeComb


listeComb2=[]
element=[['a','1'],['j','-1']]
listeComb2.append(element)
element=[['h','_on'],['a','1'],['f','off']]
listeComb2.append(element)
element=[['a','1']]
listeComb2.append(element)
element=[['abc','14']]
listeComb2.append(element)

print "avant"
print listeComb2
listeComb=compareListeCombListeCont(listeComb2,listeContraintes)
print "apres"
print listeComb2
