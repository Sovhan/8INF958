# coding : utf-8
import sys

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
        :param file_args: path to file containing the possible arguments for the app and their values
        :param file_consts: path to file containing the constraints defining forbidden combinations
        of arguments and values in conjunction.
        """
        self.app_name = app_name
        self.file_args = file_args
        self.file_consts = file_consts
        self.arguments = []
        # constraint separation, between binary constraints, and N-ary constraints
        self.complex_constraints = []
        self.pair_constraints = []
        # pairs still to be satisfied
        self.pairs = []
        # permutations of arguments to be tested for a coverage test
        self.permutations = []

    # conversion du fichier texte en tableau d'argument
    def create_list_arg(self):
        """

        :return:
        """
        # recuperation du fichier d'arguments
        try:
            f = open(self.file_args, 'r')
        except FileNotFoundError:
            raise FileNotFoundError("No arguments file found at specified path")

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
        try:
            f = open(self.file_consts, 'r')
        except FileNotFoundError:
            print("no constraint file found")
            return

        constraints = f.readlines()
        f.close()

        # on traite chaque contrainte puis on l'ajoute a la liste des contraintes
        for constraint in constraints:
            tokens = constraint.split()
            line = set()
            arg_ctr = 0
            # on traite chacune des valeurs de la contrainte :
            # - si c'est un flag, on lui ajoute la valeur _on
            # - sinon, on recupere la valeur fournie
            while tokens:
                nom = tokens.pop(0)
                arg_ctr += 1
                for e in self.arguments:
                    if ('-' + nom) == e.name:
                        if e.isFlag:
                            line.add((nom, "_on"))
                        else:
                            val = tokens.pop(0)
                            line.add((nom, val))
                        break

            if arg_ctr == 2:
                self.pair_constraints.append(frozenset(line))
            else:
                self.complex_constraints.append(frozenset(line))

    def delete_matched_pairs(self, permutation):
        """
        deletion of pairs that are matched by a set of couple (argument, value)
        :param permutation: set of couple (argument, value) to evaluate for the match
        """
        for pair in self.pairs:
            if pair.issubset(permutation):
                self.pairs.remove(pair)

    def is_transgressing_constraint(self, permutation):
        """
        tests a permutation for constraint infringement
        :param permutation: permutation to test
        :return: True if the permutation is invalid regarding the constraints, False else
        """
        for constraint in self.pair_constraints:
            if constraint.issubset(permutation):
                return True
        for constraint in self.complex_constraints:
            if constraint.issubset(permutation):
                return True
        return False

    def eval_permutation(self, permutation):
        """
        :param permutation: (argument, value)list permutation
        :return: number of yet unmatched pairs ((arg1, val1), (arg2, val2)) matched by this permutation.
        """
        return sum([pair <= permutation for pair in self.pairs])

    def get_valid_arg(self, permutation, exploration_window=10):
        """
        :param permutation:
        :param exploration_window: the set of valid arguments for this set to be compared
        :return:
        """
        select_ctr = 0
        max_sat = 0
        selected = None
        permutation_args = [argval[0] for argval in permutation]
        for pair in self.pairs:
            list_pair = list(pair)
            if (list_pair[0] in permutation and list_pair[1][0] not in permutation_args) or \
               (list_pair[1] in permutation and list_pair[0][0] not in permutation_args):
                # permutation is already a set but we need a deepcopy
                permutation_tmp = permutation
                first = list_pair[0] in permutation
                if first:
                    permutation_tmp.add(list_pair[1])
                    permutation_args.append(list_pair[1][0])
                else:
                    permutation_tmp.add(list_pair[0])
                    permutation_args.append(list_pair[0][0])
                if not self.is_transgressing_constraint(permutation_tmp):
                    sat = self.eval_permutation(permutation_tmp)
                    if sat > max_sat:
                        max_sat = sat
                        selected = list_pair[first]
                    select_ctr += 1
            if select_ctr >= exploration_window:
                break
        return selected

    def build_args_permutations(self):
        """
        method building the set of covering permutations
        """
        init_perms = self.pairs_to_cover()
        permutations_tmp = []
        while self.pairs:
            if init_perms:
                permutation_seed = set(init_perms.pop())
                new_arg = self.get_valid_arg(permutation_seed)
                if new_arg is None:
                    permutations_tmp.append(permutation_seed)
                    continue
                permutation_seed.add(new_arg)
                self.delete_matched_pairs(permutation_seed)
                permutations_tmp.append(permutation_seed)
            else:
                if permutations_tmp:
                    permutation_seed = set(permutations_tmp.pop(0))
                else:
                    permutation_seed = set(self.pairs.pop(0))
                if len(permutation_seed) < len(self.arguments):
                    new_arg = self.get_valid_arg(permutation_seed)
                    if new_arg is None:
                        permutations_tmp.append(permutation_seed)
                        permutations_tmp.insert(0, set(self.pairs.pop(0)))
                        continue
                        # raise Exception(" error in rolling phase of permutations build")
                    permutation_seed.add(new_arg)
                    self.delete_matched_pairs(permutation_seed)
                    permutations_tmp.append(permutation_seed)
                else:
                    self.permutations.append(permutation_seed)

        self.permutations.extend(permutations_tmp)

    def pairs_to_cover(self):
        """
        function populating the set of pairs that are to be tested for the application
        :return: the constructed set() of pairs that will be the seed of the set of permutations
        in which elements of form (arg1, val1, arg2, val2), and defines the set of pairs remaining.
        """
        init_pairs = set()
        argc = len(self.arguments)

        for i in range(argc):
            for value1 in self.arguments[i].values:
                for j in range(i + 1, argc):
                    for value2 in self.arguments[j].values:
                        if i == 0 and j == 1:
                            init_pairs.add(frozenset([(self.arguments[0].name, value1),
                                                      (self.arguments[1].name, value2)])
                                           )
                        else:
                            self.pairs.append(frozenset([(self.arguments[i].name, value1),
                                                         (self.arguments[j].name, value2)])
                                              )

        return init_pairs


def generate_commands(test_set, commands_file):

    f = open(commands_file, 'w')
    for permutation in test_set.permutations:
        command = test_set.app_name
        for (arg, val) in permutation:
            if val == '_on':
                command += " " + arg
            elif val == '_off':
                continue
            else:
                command += " {} {}".format(arg, val)
        command += '\n'
        f.write(command)


def usage():
    print("question1.py <app_name> <argument_file> <constraint_file> <command_output_file>")


if __name__ == "__main__":
    # if sys.argc != 5:
    #     usage()
    #     exit(1)
    #
    ts = TestSet(sys.argv[1], sys.argv[2], sys.argv[3])
    # creation de la liste des arguments
    ts.create_list_arg()
    ts.create_list_constraints()
    ts.build_args_permutations()
    generate_commands(ts, sys.argv[4])
