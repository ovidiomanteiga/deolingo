
import sys
from typing import Callable

import clingo
import clingo.ast as ast

from _facade import rewrite_atoms
from _transformer import DeolingoTransformer


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
            transformer = DeolingoTransformer(b.add)
            transformer.transform(inputs)
        prg.ground([("base", [])])
        prg.solve(on_model=None, async_=False)
