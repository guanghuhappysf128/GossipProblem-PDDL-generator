""" Writes the domain file.
"""

from utils import depth, nb_agts, generate_all_sequences_up_to, agts
from atomsbase.atom import Atom

""" Generates the visibility predicate for the given depth, of the form
'S-m ?i1 ... ?id ?s'.
"""
def visibility_predicate(d):
    return '(S-' + str(d) + ' ' + ''.join('?i' + str(i) + ' '
                                          for i in range(1, d+1)) + '?s)'


""" Generates the conditional effect corresponding to the given atom in PDDL.
"""
def str_cond_effect(atom):
    # precondition: either i or j knows this atom
    # i and j must be different from the first agent of the atom
    b_diff = ''
    e_diff = ''

    if len(atom.vis_list) > 0:
        b_diff = '(and (not (= ?i ' + str(atom.vis_list[0]) + ')) ' + \
                 '(not (= ?j ' + str(atom.vis_list[0]) + ')) '
        e_diff = ')'

    pre = b_diff + \
          '(or ' + \
          '(and ' + ' '.join(str(eat)
                             for eat in Atom.eatm(Atom.precede_by(atom, ['?i']))) + ') ' + \
          '(and ' + ' '.join(str(eat)
                             for eat in Atom.eatm(Atom.precede_by(atom, ['?j']))) + ')' + \
          ')' + e_diff + ' '

    # effect: any non-introspective sequence of i and j followed by the atom
    add = '(and ' + \
          ' '.join([str(Atom.precede_by(atom, seq))
                    for seq in generate_all_sequences_up_to('?i', '?j', depth() - atom.depth())]) + \
          ')'

    return '(when ' + pre + add + ')'


""" Generates all the conditional effects of a call between two given agents
in the form of a (PDDL) string.
"""
def str_cond_effects_call(base):
    res = ''

    # for every atom of every depth
    for d in range(0, depth()):
        for atom in base.get_atoms_of_depth(d):
            # generate conditional effect
            res += '\t\t\t' + str_cond_effect(atom) + '\n'

    return res


""" Generates the domain file (requirements, predicates and actions).
"""
def print_domain_file(base, file):

    output = ""
    output += ';; Gossip problem - PDDL domain file\n'
    output += ';; depth ' + str(depth()) + ', ' + str(nb_agts()) + ' agents\n\n'

    output += '(define (domain gossip)\n'
    output += '\t(:requirements\n'
    output += '\t\t:strips :disjunctive-preconditions :equality\n'
    output += '\t)\n\n'

    output += '\t(:predicates\n'
    output += '\t\t' + ' '.join(str(atom)
                                 for atom in base.get_atoms_of_depth(0)) + '\n'
    output += '\t\t' + ' '.join(visibility_predicate(d)
                                 for d in range(1, depth()+1)) + '\n'
    output += '\t)\n'

    output += '\n\t(:action call\n'
    output += '\t\t:parameters (?i ?j)\n'
    output += '\t\t:effect (and\n'
    output += str_cond_effects_call(base) + '\t\t)\n'
    output += '\t)\n'

    # create dummy action for FS planner
    output += '\n\t(:action dummy\n'
    output += '\t\t:parameters (?i ?j)\n'
    output += '\t\t:effect (and\n'
    output += '\t\t' + ' '.join(str(atom)
                                 for atom in base.get_atoms_of_depth(0)) + '\t\t)\n'
    output += '\t)\n'
    output += ')\n'

    for i in agts():
        output = output.replace(f"(s{i})",f"(ps{i})")
    agt_str="abcdefgh"
    for i in agts():
        output = output.replace(f" {i} ",f" {agt_str[i-1]} ")
        output = output.replace(f" {i})",f" {agt_str[i-1]})")


    file.write(output)

