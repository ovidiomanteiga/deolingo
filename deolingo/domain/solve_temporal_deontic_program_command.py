
from deolingo._telingo_app import DeolingoTelingoApp
from deolingo.domain.use_case_command import UseCaseCommand


class SolveTemporalDeonticProgramCommand(UseCaseCommand):

    def __init__(self, program, files, weak=False):
        super().__init__()
        self.program = program
        self.files = files
        self.weak = weak
        self._app = DeolingoTelingoApp()

    def execute(self):
        self._app.run(self.program, self.files, weak=self.weak)
