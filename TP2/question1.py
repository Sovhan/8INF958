#from enum import Enum

print 'Test'
f = open('arg.txt','r')
lignes  = f.readlines()
f.close()

f = open('contraintes.txt','r')
constraints = f.readlines()
f.close

liste={}
listeArg=[]
listeContraintes=[]

#Etype = Enum('flag', 'nonFlag')

class Argument:

	def __init__(self,nom,isFlag,values):
		# contructeur
		self.nom=nom
		self.isFlag=isFlag
		if (isFlag):
			values=['_on','_off']
		self.values=values
	
	def toString(self):
		print "nom :"
		print self.nom
		print "is flag :"
		print self.isFlag
		print "values :"
		print self.values
"""
for ligne in lignes:
	print ligne
	
	values = ligne.split()
	key=values[0]
	values.remove(key)
	if (values == ['flag']):
		values = ['_on','_off']
	liste[key] = values

print liste
"""
print "test avec classe argument"
for ligne in lignes:
	values = ligne.split()
	nom = values[0]
	values.remove(nom)	
	listeArg.append(Argument(nom,(values==['flag']),values))

for element in listeArg :
	element.toString()


for constraint in constraints :
	values = constraint.split()
	isFlag=False
	print values
	arg1=values[0]
	for e in listeArg :
		isFlag=((('-'+arg1)==e.nom) and e.isFlag)
	if isFlag :
		val1='_on'
		arg2=values[1]
		for e in listeArg :
			if((('-'+arg2)==e.nom) and e.isFlag):
				val2='_on'
			else :
				val2=values[2]
	else :
		val1=values[1]
		arg2=values[2]
		for e in listeArg:
			if(('-'+arg2)==e.nom):
				if (e.isFlag):
					val2='_on'
				else :
					val2=values[3]
	listeContraintes.append([arg1,val1,arg2,val2])

print listeContraintes
