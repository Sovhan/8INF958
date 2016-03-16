# classe argument : permet de verifier si un argument est un flag, et quelles valeurs sont possibles
class Argument:
    # constructeur
    def __init__(self, nom, isFlag, values):
        self.nom = nom
        self.isFlag = isFlag
        if (isFlag):
            self.values = ['_on', '_off']
        self.values = values

    # affichage : utile pour le debug
    def toString(self):
        print()
        print("**********")
        print("nom :")
        print(self.nom)
        print("is flag :")
        print(self.isFlag)
        print("values :")
        print(self.values)
        print("**********")
        print()


# conversion du fichier texte en tableau d'argument
def createListeArg(file):
    # recuperation du fichier d'arguments
    # f = open('arg.txt','r')
    f = open(file, 'r')
    lignes = f.readlines()
    f.close()

    # variables utilisees
    listeArg = []

    for ligne in lignes:
        values = ligne.split()
        nom = values.pop(0)
        listeArg.append(Argument(nom, (values == ['flag']), values))

    return listeArg


# conversion du fichier texte en tableau de contraintes
# mise en forme des contraintes : si la variable est un flag on ajoute sa valeur _on
# au final on aura juste une suite de variable / valeur facile a utiliser
def createListeContraintes(file, listeArg):
    # recuperation du fichier de contraintes
    f = open(file, 'r')
    constraints = f.readlines()
    f.close()

    # variables utilisees
    contraintes = []

    # on traite chaque contrainte puis on l'ajoute a la liste des contraintes
    for constraint in constraints:
        values = constraint.split()
        line = []
        # on traite chacune des valeurs de la contrainte :
        # - si c'est un flag, on lui ajoute la valeur _on
        # - sinon, on recupere la valeur fournie
        while values:
            nom = values.pop(0)
            line.append(nom)

            for e in listeArg:
                if ('-' + nom) == e.nom:
                    if e.isFlag:
                        line.append('_on')
                    else:
                        val = values[0]
                        line.append(val)
                        values.remove(val)

        contraintes.append(line)
    return contraintes

if __name__ == "__main__":
    # creation de la liste des arguments
    listeArguments = createListeArg('arg.txt')
    # affichage
    print("\n affichage de la liste des arguments")
    for element in listeArguments:
        element.toString()

    # creation de la liste des contraintes
    listeContraintes = createListeContraintes('contraintes.txt', listeArguments)
    # affichage
    print("\n affichage de la liste des contraintes")
    print(listeContraintes)
