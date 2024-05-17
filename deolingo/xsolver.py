
from deolingo.xcontrol import XDeolingoControl


class XDeolingoSolver:

    def __init__(self, xcontrol=None):
        self._xcontrol = xcontrol if xcontrol is not None else XDeolingoControl()

    def solve(self, inputs):
        self._xcontrol = XDeolingoControl(n_solutions='0', n_explanations='0', auto_trace='none')
        self._xcontrol.add_inputs(inputs)
        self._xcontrol.ground([("base", [])])
        return self._xcontrol.explain()
