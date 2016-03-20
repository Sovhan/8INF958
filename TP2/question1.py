# coding : utf-8
import sys
from random import sample


# classe argument : permet de verifier si un argument est un flag, et quelles valeurs sont possibles
class Argument:
    # constructeur
    def __init__(self, name, is_flag, values):
        self.name = name
        self.is_flag = is_flag
        self.values = values

    # affichage : utile pour le debug
    def toString(self):
        print()
        print("**********")
        print("nom :")
        print(self.name)
        print("is flag :")
        print(self.is_flag)
        print("values :")
        print(self.values)
        print("**********")
        print()


class TestSet:
    """
    class constructing a set of permutations of arguments to call on an application to execute a pairwise
    cover test.
    """

    def __init__(self, app_name, file_args, file_consts, file_commands):
        """
        constructor
        :param app_name: the string to call to execute the app without arguments
        :param file_args: path to file containing the possible arguments for the app and their values
        :param file_consts: path to file containing the constraints defining forbidden combinations
        of arguments and values in conjunction.
        """
        self.app_name = app_name
        if self.app_name.isspace():
            raise Exception("app_name empty")
        self.file_args = file_args
        self.file_consts = file_consts
        self.file_commands = file_commands
        self.arguments = []
        # constraint separation, between binary constraints, and N-ary constraints
        self.complex_constraints = []
        self.pair_constraints = []
        # pairs still to be satisfied
        self.init_pairs = []
        self.pairs = []
        # permutations of arguments to be tested for a coverage test
        self.permutations = []
        self.cover = []

        # initialisation of object
        self.create_list_arg()
        self.create_list_constraints()
        self.build_pairs_to_cover()
        self.build_args_permutations()

    # conversion du fichier texte en tableau d'argument
    def create_list_arg(self):
        """
        extraction of arg_file into the form of a list of Arguments
        """
        # recuperation du fichier d'arguments
        try:
            f = open(self.file_args, 'r')
        except FileNotFoundError:
            raise FileNotFoundError("No arguments file found at specified path")

        lignes = f.readlines()
        f.close()

        for ligne in lignes:
            if ligne.isspace():
                continue
            values = ligne.split()
            nom = values.pop(0)
            # ignoring help flag
            if nom == '-h':
                continue
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
            if constraint.isspace():
                continue
            tokens = constraint.split()
            line = []
            arg_ctr = 0
            # on traite chacune des valeurs de la contrainte :
            # - si c'est un flag, on lui ajoute la valeur _on
            # - sinon, on recupere la valeur fournie
            while tokens:
                nom = tokens.pop(0)
                arg_ctr += 1
                for e in self.arguments:
                    if ('-' + nom) == e.name:
                        if e.is_flag:
                            line.append((nom, "flag"))
                        else:
                            try:
                                val = tokens.pop(0)
                            except IndexError:
                                print("--------------------------------------------\n" +
                                      "constraint file inconsistent with arguments.\n" +
                                      "--------------------------------------------", file=sys.stderr)
                                exit(1)

                            line.append((nom, val))
                        break

            if arg_ctr == 2:
                self.pair_constraints.append(set(line))
            else:
                self.complex_constraints.append(set(line))

    def build_pairs_to_cover(self):
        """
        function populating the list of pairs that are to be tested for the application
        """
        argc = len(self.arguments)
        for i in range(argc):
            for value1 in self.arguments[i].values:
                for j in range(i + 1, argc):
                    for value2 in self.arguments[j].values:
                        self.pairs.append({(self.arguments[i].name, value1), (self.arguments[j].name, value2)})

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
        :param exploration_window: the number of valid arguments for this set to be compared
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
                first = list_pair[0] in permutation
                permutation.add(list_pair[first])
                if not self.is_transgressing_constraint(permutation):
                    sat = self.eval_permutation(permutation)
                    if sat > max_sat:
                        max_sat = sat
                        selected = list_pair[first]
                    select_ctr += 1
                permutation.remove(list_pair[first])
            if select_ctr >= exploration_window:
                break
        return selected

    def generate_pairs_from_permutation(self, permutation):
        """
        regeneration of pairs covered by a permutation
        :param permutation:  set of (arg, val)
        :return:
        """
        while permutation:
            pair_tmp = permutation.pop()
            for pair in permutation:
                self.pairs.append({pair_tmp, pair})

    def build_args_permutations_grow(self):
        while self.pairs:
            if self.permutations:
                permutation_seed = self.permutations.pop(0)
            else:
                permutation_seed = self.pairs.pop(0)
                permutation_seed = set(permutation_seed)
            if len(permutation_seed) < len(self.arguments):
                new_arg = self.get_valid_arg(permutation_seed)
                if new_arg is None:
                    self.permutations.append(permutation_seed)
                    self.permutations.insert(0, set(self.pairs.pop(0)))
                    continue
                permutation_seed.add(new_arg)
                self.delete_matched_pairs(permutation_seed)
                self.permutations.insert(0, permutation_seed)
            else:
                self.cover.append(permutation_seed)

    def refine_permutations(self, grain):
        """
        method to reprocess the permutations that are shorter than a certain size
        :param grain: mail size
        """
        for permutation in self.permutations:
            if len(permutation) < grain:
                self.generate_pairs_from_permutation(permutation)
            else:
                self.cover.append(permutation)
            self.permutations.remove(permutation)

    def build_args_permutations(self):
        """
        method building the set of covering permutations
        """
        self.build_args_permutations_grow()
        self.weld_short_permutations(9 * len(self.arguments) / 10)
        self.cover.extend(self.permutations)
        self.permutations.clear()

    def weld_short_permutations(self, grain, repetitions=3):
        """
        try to combine all the permutations shorter than a certain size, trying to reduce the final set
        :param grain: threshold size
        :param repetitions: number of passes on all the permutations
        """
        for _ in range(repetitions):
            for permutation1 in self.permutations:
                if len(permutation1) < grain:
                    args1 = set([arg for (arg, val) in permutation1])
                    for permutation2 in self.permutations:
                        args2 = set([arg for (arg, val) in permutation2])
                        if args1.isdisjoint(args2):
                            permutation_tmp = permutation1.union(permutation2)
                            if not self.is_transgressing_constraint(permutation_tmp):
                                self.permutations.append(permutation_tmp)
                                self.permutations.remove(permutation1)
                                self.permutations.remove(permutation2)
                            break

    def complete_short_permutations(self):

        for permutation in self.cover:
            args_in = [arg for arg, val in permutation]
            if len(permutation) < len(self.arguments):
                for argument in self.arguments:
                    if argument.name not in args_in:
                        if not argument.is_flag:
                            permutation.add((argument.name, sample(argument.values, 1)[0]))
                            args_in.append(argument.name)

    def generate_commands(self):
        """
        generation (or overwrite) of the file containing the set of commands.
        """
        f = open(self.file_commands, 'w')
        for permutation in self.cover:
            command = self.app_name
            for (arg, val) in permutation:
                if val == 'flag':
                    command += " " + arg
                elif val.isnumeric() and int(val) >= 0:
                    command += " {} {}".format(arg, val)
                elif val.isnumeric() and int(val) < 0:
                    command += ' {} "{}"'.format(arg, val)
                elif val[0] == '-':
                    command += ' {} "{}"'.format(arg, val)
                else:
                    command += " {} {}".format(arg, val)

            command += '\n'
            f.write(command)

    def build_pairs_from_command(self, command):
        args = []
        if not command.isspace():
            tokens = command.split()
            # first token is app_name
            tokens.pop(0)
            while tokens:
                nom = tokens.pop(0)
                for e in self.arguments:
                    if nom == e.name:
                        if e.is_flag:
                            args.append((nom, "flag"))
                        else:
                            val = tokens.pop(0)
                            val = val.replace('\"', '')
                            args.append((nom, val))
                        break
        pairs = []
        while args:
            arg1 = args.pop(0)
            for arg2 in args:
                pair = {arg1, arg2}
                if not self.is_transgressing_constraint(pair):
                    pairs.append({arg1, arg2})
        return pairs

    def check_cover(self):
        self.build_pairs_to_cover()
        self.pairs.extend(self.init_pairs)
        self.init_pairs.clear()
        f = open(self.file_commands, 'r')
        commands = f.readlines()
        for command in commands:
            pairs = self.build_pairs_from_command(command)
            for pair in pairs:
                try:
                    while True:
                        self.pairs.remove(pair)
                except ValueError:
                    pass
        if self.pairs:
            print(len(self.pairs))
            raise Exception("the command set generated isn't pairwise covering")


def usage():
    print("question1.py <app_name> <argument_file> <constraint_file> <command_output_file>")
    print("with:")
    print("<app_name> = path of application invocation without parameters")
    print("<argument_file> = file containing the arguments and their possible values")
    print('<constraint_file> = file containing the constraints to apply on pairwise cover')
    print("<command_output_file> = file regrouping all the commands generated")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        usage()
        exit(1)

    ts = TestSet(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    ts.generate_commands()
    ts.check_cover()
    ts.complete_short_permutations()
    ts.generate_commands()
    ts.check_cover()
