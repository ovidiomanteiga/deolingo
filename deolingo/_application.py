import sys
from typing import Callable

import clingo
import clingo.ast as ast
import xclingo

import deolingo._version as deolingo_version
from deolingo._deontic_answer_set_rewriter import DeonticAnswerSetRewriter
from deolingo._transformer import DeolingoTransformer
from deolingo.xcontrol import XDeolingoControl


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
        self.version = deolingo_version.__version__
        self.translate_flag = clingo.Flag(False)
        self.ungrouped_flag = clingo.Flag(False)
        self.explain_flag = clingo.Flag(False)
        self.answer_set_rewriter = DeonticAnswerSetRewriter()

    def register_options(self, options: clingo.ApplicationOptions):
        """
        Registers the options for the application.
        """
        # add an option to translate the deontic logic program into an ASP program
        options.add_flag("deontic", "translate",
                         "Translate a deontic logic program into an ASP program", self.translate_flag)
        options.add_flag("deontic", "ungrouped",
                         "Do not group the answer sets deontic worlds", self.ungrouped_flag)
        options.add_flag("deontic", "explain",
                         "Use Xclingo to generate explanations", self.explain_flag)

    def print_model(self, model: clingo.Model, printer: Callable[[], None] = None):
        """
        Prints the atoms of the given model.
        This function is called for each model of the problem.
        """
        atoms = model.symbols(shown=True)
        grouped = not self.ungrouped_flag.flag
        self.answer_set_rewriter.grouped = grouped
        rewritten_atoms, ob, fb = self.answer_set_rewriter.rewrite_atoms(atoms)
        if grouped:
            print(f'FACTS: {", ".join(rewritten_atoms)}')
            print(f'OBLIGATIONS: {", ".join(ob)}')
            print(f'PROHIBITIONS: {", ".join(fb)}')
            print()
        else:
            print(", ".join(rewritten_atoms))

    def print_text_explanations(self, x_control: xclingo.XclingoControl):
        n = 0
        for answer in x_control.explain():
            n += 1
            print(f'Answer {1}')
            for expl in answer:
                print(expl.ascii_tree())

    def main(self, prg, files):
        """
        Implements the incremental solving loop.
        This function implements the Application.main() function as required by
        clingo.clingo_main().
        """
        files = [open(f) for f in files]
        if len(files) == 0:
            files.append(sys.stdin)
        inputs = [f.read() for f in files]
        if self.explain_flag.flag:
            xprg = XDeolingoControl(n_solutions='0', n_explanations='0', auto_trace='none')

            def xadd(statement: ast.AST) -> None:
                xprg.add("base", [], str(statement))

            transformer = DeolingoTransformer(xadd, translate=True)
            transformer.transform(inputs)
            xprg.add("base", [], transformer.translated_program)
            if self.translate_flag.flag:
                print(xprg.rewritten_program)
                return
            xprg.ground([("base", [])])
            self.print_text_explanations(xprg)
            return
        with ast.ProgramBuilder(prg) as b:
            transformer = DeolingoTransformer(b.add, translate=self.translate_flag.flag)
            transformer.transform(inputs)
        if self.translate_flag.flag:
            print(transformer.translated_program)
            return
        prg.configuration.solve.quiet = True
        prg.ground([("base", [])])
        prg.solve(on_model=None, async_=False)
