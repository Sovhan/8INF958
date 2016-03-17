# classe argument : permet de verifier si un argument est un flag, et quelles valeurs sont possibles
class Argument:
    # constructeur
    def __init__(self, name, isFlag, values):
        self.name = name
        self.isFlag = isFlag
        if isFlag:
            self.values = ['_on', '_off']
        else:
            self.values = values

    # affichage : utile pour le debug
    def toString(self):
        print()
        print("**********")
        print("nom :")
        print(self.name)
        print("is flag :")
        print(self.isFlag)
        print("values :")
        print(self.values)
        print("**********")
        print()


class TestSet:
    """
    class constructing a set of permutations of arguments to call on an application to execute a pairwise
    cover test.
    """
    def __init__(self, app_name, file_args, file_consts):
        """
        constructor
        :param app_name: the string to call to execute the app without arguments
        :param file_args: file containing the possible arguments for the app and their values
        :param file_consts: file containing the constraints defining forbidden combinations
        of arguments and values.
        """
        self.app_name = app_name
        self.file_args = file_args
        self.file_consts = file_consts
        self.arguments = []
        self.constraints = []
        self.pairs = set()
        self.permutations = set()

    # conversion du fichier texte en tableau d'argument
    def create_list_arg(self):
        # recuperation du fichier d'arguments
        # f = open('arg.txt','r')
        f = open(self.file_args, 'r')
        lignes = f.readlines()
        f.close()

        for ligne in lignes:
            values = ligne.split()
            nom = values.pop(0)
            self.arguments.append(Argument(nom, values[0] == 'flag', values))

        self.arguments.sort(key=lambda x: len(x.values), reverse=True)

    # conversion du fichier texte en tableau de contraintes
    # mise en forme des contraintes : si la variable est un flag on ajoute sa valeur _on
    # au final on aura juste une suite de variable / valeur facile a utiliser
    def create_list_constraints(self):
        """
        conversion of the constraint file, taking conjunctions expressed in the file
        to a list of constraints on arguments permutations, expressed in tuples of form
        (arg1, val1, arg2, val2...) in which all the arguments arg of value val are incompatible altogether
        """

        # recuperation du fichier de contraintes
        f = open(self.file_consts, 'r')
        constraints = f.readlines()
        f.close()

        # on traite chaque contrainte puis on l'ajoute a la liste des contraintes
        for constraint in constraints:
            tokens = constraint.split()
            line = []
            # on traite chacune des valeurs de la contrainte :
            # - si c'est un flag, on lui ajoute la valeur _on
            # - sinon, on recupere la valeur fournie
            while tokens:
                nom = tokens.pop(0)

                for e in self.arguments:
                    if ('-' + nom) == e.name:
                        if e.isFlag:
                            line.append((nom, "_on"))
                        else:
                            val = tokens.pop(0)
                            line.append((nom, val))

            self.constraints.append(line)

    # def replace_invalid_permutations(self, pairs, constraints):
    #     for arguments in pairs:
    #         for constraint in constraints:
    #             if constraint in arguments:
    #                 replace_permutation(arguments, constraints)

    def delete_matched_pairs(self, permutation_seed):
        """
        deletion of pairs that are matched by a set of couple (argument, value)
        :param permutation_seed: set of couple (argument, value) to evaluate for the match
        """
        for pair in self.pairs:
            if pair.issubset(permutation_seed):
                print(pair)
                self.pairs.remove(pair)

    def create_args_permutations(self):
        init_pairs = self.pairs_to_cover()
        while init_pairs:
            permutation_seed = list(init_pairs.pop())
            permutation_seed.append()
            permutation_seed = tuple(permutation_seed)
            self.delete_matched_pairs(permutation_seed)

    def pairs_to_cover(self):
        """
        function populating the set of pairs that are to be tested for the application
        :return: the constructed set() of pairs that will be the seed of the set of permutations
        in which elements of form (arg1, val1, arg2, val2)
        """

        init_pairs = set()
        argc = len(self.arguments)
        for value1 in self.arguments[0].values:
                for k in range(1, argc):
                    for value2 in self.arguments[k].values:
                        init_pairs.add(
                            ((self.arguments[0].name, value1),
                             (self.arguments[k].name, value2))
                        )
        for i in range(1, argc):
            for value1 in self.arguments[i].values:
                for j in range(i+1, argc):
                    for value2 in self.arguments[j].values:
                        self.pairs.add(
                            ((self.arguments[i].name, value1),
                             (self.arguments[j].name, value2))
                        )
        print(init_pairs, self.pairs)
        return init_pairs


if __name__ == "__main__":
    ts = TestSet("plop", "arg.txt", "contraintes.txt")
    # creation de la liste des arguments
    ts.create_list_arg()
    ts.create_list_constraints()
    # affichage
    # print("\n affichage de la liste des arguments")
    # for element in ts.arguments:
    #     element.toString()
    #
    # # affichage
    # print("\n affichage de la liste des contraintes")
    # print(ts.constraints)

    ts.pairs_to_cover()
