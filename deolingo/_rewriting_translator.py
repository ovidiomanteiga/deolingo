
from deolingo._ast_rewriting_transformer import DeonticASTRewritingTransformer

from deolingo._deolingo_theory import _DEOLINGO_RESTRICTED_THEORY
from deolingo._deontic_atom import DeonticAtoms
from deolingo._deontic_rules import DeonticRules
from deolingo._translator import DeolingoTranslator


class DeolingoRewritingTranslator(DeolingoTranslator):

    # <editor-fold desc="Initialization">

    def __init__(self, add_to_program_callback, transformer=None, translate=False,
                 add_theory=True, add_deontic_rules=True, weak=False):
        transformer = transformer if transformer is not None else DeonticASTRewritingTransformer(translate)
        super().__init__(add_to_program_callback, transformer, translate, add_theory, add_deontic_rules, weak=weak)

    # </editor-fold>

    # <editor-fold desc="Private methods"

    def _add_deolingo_theory(self):
        """Add the Deolingo theory to the program if it has not been added yet."""
        if self._add_theory and not self._deolingo_theory_added:
            self._add_string_to_program(_DEOLINGO_RESTRICTED_THEORY, add_to_translation=not self.translate)
            self._deolingo_theory_added = True

    def _add_rules_for_each_deontic_atom(self):
        super()._add_rules_for_each_deontic_atom()

    def _add_common_deontic_rules(self):
        if self._deontic_rules_added:
            return
        self._deontic_rules_added = True
        necessary_rules = self.deontic_transformer.derivation_rules_to_be_added
        if not self.weak:
            super()._add_string_to_program("\n".join(DeonticRules.deontic_weak_axiom()) + '\n')
        else:
            super()._add_string_to_program("\n".join(DeonticRules.deontic_weak_axiom_weak_constraint()) + '\n')
        super()._add_string_to_program("\n".join(DeonticRules.obligation_prohibition_equivalence()) + '\n')
        if len(necessary_rules) == 0:
            return
        super()._add_string_to_program("\n% Deontic rules\n")
        rules = {
            DeonticAtoms.VIOLATED_OBLIGATION.value.prefixed(): DeonticRules.derive_violated_obligation(),
            DeonticAtoms.FULFILLED_OBLIGATION.value.prefixed(): DeonticRules.derive_fulfilled_obligation(),
            DeonticAtoms.VIOLATED_PROHIBITION.value.prefixed(): DeonticRules.derive_violated_prohibition(),
            DeonticAtoms.FULFILLED_PROHIBITION.value.prefixed(): DeonticRules.derive_fulfilled_prohibition(),
            DeonticAtoms.NON_VIOLATED_OBLIGATION.value.prefixed(): DeonticRules.derive_non_violated_obligation(),
            DeonticAtoms.NON_FULFILLED_OBLIGATION.value.prefixed(): DeonticRules.derive_non_fulfilled_obligation(),
            DeonticAtoms.NON_VIOLATED_PROHIBITION.value.prefixed(): DeonticRules.derive_non_violated_prohibition(),
            DeonticAtoms.NON_FULFILLED_PROHIBITION.value.prefixed(): DeonticRules.derive_non_fulfilled_prohibition(),
            DeonticAtoms.UNDETERMINED_OBLIGATION.value.prefixed(): DeonticRules.derive_undetermined_obligation(),
            DeonticAtoms.UNDETERMINED_PROHIBITION.value.prefixed(): DeonticRules.derive_undetermined_prohibition(),
        }
        for deontic_atom_name in necessary_rules:
            super()._add_string_to_program(rules[deontic_atom_name] + "\n")

    # </editor-fold>
