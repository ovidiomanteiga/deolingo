
import sys
import clingo
import clingo.ast as ast
from typing import Callable


ex0 = """
%&forbidden{-exercise}.
&not_forbidden{exercise}.
%&obligatory{exercise}.
%&forbidden{smoke}.
%&obligatory{-smoke}.
%&obligatory{-smoke; exercise}.
%&forbidden{smoke; -exercise}.
%-exercise.
%smoke.
"""

ex1 = """
park :- not &forbidden{park}.
"""

ex2 = """
&obligatory{work} :- not &not_obligatory{work}.
&not_obligatory(work) :- weekend.
-weekend.
-work.
"""

ex3 = """
&obligatory{fight}.
&forbidden{fight}.
"""

ex4 = """
&forbidden{walk}.
&obligatory{walk_right} :- walk.
walk :- walk_right.
&obligatory{walk} :- &obligatory{walk_right}.
walk.
walk_right.
"""

ex5 = """
&forbidden{fence} :- not &not_forbidden{fence}.
&obligatory{white} :- fence.%, &forbidden{fence}.
&not_forbidden{fence} :- sea.
fence.
sea.
"""

deolingo_theory = """
#theory deo {
    deontic_term { 
        & : 2, binary, left;
        - : 3, unary;
        ~ : 3, unary;
        | : 1, binary, left
    };
    &obligatory/0 : deontic_term, any;
    &forbidden/0 : deontic_term, any;
    &not_obligatory/0 : deontic_term, any;
    &not_forbidden/0 : deontic_term, any
}.
"""


def deontic_transform(ctl, prog=ex0):
    ctl.configuration.solve.models = 0
    prog += deolingo_theory
    prog += "_deolingo_violation(X) :- _deolingo_obligatory(X), -_deolingo_holds(X)."
    prog += "_deolingo_violation(X) :- _deolingo_forbidden(X), _deolingo_holds(X)."
    prog += "_deolingo_fulfilled(X) :- _deolingo_obligatory(X), _deolingo_holds(X)."
    prog += "_deolingo_fulfilled(X) :- _deolingo_forbidden(X), -_deolingo_holds(X)."
    prog += "_deolingo_obligatory(X) :- _deolingo_forbidden(-X)."
    prog += "_deolingo_forbidden(X) :- _deolingo_obligatory(-X)."
    prog += "_deolingo_implicit_permission(X) :- not _deolingo_forbidden(X), _deolingo_deontic(X)."
    prog += "_deolingo_explicit_permission(X) :- -_deolingo_forbidden(X), _deolingo_deontic(X)."
    prog += ":- _deolingo_obligatory(X), _deolingo_forbidden(X), not _deolingo_holds(X), not -_deolingo_holds(X)."
    ctl.add("base", [], prog)
    # Ground the program
    ctl.ground([("base", [])])
    # Access parsed AST of the program to add rules for the deontic operators
    for theory_atom in ctl.theory_atoms:
        is_deontic = False
        theory_atom_name = theory_atom.term.name
        for theory_atom_element in theory_atom.elements:
            for theory_atom_element_term in theory_atom_element.terms:
                is_negated = theory_atom_element_term.name == "-"
                theory_atom_element_term_name = theory_atom_element_term.arguments[0].name if is_negated else theory_atom_element_term.name
                if theory_atom_name == "obligatory":
                    ctl.add("base", [], f"_deolingo_obligatory({theory_atom_element_term}).")
                    is_deontic = True
                elif theory_atom_name == "forbidden":
                    ctl.add("base", [], f"_deolingo_forbidden({theory_atom_element_term}).")
                    is_deontic = True
                elif theory_atom_name == "not_obligatory":
                    ctl.add("base", [], f"-_deolingo_obligatory({theory_atom_element_term}).")
                    is_deontic = True
                elif theory_atom_name == "not_forbidden":
                    ctl.add("base", [], f"-_deolingo_forbidden({theory_atom_element_term}).")
                    is_deontic = True
                if is_deontic:
                    #ctl.add("base", [], f":- _deolingo_obligatory_({theory_atom_element_term_name}), _deolingo_forbidden_({theory_atom_element_term_name}), not {theory_atom_element_term_name}, not -{theory_atom_element_term_name}.")
                    ctl.add("base", [], f"_deolingo_holds({theory_atom_element_term_name}) :- {theory_atom_element_term_name}.")
                    ctl.add("base", [], f"-_deolingo_holds({theory_atom_element_term_name}) :- -{theory_atom_element_term_name}.")
                    ctl.add("base", [], f"_deolingo_deontic({theory_atom_element_term_name}).")
    # Ground the program again after adding deontic rules
    ctl.ground([("base", [])])


def rewrite_atoms(atoms):
    """
    Rewrites the atom by removing the prefix '_deolingo_' if present.
    """
    rewritten_atoms = []
    for atom in atoms:
        str_atom = str(atom)
        if "_deolingo_deontic" in str_atom or "_deolingo_holds" in str_atom:
            continue
        elif str_atom.startswith("_deolingo_"):
            rewritten_atoms.append(str_atom[len("_deolingo_"):])
        elif str_atom.startswith("-_deolingo_"):
            rewritten_atoms.append("-" + str_atom[len("-_deolingo_"):])
        else:
            rewritten_atoms.append(str_atom)
    return rewritten_atoms


class DeolingoApplication(clingo.Application):
    """
    Application object as accepted by clingo.clingo_main().
    Rewrites the incoming deontic logic programs into deontic ASP programs and solves them.
    """
    def __init__(self):
        """
        Initializes the application setting the program name.
        See clingo.clingo_main().
        """
        self.program_name = "deolingo"
        self.version = "0.0.1'"


    def print_model(self, model: clingo.Model, printer: Callable[[], None] = None):
        """
        Prints the atoms of the given model.
        This function is called for each model of the problem.
        """
        atoms = model.symbols(shown=True)
        rewritten_atoms = rewrite_atoms(atoms)
        print("Answer: " + str(rewritten_atoms))


    def main(self, prg, files):
        """
        Implements the incremental solving loop.
        This function implements the Application.main() function as required by
        clingo.clingo_main().
        """
        deontic_transform(prg)
        prg.solve(on_model=None, async_=False)


def rewrite_model(model: clingo.Model):
    """
    Rewrites the atoms of the given model by removing the prefix '_deolingo_' if present.
    """
    atoms = model.symbols(shown=True)
    rewritten_atoms = rewrite_atoms(atoms)
    return rewritten_atoms


def run_deolingo(prog=""):
    ctl = clingo.Control()
    deontic_transform(ctl, prog)
    models = []
    def on_model(m):
        nonlocal models
        models += [rewrite_model(m)]
    solved = ctl.solve(on_model=on_model)
    for m in models:
        print("Answer: " + str(m))
    return models


def main():
    """
    Run the deolingo application.
    """
    sys.exit(int(clingo.clingo_main(DeolingoApplication(), sys.argv[1:])))


if __name__ == '__main__':
    main()
