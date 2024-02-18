
import sys
import clingo
import clingo.ast as ast
from typing import Callable
from clingo.ast import Transformer, Variable, parse_string, SymbolicAtom, ProgramBuilder
from clingox.ast import theory_term_to_literal
import clingox as clx
from clingox.pprint import PrettyPrinter
from os import listdir
from os.path import isfile, join, isdir
from pathlib import Path


deolingo_theory = """
#theory deo {
    deontic_term { 
        & : 2, binary, left;
        - : 3, unary;
        ~ : 3, unary;
        | : 1, binary, left
    };
    &ob/0 : deontic_term, any;
    &fb/0 : deontic_term, any;
    &nob/0 : deontic_term, any;
    &nfb/0 : deontic_term, any
}.
"""

deontic_theory_atoms = ["ob", "fb", "nob", "nfb"]
deontic_theory_atoms_obligation = ["ob", "nob"]
deontic_theory_atoms_negation = ["nob", "nfb"]


class DeonticTransformer(Transformer):

    def __init__(self):
        super().__init__()
        self.deontic_atoms = set()

    def map_deontic_atom(self, atom, as_literal=False):
        if atom.term.name in deontic_theory_atoms:
            is_negated = atom.term.name in deontic_theory_atoms_negation
            is_obligatory = atom.term.name in deontic_theory_atoms_obligation
            new_name = "ob" if is_obligatory else "fb"
            if len(atom.elements) == 1:                   
                new_name = ("-" if is_negated else "") + "_deolingo_" + new_name
                new_terms = [clx.ast.theory_term_to_term(tterm) for tterm in atom.elements[0].terms]
                new_atom =  ast.SymbolicAtom(ast.Function(atom.term.location, new_name, new_terms, False))
                if as_literal:
                    new_atom = ast.Literal(atom.term.location, ast.Sign.NoSign, new_atom)
                deontic_term = new_terms[0]
                if deontic_term.ast_type != ast.ASTType.Variable:
                    dt_name = str(deontic_term)
                    dt_is_negated = dt_name.startswith("-")
                    dt_name = dt_name[1:] if dt_is_negated else dt_name
                    self.deontic_atoms.add(dt_name)
                return new_atom
        return atom

    def visit_Rule(self, rule):
        new_head = rule.head
        if rule.head is not None:
            if rule.head.ast_type == ast.ASTType.TheoryAtom:
                new_head = self.map_deontic_atom(rule.head, as_literal=True)
            new_head = self(new_head)
        new_body = rule.body
        if rule.body is not None:
            new_body = self.visit_sequence(rule.body)
        return ast.Rule(rule.location, new_head, new_body)

    def visit_TheoryAtom(self, atom):
        return self.map_deontic_atom(atom)


def deontic_transform(inputs, callback):
    inputs.insert(0, deolingo_theory)
    dt = DeonticTransformer()
    def int_callback(stm):
        tstm = dt(stm)
        callback(tstm)   
    for input in inputs:
        parse_string(input, int_callback)
    for da in dt.deontic_atoms:
        parse_string(f"_deolingo_holds({da}) :- {da}.", callback)
        parse_string(f"_deolingo_holds(-{da}) :- -{da}.", callback)
        parse_string(f"_deolingo_deontic({da}).", callback)
    nprog = """
    _deolingo_violation(X) :- _deolingo_ob(X), _deolingo_holds(-X).
    _deolingo_violation(X) :- _deolingo_fb(X), _deolingo_holds(X).
    _deolingo_fulfilled(X) :- _deolingo_ob(X), _deolingo_holds(X).
    _deolingo_fulfilled(X) :- _deolingo_fb(X), _deolingo_holds(-X).
    _deolingo_ob(X) :- _deolingo_fb(-X).
    _deolingo_fb(X) :- _deolingo_ob(-X).
    _deolingo_implicit_permission(X) :- not _deolingo_fb(X), _deolingo_deontic(X).
    _deolingo_explicit_permission(X) :- -_deolingo_fb(X), _deolingo_deontic(X).
    :- _deolingo_ob(X), _deolingo_fb(X), not _deolingo_holds(X), not _deolingo_holds(-X).
    """
    parse_string(nprog, callback)


def rewrite_atoms(atoms):
    """
    Rewrites the atom by removing the prefix '_deolingo_' if present.
    """
    rewritten_atoms = []
    for atom in atoms:
        str_atom = str(atom)
        if "_deolingo_deontic" in str_atom or "_deolingo_holds" in str_atom:
            continue
        if str_atom.startswith("_deolingo_"):
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
        self.version = "0.0.3"

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
        with ast.ProgramBuilder(prg) as b:
            files = [open(f) for f in files]
            if len(files) == 0:
                files.append(sys.stdin)
            inputs = [f.read() for f in files]
            deontic_transform(inputs, b.add)
        prg.ground([("base", [])])
        prg.solve(on_model=None, async_=False)


def rewrite_model(model: clingo.Model):
    """
    Rewrites the atoms of the given model by removing the prefix '_deolingo_' if present.
    """
    atoms = model.symbols(shown=True)
    rewritten_atoms = rewrite_atoms(atoms)
    return rewritten_atoms


def run_deolingo(prog, all_models=False):
    ctl = clingo.Control()
    if all_models:
        ctl.configuration.solve.models = 0
    with ast.ProgramBuilder(ctl) as b:
        deontic_transform([prog], b.add)
    ctl.ground([("base", [])])
    models = []
    def on_model(m):
        nonlocal models
        models += [rewrite_model(m)]
    solved = ctl.solve(on_model=on_model)
    for m in models:
        print("Answer: " + str(m))
    return models


def read_examples():
    """
    Returns a list of all examples reading from folders in ../examples
    """
    examples_folder = Path(__file__).parent / "../examples"
    folders = [f for f in listdir(examples_folder) if isdir(join(examples_folder, f))]
    examples_files = []
    for folder in folders:
        folder = examples_folder / folder
        examples_files += [folder / f for f in listdir(folder) if isfile(join(folder, f)) and f.endswith(".lp")]
    def name(f):
        return f.parent.name + "/" + f.name
    files = [(name(f), open(f)) for f in examples_files]
    examples = [(f[0],f[1].read()) for f in files]
    return examples
    

def main():
    """
    Run the deolingo application.
    """
    sys.exit(int(clingo.clingo_main(DeolingoApplication(), sys.argv[1:])))


if __name__ == '__main__':
    main()
