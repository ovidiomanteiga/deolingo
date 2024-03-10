from typing import Sequence, Optional, overload, Union, Tuple, Callable

from clingo import Control, Logger, ast, Symbol, Model, StatisticsMap, SolveResult, SolveHandle

from deolingo._deontic_answer_set_rewriter import DeonticAnswerSetRewriter
from deolingo._transformer import DeolingoTransformer


class DeolingoControl(Control):
    def __init__(self, arguments: Sequence[str] = None, logger: Optional[Logger] = None, message_limit: int = 20):
        if arguments is None:
            arguments = []
        super().__init__(arguments, logger, message_limit)
        self._translate_control = Control(arguments, logger, message_limit)
        self._program_builder = ast.ProgramBuilder(self._translate_control)
        self._transformer = DeolingoTransformer(self._program_builder.add, translate=True)
        translated = self._transformer.transform("")
        super()._add2("base", [], translated)
        self._rewriter = DeonticAnswerSetRewriter()

    def _add2(self, name: str, parameters: Sequence[str], program: str) -> None:
        translated = self._transformer.transform_source(program)
        super()._add2(name, parameters, translated)

    def solve(
        self,
        assumptions: Sequence[Union[Tuple[Symbol, bool], int]] = [],
        on_model: Optional[Callable[[Model], Optional[bool]]] = None,
        on_unsat: Optional[Callable[[Sequence[int]], None]] = None,
        on_statistics: Optional[Callable[[StatisticsMap, StatisticsMap], None]] = None,
        on_finish: Optional[Callable[[SolveResult], None]] = None,
        on_core: Optional[Callable[[Sequence[int]], None]] = None,
        yield_: bool = False,
        async_: bool = False,
    ) -> Union[SolveHandle, SolveResult]:
        return super().solve(assumptions, self._on_model(on_model), on_unsat, on_statistics,
                             on_finish, on_core, yield_, async_)

    def _on_model(self, on_model_callback):
        if on_model_callback is None:
            return None
        return lambda m: on_model_callback(self._rewriter.rewrite_model(m))
