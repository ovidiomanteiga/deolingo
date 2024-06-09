
from deolingo.domain.use_case_command import UseCaseCommand
from deolingo.xcontrol import XDeolingoControl


class ExplainDeonticProgramCommand(UseCaseCommand):

    def __init__(self, inputs, n_solutions='1', _n_explanations='1', translate=False, weak=False):
        super().__init__()
        self.inputs = inputs
        self.translate = translate
        self._xcontrol = XDeolingoControl(n_solutions=n_solutions, n_explanations=_n_explanations, weak=weak)

    def execute(self):
        self._xcontrol.add_inputs(self.inputs)
        if self.translate:
            print(self._xcontrol.rewritten_program)
            return
        self._xcontrol.ground([("base", [])])
        self._print_text_explanations()

    def _print_text_explanations(self):
        n = 0
        for answer in self._xcontrol.explain():
            n += 1
            print(f'Answer {n}')
            for expl in answer:
                print(expl.ascii_tree())
