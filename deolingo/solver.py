
from deolingo.control import DeolingoControl


class DeolingoSolver:

    def __init__(self, all_models=False, grouped=False, control=None):
        self._control = control if control is not None else DeolingoControl(grouped=grouped)
        self._all_models = all_models
        self._models = []
        if all_models:
            self._control.configuration.solve.models = 0

    def solve(self, program):
        self._control.add(program)
        self._control.ground()
        self._control.solve(on_model=self._on_model)
        return self._models

    def _on_model(self, model):
        self._models.append(model)
        return model
