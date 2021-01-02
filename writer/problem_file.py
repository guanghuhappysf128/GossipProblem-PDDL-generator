""" Writes the problem file.
"""

from utils import depth, agts, nb_agts

""" Generates the string representing the goal.
"""
def str_goal(base):
    res = ''

    for d in range(0, depth()+1):
        res += '\t\t' + base.repr_depth(d) + '\n'

    return res


""" Generates the problem file (agents, initial state and goal).
"""
def print_problem_file(base, file):
    output = ""
    output += ';; Gossip problem - PDDL problem file\n'
    output += ';; depth ' + str(depth()) + ', ' + str(nb_agts()) + ' agents\n\n'

    output += '(define (problem gossip)\n'
    output += '\t(:domain gossip)\n\n'

    output += '\t(:objects ' + ' '.join(str(i) for i in agts()) + ' ' +' '.join('s'+str(i) for i in agts())+ ')\n\n'

    output += '\t(:init\n'
    output += '\t\t' + ' '.join(str(atom) for atom in base.get_atoms_of_depth(0)) + '\n'
    output += '\t\t' + ' '.join(str(atom) for atom in base.get_atoms_of_depth(1)
                            if atom.is_initial()) + '\n'
    output += '\t)\n\n'

    output += '\t(:goal (and\n'
    output += str_goal(base) + '\t))\n'

    output += ')\n'

    for i in agts():
        output = output.replace(f"(s{i})",f"(ps{i})")
    
    agt_str="abcdefgh"
    for i in agts():
        output = output.replace(f" {i} ",f" {agt_str[i-1]} ")
        output = output.replace(f" {i})",f" {agt_str[i-1]})")

    file.write(output)    