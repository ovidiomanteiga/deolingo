
import sys
import clingo
import clingo.ast as ast
from typing import Callable
from clingo.ast import Transformer, Variable, parse_string, SymbolicAtom, ProgramBuilder


ex0 = """
%&forbidden{smoke;kk}.
&forbidden{smoke}.
%&forbidden{-smoke}.
a :- &forbidden{smoke;kk}, p.
%b :- &obligatory{exercise;ff}, q.
%a1 :- &not_forbidden{smoke}, p.
%b2 :- &not_obligatory{exercise}, q.
"""

ex0_0 = """
%&forbidden{-exercise}.
%&not_forbidden{exercise}.
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
&not_obligatory{work} :- weekend.
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


class DeonticTransformer(Transformer):

    def map_deontic_atoms(self, sequence):
        new_sequence = []
        if not sequence:
            return sequence
        for lit in sequence:
            if lit.ast_type != ast.ASTType.Literal:
                new_sequence.append(lit)
                continue
            if lit.atom.ast_type == ast.ASTType.TheoryAtom and lit.atom.term.name in ["forbidden", "obligatory", "not_forbidden", "not_obligatory"]:
                is_negated = lit.atom.term.name in ["not_forbidden", "not_obligatory"]                    
                for el in lit.atom.elements:
                    is_obligatory = lit.atom.term.name in ["obligatory", "not_obligatory"]
                    new_name = "obligatory" if is_obligatory else "forbidden"
                    new_name = ("-" if is_negated else "") + "_deolingo_" + new_name
                    new_atom = ast.SymbolicAtom(ast.Function(lit.atom.term.location, new_name, el.terms, False))
                    new_lit = ast.Literal(lit.location, lit.sign, new_atom)
                    new_sequence.append(new_lit)
            else:
                new_sequence.append(lit)
        return new_sequence

    def visit_sequence(self, sequence):
        return self.map_deontic_atoms(sequence)

    def visit_TheoryAtom(self, atom):
        if atom.term.name in ["forbidden", "obligatory", "not_forbidden", "not_obligatory"]:
            is_negated = atom.term.name in ["not_forbidden", "not_obligatory"] 
            is_obligatory = atom.term.name in ["obligatory", "not_obligatory"]
            new_name = "obligatory" if is_obligatory else "forbidden"
            if len(atom.elements) == 1:                   
                new_name = ("-" if is_negated else "") + "_deolingo_" + new_name
                new_atom = ast.Literal(atom.term.location, ast.Sign.NoSign, ast.SymbolicAtom(ast.Function(atom.term.location, new_name, atom.elements[0].terms, False)))
                return new_atom
        return atom


def deontic_transform(ctl, prog=ex5):
    ctl.configuration.solve.models = 0
    prog += deolingo_theory
    #ctl.add("base", [], prog)
    # Ground the program
    #ctl.ground([("base", [])])
    def callback(bld, stm):
        tstm = dt(stm)
        print(str(tstm))
        bld.add(tstm)   
    with ProgramBuilder(ctl) as bld:
        ctl2 = clingo.Control()
        ctl2.add("base", [], prog)
        ctl2.ground([("base", [])])
        # Access parsed AST of the program to add rules for the deontic operators
        for theory_atom in ctl2.theory_atoms:
            is_deontic = False
            theory_atom_name = theory_atom.term.name
            for theory_atom_element in theory_atom.elements:
                for theory_atom_element_term in theory_atom_element.terms:
                    is_negated = theory_atom_element_term.name == "-"
                    theory_atom_element_term_name = theory_atom_element_term.arguments[0].name if is_negated else theory_atom_element_term.name
                    is_deontic = theory_atom_name in ["obligatory", "forbidden", "not_obligatory", "not_forbidden"]
                    if is_deontic:
                        #ctl.add("base", [], f":- _deolingo_obligatory_({theory_atom_element_term_name}), _deolingo_forbidden_({theory_atom_element_term_name}), not {theory_atom_element_term_name}, not -{theory_atom_element_term_name}.")
                        parse_string(f"_deolingo_holds({theory_atom_element_term_name}) :- {theory_atom_element_term_name}.", bld.add)
                        parse_string(f"-_deolingo_holds({theory_atom_element_term_name}) :- -{theory_atom_element_term_name}.", bld.add)
                        parse_string(f"_deolingo_deontic({theory_atom_element_term_name}).", bld.add)
        dt = DeonticTransformer()
        parse_string(prog, lambda stm: callback(bld, stm))
        nprog = """
        _deolingo_violation(X) :- _deolingo_obligatory(X), -_deolingo_holds(X).
        _deolingo_violation(X) :- _deolingo_forbidden(X), _deolingo_holds(X).
        _deolingo_fulfilled(X) :- _deolingo_obligatory(X), _deolingo_holds(X).
        _deolingo_fulfilled(X) :- _deolingo_forbidden(X), -_deolingo_holds(X).
        %_deolingo_obligatory(X) :- _deolingo_forbidden(-X).
        %_deolingo_forbidden(X) :- _deolingo_obligatory(-X).
        _deolingo_implicit_permission(X) :- not _deolingo_forbidden(X), _deolingo_deontic(X).
        _deolingo_explicit_permission(X) :- -_deolingo_forbidden(X), _deolingo_deontic(X).
        :- _deolingo_obligatory(X), _deolingo_forbidden(X), not _deolingo_holds(X), not -_deolingo_holds(X).
        """
        parse_string(nprog, bld.add)
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
        self.version = "0.0.2"


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
