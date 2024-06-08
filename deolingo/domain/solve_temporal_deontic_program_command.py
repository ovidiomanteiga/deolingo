
from deolingo._telingo_app import DeolingoTelingoApp
from deolingo.domain.use_case_command import UseCaseCommand


class SolveTemporalDeonticProgramCommand(UseCaseCommand):

    def __init__(self, program, files):
        super().__init__()
        self.program = program
        self.files = files
        self._app = DeolingoTelingoApp()

    def execute(self, params=None):
        self._app.run(self.program, self.files)
