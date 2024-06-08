
from deolingo._rewriting_translator import DeolingoRewritingTranslator
from deolingo._translator import DeolingoTranslator
from deolingo.domain.use_case_command import UseCaseCommand

import clingo.ast as ast


class SolveDeonticProgramCommand(UseCaseCommand):

    def __init__(self, program, files, translate=False, optimize=False):
        super().__init__()
        self.program = program
        self.files = files
        self.translate = translate
        self.optimize = optimize

    def execute(self):
        with ast.ProgramBuilder(self.program) as builder:
            if self.optimize:
                transformer = DeolingoRewritingTranslator(builder.add, translate=self.translate)
            else:
                transformer = DeolingoTranslator(builder.add, translate=self.translate)
            transformer.transform_sources(None, self.files)
        if self.translate:
            print(transformer.translated_program)
            return
        self.program.configuration.solve.quiet = True
        self.program.ground([("base", [])])
        self.program.solve(on_model=None, async_=False)
