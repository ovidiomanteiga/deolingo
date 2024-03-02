from clingo.ast import parse_string

from deolingo._deontic_ast_transformer import DeonticASTTransformer

from deolingo._deontic_atom import *


deolingo_theory = f"""
#theory _deolingo_ {{
    deontic_term {{
        - : 1, unary
    }};
    show_term {{ / : 1, binary, left }};
    &{DeonticAtoms.OBLIGATORY.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.FORBIDDEN.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.OMISSIBLE.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.PERMITTED.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.OPTIONAL.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.PERMITTED_BY_DEFAULT.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.OMISSIBLE_BY_DEFAULT.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.HOLDS.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.DEONTIC.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.PERMITTED_IMPLICITLY.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.OMISSIBLE_IMPLICITLY.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.VIOLATED.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.FULFILLED.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.VIOLATED_OBLIGATION.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.FULFILLED_OBLIGATION.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.NON_VIOLATED_OBLIGATION.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.NON_FULFILLED_OBLIGATION.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.UNDETERMINED_OBLIGATION.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.DEFAULT_OBLIGATION.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.VIOLATED_PROHIBITION.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.FULFILLED_PROHIBITION.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.NON_VIOLATED_PROHIBITION.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.NON_FULFILLED_PROHIBITION.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.UNDETERMINED_PROHIBITION.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.DEFAULT_PROHIBITION.value.name}/0 : deontic_term, any;
    &show/0 : show_term, directive
}}.
"""


