
from deolingo._ast_rewriting_transformer import DeonticASTRewritingTransformer

from deolingo._deolingo_theory import _DEOLINGO_RESTRICTED_THEORY
from deolingo._translator import DeolingoTranslator


class DeolingoRewritingTranslator(DeolingoTranslator):

    # <editor-fold desc="Initialization">

    def __init__(self, add_to_program_callback, transformer=None, translate=False, add_theory=True):
        transformer = transformer if transformer is not None else DeonticASTRewritingTransformer(translate)
        super().__init__(add_to_program_callback, transformer, translate, add_theory)

    # </editor-fold>

    # <editor-fold desc="Private methods"

    def _add_deolingo_theory(self):
        """Add the Deolingo theory to the program if it has not been added yet."""
        if self._add_theory and not self._deolingo_theory_added:
            self._add_string_to_program(_DEOLINGO_RESTRICTED_THEORY, add_to_translation=not self.translate)
            self._deolingo_theory_added = True

    def _add_rules_for_each_deontic_atom(self):
        pass

    def _add_common_deontic_rules(self):
        pass

    # </editor-fold>
