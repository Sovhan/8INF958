print 'Test'
f = open('arg.txt','r')
lignes  = f.readlines()
f.close()
liste={}

 
for ligne in lignes:
	print ligne
	
	values = ligne.split()
	key=values[0]
	values.remove(key)
	liste[key] = values

print liste