class DeolingoTransformer:

    def __init__(self, add_to_program_callback, transformer=DeonticASTTransformer(), translate=False):
        self.deontic_transformer = transformer
        self._add_to_program_callback = add_to_program_callback
        self.translate = translate
        self.translated_program = ""
        transformer.translate = translate

    def transform(self, inputs):
        self._add_string_to_program(deolingo_theory)
        self._transform_and_add_source_inputs(inputs)
        self._add_common_deontic_rules()
        self._add_rules_for_each_deontic_atom()
        self._add_show_directive()

    def _add_to_translation(self, statement):
        if self.translate:
            self.translated_program += str(statement)

    def _add_string_to_program(self, statement):
        parse_string(statement, self._add_to_program_callback)
        self._add_to_translation(statement)

    def _transform_and_add_to_program(self, statement):
        transformed_statement = self.deontic_transformer(statement)
        self._add_to_program_callback(transformed_statement)

    def _transform_and_add_source_inputs(self, inputs):
        for source_input in inputs:
            parse_string(source_input, self._transform_and_add_to_program)
        self._add_to_translation(self.deontic_transformer.translated_program)

    def _add_rules_for_each_deontic_atom(self):
        for deontic_atom in self.deontic_transformer.deontic_atoms:
            holds_positive = holds(deontic_atom)
            holds_negative = holds(f"-{deontic_atom}")
            is_deontic = deontic(deontic_atom)
            rules = [
                f"\n% Deontic atom rules for '{deontic_atom}'",
                f"{holds_positive} :- {deontic_atom}.",
                f"{holds_negative} :- -{deontic_atom}.",
                f"{is_deontic}."
            ]
            rules_as_string = "\n".join(rules) + '\n'
            self._add_string_to_program(rules_as_string)

    def _add_common_deontic_rules(self):
        deontic_rules = [
            f"\n% Deontic axiom D for DELX",
            f":- {obligatory('X')}, {forbidden('X')}, not {holds('X')}, not {holds('-X')}.",
            f"\n% Deontic operator rules",
            # Violation
            f"{violated('X')} :- {violated_obligation('X')}.",
            f"{violated('X')} :- {violated_prohibition('X')}.",
            # Fulfillment
            f"{fulfilled('X')} :- {fulfilled_obligation('X')}.",
            f"{fulfilled('X')} :- {fulfilled_prohibition('X')}.",
            # Obligation/prohibition equivalence
            f"{obligatory('X')} :- {forbidden('-X')}.",
            f"{forbidden('-X')} :- {obligatory('X')}.",
            f"{forbidden('X')}  :- {obligatory('-X')}.",
            f"{obligatory('-X')} :- {forbidden('X')}.",
            f"-{obligatory('X')} :- -{forbidden('-X')}.",
            f"-{forbidden('-X')} :- -{obligatory('X')}.",
            f"-{forbidden('X')}  :- -{obligatory('-X')}.",
            f"-{obligatory('-X')} :- -{forbidden('X')}.",
            # Implicit permission
            f"{permitted_implicitly('X')} :- not {forbidden('X')}, {deontic('X')}.",
            f"not {forbidden('X')} :- {permitted_implicitly('X')}.",
            # Implicit omission
            f"{omissible_implicitly('X')} :- not {obligatory('X')}, {deontic('X')}.",
            f"not {obligatory('X')} :- {omissible_implicitly('X')}.",
            # Permissible and omissible
            f"{omissible('X')} :- -{obligatory('X')}.",
            f"-{obligatory('X')} :- {omissible('X')}.",
            f"{permitted('X')} :- -{forbidden('X')}.",
            f"-{forbidden('X')} :- {permitted('X')}.",
            f"-{omissible('X')} :- {obligatory('X')}.",
            f"{obligatory('X')} :- -{omissible('X')}.",
            f"-{permitted('X')} :- {forbidden('X')}.",
            f"{forbidden('X')} :- -{permitted('X')}.",
            # Optional
            f"{optional('X')} :- {omissible('X')}, {permitted('X')}.",
            f"{omissible('X')} :- {optional('X')}.",
            f"{permitted('X')} :- {optional('X')}.",
            # Permitted by default
            f"{permitted_by_default('X')} :- {permitted('X')}: not {forbidden('X')}; {deontic('X')}.",
            f"{permitted('X')} :- not {forbidden('X')}, {permitted_by_default('X')}.",
            # Omissible by default
            f"{omissible_by_default('X')} :- {omissible('X')}: not {obligatory('X')}; {deontic('X')}.",
            f"{omissible('X')} :- not {obligatory('X')}, {omissible_by_default('X')}.",
            # Obligation violation
            f"{violated_obligation('X')} :- {obligatory('X')}, {holds('-X')}.",
            f"{obligatory('X')} :- {violated_obligation('X')}.",
            f"{holds('-X')} :- {violated_obligation('X')}.",
            # Fulfilled obligation
            f"{fulfilled_obligation('X')} :- {obligatory('X')}, {holds('X')}.",
            f"{obligatory('X')} :- {fulfilled_obligation('X')}.",
            f"{holds('X')} :- {fulfilled_obligation('X')}.",
            # Non-fulfilled obligation
            f"{non_fulfilled_obligation('X')} :- {obligatory('X')}, not {holds('X')}.",
            f"{obligatory('X')} :- {non_fulfilled_obligation('X')}.",
            f"not {holds('X')} :- {non_fulfilled_obligation('X')}.",
            # Non-violated obligation
            f"{non_violated_obligation('X')} :- {obligatory('X')}, not {holds('-X')}.",
            f"{obligatory('X')} :- {non_violated_obligation('X')}.",
            f"not {holds('-X')} :- {non_violated_obligation('X')}.",
            # Undetermined obligation
            f"{undetermined_obligation('X')} :- {obligatory('X')}, not {holds('X')}, not {holds('-X')}.",
            f"{obligatory('X')} :- {undetermined_obligation('X')}.",
            f"not {holds('X')} :- {undetermined_obligation('X')}.",
            f"not {holds('-X')} :- {undetermined_obligation('X')}.",
            # Default obligation
            f"{default_obligation('X')} :- {obligatory('X')}: not {permitted('-X')}; {deontic('X')}.",
            f"{obligatory('X')} :- not {permitted('-X')}, {default_obligation('X')}.",
            # Violated prohibition
            f"{violated_prohibition('X')} :- {forbidden('X')}, {holds('X')}.",
            f"{forbidden('X')} :- {violated_prohibition('X')}.",
            f"{holds('X')} :- {violated_prohibition('X')}.",
            # Fulfilled obligation
            f"{fulfilled_prohibition('X')} :- {forbidden('X')}, {holds('-X')}.",
            f"{forbidden('X')} :- {fulfilled_prohibition('X')}.",
            f"{holds('-X')} :- {fulfilled_prohibition('X')}.",
            # Non-fulfilled prohibition
            f"{non_fulfilled_prohibition('X')} :- {forbidden('X')}, not {holds('-X')}.",
            f"{forbidden('X')} :- {non_fulfilled_prohibition('X')}.",
            f"not {holds('-X')} :- {non_fulfilled_prohibition('X')}.",
            # Non-violated prohibition
            f"{non_violated_prohibition('X')} :- {forbidden('X')}, not {holds('X')}.",
            f"{forbidden('X')} :- {non_violated_prohibition('X')}.",
            f"not {holds('X')} :- {non_violated_prohibition('X')}.",
            # Undetermined prohibition
            f"{undetermined_prohibition('X')} :- {forbidden('X')}, not {holds('X')}, not {holds('-X')}.",
            f"{forbidden('X')} :- {undetermined_prohibition('X')}.",
            f"not {holds('X')} :- {undetermined_prohibition('X')}.",
            f"not {holds('-X')} :- {undetermined_prohibition('X')}.",
            # Default prohibition
            f"{default_prohibition('X')} :- {forbidden('X')}: not {permitted('X')}; {deontic('X')}.",
            f"{forbidden('X')} :- not {permitted('X')}, {default_prohibition('X')}.",
        ]
        deontic_rules_as_string = "\n".join(deontic_rules) + '\n'
        self._add_string_to_program(deontic_rules_as_string)

    def _add_show_directive(self):
        show_atoms = self.deontic_transformer.show_atoms
        if show_atoms is None or len(show_atoms) == 0:
            return
        show_directives = [f"\n% Show directives for deontic atoms"]
        for show_atom in show_atoms:
            show_directive = f"#show {show_atom}."
            show_directives.append(show_directive)
        show_directive = "\n".join(show_directives) + '\n'
        self._add_string_to_program(show_directive)
