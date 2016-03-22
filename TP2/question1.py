# coding : utf-8
import sys
from random import sample


# classe argument : permet de verifier si un argument est un flag, et quelles valeurs sont possibles
class Argument:
    # constructeur
    def __init__(self, name, is_flag, values):
        self.name = name
        self.is_flag = is_flag
        if is_flag:
            self.values = ["_on", "_off"]
        else:
            self.values = values


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
        self.pairs = []
        # permutations of arguments to be tested for a coverage test
        self.permutations = []
        self.cover = []

        # initialisation of object according to files content
        self.create_list_arg()
        self.create_list_constraints()
        self.build_pairs_to_cover()

    def create_list_arg(self):

        """
        extraction of arg_file into the form of a list of Arguments
        """
        try:
            f = open(self.file_args, 'r')
        except FileNotFoundError:
            raise FileNotFoundError("No arguments file found at specified path")

        # split the lines of the file into a list
        lignes = f.readlines()
        f.close()

        for ligne in lignes:
            # drop empty lines
            if ligne.isspace():
                continue
            values = ligne.split()
            # catching the name of the argument described by the current line
            nom = values.pop(0)
            # ignoring help flag
            if nom == '-h':
                continue
            if not values:
                raise Exception("Empty values for argument in argument file, non compatible file")
            # build argument object and add it to the list
            self.arguments.append(Argument(nom, values[0] == 'flag', values))
        # sorting decreasingly according to the number of parameters
        self.arguments.sort(key=lambda x: len(x.values), reverse=True)

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
                            line.append((nom, "_on"))
                        else:
                            try:
                                val = tokens.pop(0)
                            except IndexError:
                                """
                                if conflict in this part it means that the current argument should have been a flag
                                according to the constraint file, but is registered as a binary argument in argument
                                file.
                                """
                                print("--------------------------------------------\n" +
                                      "constraint file inconsistent with arguments.\n" +
                                      "--------------------------------------------", file=sys.stderr)
                                exit(1)

                            line.append((nom, val))
                        break

            # separation of constraints: pairs for direct elimination of pairs to cover, complex for later use
            if arg_ctr == 2:
                self.pair_constraints.append(set(line))
            else:
                self.complex_constraints.append(set(line))

    def build_pairs_to_cover(self):
        """
        function populating the list of pairs that are to be tested for the application
        ( 2-combination of the set of parameters )
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
        :param permutation: permutation to which we want to add a new (argument, value) couple
        :param exploration_window: the number of valid arguments for this set to be compared
        :return: the most effective couple in term of matching pairs in pairs yet to cover
        """
        # select_ctr: number of valid args tested for the current permutation
        select_ctr = 0
        # number of pairs matched by the most effective valid new argument
        max_sat = 0
        # most effective new arg to add to the permutation
        selected = None
        # list of arg names already presents in the permutation
        permutation_args = [argval[0] for argval in permutation]

        # foreach pairs (set of two (arg, val) tuples) non matched
        for pair in self.pairs:
            list_pair = list(pair)
            """
            if the first (arg, val) in pair is in the permutation, and the second argument isn't set yet in the
            permutation, or vice versa, add temporarily the argument to check if the new member doesn't make the
            permutation illegal according to constraints, if not then evaluate the effectiveness on the reduction
            of unmatched pairs number. save the best score and (arg, val) corresponding at each iteration.
            """
            if (list_pair[0] in permutation and list_pair[1][0] not in permutation_args) or \
                    (list_pair[1] in permutation and list_pair[0][0] not in permutation_args):
                first = list_pair[0] in permutation
                permutation_tmp = set(permutation)
                permutation_tmp.add(list_pair[first])
                if not self.is_transgressing_constraint(permutation_tmp):
                    sat = self.eval_permutation(permutation_tmp)
                    if sat > max_sat:
                        max_sat = sat
                        selected = list_pair[first]
                    select_ctr += 1
            # break when we reached the depth of exploration we specified
            if select_ctr >= exploration_window:
                break
        return selected

    def build_args_permutations_grow(self, exploration_window=10):
        """
        first phase of permutation set generation, building a covering set of possibly incomplete arguments permutations
        :param exploration_window: argument propagation to get_valid_arg
        """
        # while all the 2-combination of arguments isn't matched
        while self.pairs:
            # if there is already a permutation in the set, try to expand it, else pick the first unmatched pair
            if self.permutations:
                permutation_seed = self.permutations.pop(0)
            else:
                permutation_seed = self.pairs.pop(0)
                permutation_seed = set(permutation_seed)
            # if the permutation isn't complete try to expand it, else add it to the covering set
            if len(permutation_seed) < len(self.arguments):
                new_arg = self.get_valid_arg(permutation_seed, exploration_window)
                # if the permutation isn't growing anymore, store it in queue of self.permutation for later treatment
                if new_arg is None:
                    self.permutations.append(permutation_seed)
                    self.permutations.insert(0, set(self.pairs.pop(0)))
                    continue
                permutation_seed.add(new_arg)
                self.delete_matched_pairs(permutation_seed)
                self.permutations.insert(0, permutation_seed)
            else:
                self.cover.append(permutation_seed)

    def build_args_permutations(self, exploration_window=10, recombination_threshold=10, repetitions=3):
        """
        method building the set of covering permutations

        :param exploration_window: number of valid arguments to be tested during the growing of permutations at
        each iteration
        :param recombination_threshold: threshold size at which the heuristic tries to recombine a permutation with
        another smaller one
        :param repetitions: number of passes of welding_short_permutations
        """
        self.build_args_permutations_grow(exploration_window)
        self.weld_short_permutations(recombination_threshold, repetitions)
        # queueing the incomplete permutations to the cover table
        self.cover.extend(self.permutations)
        self.permutations.clear()

    def weld_short_permutations(self, recombination_threshold, repetitions):
        """
        try to combine all the permutations shorter than a certain size, trying to reduce the final set
        :param recombination_threshold: threshold size
        :param repetitions: number of passes on all the permutations
        """
        # multiple passes for more compact set of permutations
        for _ in range(repetitions):
            """
            foreach incomplete permutation shorter than threshold recombine with another permutation not containing
            any of its own arguments
            """
            for permutation1 in self.permutations:
                if len(permutation1) < recombination_threshold:
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
        """
        to be executed at the end of build_args_permutations: completes non significant missing arguments of
        permutations with random values
        """

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
        generation (or overwrite) of the file (specified in self.const_file) containing the set of commands.
        """
        f = open(self.file_commands, 'w')
        for permutation in self.cover:
            command = self.app_name
            for (arg, val) in permutation:
                # if value is _off - meaning the absence of flag - skip to the next argument
                if val == '_off':
                    continue
                # if value is _on only put the flag name
                elif val == '_on':
                    command += " " + arg
                # case of negative value of negative numeric argument (- prefix messing with bash)
                elif val[0] == '-':
                    command += ' {} "{}"'.format(arg, val)
                else:
                    command += " {} {}".format(arg, val)

            command += '\n'
            f.write(command)

    def build_pairs_from_command(self, command):
        """
        regenerate pairs covered by a command, for coverage control
        :param command: said command
        :return : the pairs covered by the command
        """

        # args listed in the command
        args = []

        # generation of couples (arg, val) from the command
        if not command.isspace():
            tokens = command.split()
            # first token is app_name
            tokens.pop(0)
            # for all arguments in command build (arg, val) couple
            while tokens:
                nom = tokens.pop(0)
                for e in self.arguments:
                    if nom == e.name:
                        if e.is_flag:
                            args.append((nom, "_on"))
                        else:
                            val = tokens.pop(0)
                            # purge of quotes added on arguments values starting with "-"
                            val = val.replace('\"', '')
                            args.append((nom, val))
                        break
            # adjunction of non present flags
            args_names = [nom for nom, val in args]
            for argument in self.arguments:
                if argument.is_flag and argument.name not in args_names:
                    args.append((argument.name, "_off"))
        # 2-combination of (arg, val) couples == pairs covered by the command
        pairs = []
        while args:
            arg1 = args.pop(0)
            for arg2 in args:
                pair = {arg1, arg2}
                if not self.is_transgressing_constraint(pair):
                    pairs.append({arg1, arg2})
        return pairs

    def check_cover(self):
        """
        control method to ensure that the set of commands generated is pairwise covering
        """
        # regenerate pairs to cover
        self.build_pairs_to_cover()
        try:
            f = open(self.file_commands, 'r')
        except FileNotFoundError:
            print("Problem occurred between generation and checking:\n"
                  " commands_file has been deleted or made unreadable", file=sys.stderr)
        commands = f.readlines()
        # foreach commands in the commands_file regenerate pairs covered by it, and delete them from the pairs to cover
        for command in commands:
            pairs = self.build_pairs_from_command(command)
            for pair in pairs:
                try:
                    while True:
                        self.pairs.remove(pair)
                except ValueError:
                    pass
        # if remaining pairs, generation is faulty
        if self.pairs:
            print("the command set generated isn't pairwise covering", file=sys.stderr)
            exit(1)


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
    thresh = 9 * len(ts.arguments) / 10
    ts.build_args_permutations(exploration_window=10, recombination_threshold=thresh)
    ts.complete_short_permutations()
    ts.generate_commands()
    ts.check_cover()
