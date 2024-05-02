import logging

from clingo.ast import parse_string

from deolingo._deontic_ast_transformer import DeonticASTTransformer, MultipleRuleException

from deolingo._deontic_atom import *


deolingo_theory = f"""
#theory _deolingo_ {{
    deontic_term {{
        - : 2, unary;
        | : 1, binary, left
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

    def __init__(self, add_to_program_callback, transformer=None, translate=False):
        self.deontic_transformer = transformer if transformer is not None else DeonticASTTransformer(translate)
        self._add_to_program_callback = add_to_program_callback
        self.translate = translate
        self.translated_program = ""
        self._translated_part = ""
        self._deolingo_theory_added = False
        self._deontic_rules_added = False

    def transform_source(self, source):
        return self.transform([source])

    def transform(self, inputs):
        self._translated_part = ""
        self._add_deolingo_theory()
        self._transform_and_add_source_inputs(inputs)
        self._add_common_deontic_rules()
        self._add_rules_for_each_deontic_atom()
        part = self._translated_part
        self._translated_part = ""
        return part

    def _add_to_translation(self, statement):
        if self.translate:
            statement_str = str(statement)
            self.translated_program += statement_str
            self._translated_part += statement_str

    def _add_string_to_program(self, statement):
        parse_string(statement, self._add_to_program_callback)
        self._add_to_translation(statement)

    def _add_deolingo_theory(self):
        if not self._deolingo_theory_added:
            #parse_string(deolingo_theory, self._add_to_program_callback)
            self._add_string_to_program(deolingo_theory)
            self._deolingo_theory_added = True

    def _transform_and_add_to_program(self, statement):
        try:
            self.deontic_transformer.translated_program = ""
            transformed_statement = self.deontic_transformer(statement)
            if self.deontic_transformer.translated_program == "":
                self._add_to_translation("\n" + str(transformed_statement))
            else:
                self._add_to_translation(self.deontic_transformer.translated_program)
            self._add_to_program_callback(transformed_statement)
        except MultipleRuleException as mr:
            if mr.line is not None:
                self.translated_program += f"\n% Source line: {mr.line.begin.line}\n"
            for r in mr.rules:
                self._add_to_translation(str(r) + "\n")
                self._add_to_program_callback(r)

    def _transform_and_add_source_inputs(self, inputs):
        for source_input in inputs:
            parse_string(source_input, self._transform_and_add_to_program)

    def _add_rules_for_each_deontic_atom(self):
        for deontic_atom in self.deontic_transformer.deontic_atoms:
            holds_positive = holds(deontic_atom)
            holds_negative = holds(f"-{deontic_atom}")
            rules = [
                f"\n% Deontic atom rules for '{deontic_atom}'",
                f"{holds_positive} :- {deontic_atom}.",
                f"{holds_negative} :- -{deontic_atom}."
            ]
            rules_as_string = "\n".join(rules) + '\n'
            self._add_string_to_program(rules_as_string)

    def _add_common_deontic_rules(self):
        if self._deontic_rules_added:
            return
        self._deontic_rules_added = True
        deontic_rules = [
            f"\n% Deontic axiom D for DELX",
            f":- {obligatory('X')}, {forbidden('X')}, not {holds('X')}, not {holds('-X')}.",
            f"\n% Deontic operator rules",
            f"\n% Violation",
            f"{violated('X')} :- {violated_obligation('X')}.",
            f"{violated('X')} :- {violated_prohibition('X')}.",
            f"\n% Fulfillment",
            f"{fulfilled('X')} :- {fulfilled_obligation('X')}.",
            f"{fulfilled('X')} :- {fulfilled_prohibition('X')}.",
            f"\n% Obligation/prohibition equivalence",
            f"{obligatory('X')} :- {forbidden('-X')}.",
            f"{forbidden('-X')} :- {obligatory('X')}.",
            f"{forbidden('X')}  :- {obligatory('-X')}.",
            f"{obligatory('-X')} :- {forbidden('X')}.",
            f"-{obligatory('X')} :- -{forbidden('-X')}.",
            f"-{forbidden('-X')} :- -{obligatory('X')}.",
            f"-{forbidden('X')}  :- -{obligatory('-X')}.",
            f"-{obligatory('-X')} :- -{forbidden('X')}.",
            f"\n% Implicit permission",
            f"{permitted_implicitly('X')} :- not {forbidden('X')}, {deontic('X')}.",
            f"not {forbidden('X')} :- {permitted_implicitly('X')}.",
            f"\n% Implicit omission",
            f"{omissible_implicitly('X')} :- not {obligatory('X')}, {deontic('X')}.",
            f"not {obligatory('X')} :- {omissible_implicitly('X')}.",
            f"\n% Permissible and omissible",
            f"{omissible('X')} :- -{obligatory('X')}.",
            f"-{obligatory('X')} :- {omissible('X')}.",
            f"{permitted('X')} :- -{forbidden('X')}.",
            f"-{forbidden('X')} :- {permitted('X')}.",
            f"-{omissible('X')} :- {obligatory('X')}.",
            f"{obligatory('X')} :- -{omissible('X')}.",
            f"-{permitted('X')} :- {forbidden('X')}.",
            f"{forbidden('X')} :- -{permitted('X')}.",
            f"\n% Optional",
            f"{optional('X')} :- {omissible('X')}, {permitted('X')}.",
            f"{omissible('X')} :- {optional('X')}.",
            f"{permitted('X')} :- {optional('X')}.",
            f"\n% Permitted by default",
            f"{permitted_by_default('X')} :- not not {forbidden('X')}; {deontic('X')}.",
            f"{permitted_by_default('X')} :- {permitted('X')}; {deontic('X')}.",
            f"{permitted('X')} :- not {forbidden('X')}, {permitted_by_default('X')}.",
            f"\n% Omissible by default",
            f"{omissible_by_default('X')} :- not not {obligatory('X')}; {deontic('X')}.",
            f"{omissible_by_default('X')} :- {omissible('X')}; {deontic('X')}.",
            f"{omissible('X')} :- not {obligatory('X')}, {omissible_by_default('X')}.",
            f"\n% Obligation violation",
            f"{violated_obligation('X')} :- {obligatory('X')}, {holds('-X')}.",
            f"{obligatory('X')} :- {violated_obligation('X')}.",
            f"{holds('-X')} :- {violated_obligation('X')}.",
            f"\n% Fulfilled obligation",
            f"{fulfilled_obligation('X')} :- {obligatory('X')}, {holds('X')}.",
            f"{obligatory('X')} :- {fulfilled_obligation('X')}.",
            f"{holds('X')} :- {fulfilled_obligation('X')}.",
            f"\n% Non-fulfilled obligation",
            f"{non_fulfilled_obligation('X')} :- {obligatory('X')}, not {holds('X')}.",
            f"{obligatory('X')} :- {non_fulfilled_obligation('X')}.",
            f"not {holds('X')} :- {non_fulfilled_obligation('X')}.",
            f"\n% Non-violated obligation",
            f"{non_violated_obligation('X')} :- {obligatory('X')}, not {holds('-X')}.",
            f"{obligatory('X')} :- {non_violated_obligation('X')}.",
            f"not {holds('-X')} :- {non_violated_obligation('X')}.",
            f"\n% Undetermined obligation",
            f"{undetermined_obligation('X')} :- {obligatory('X')}, not {holds('X')}, not {holds('-X')}.",
            f"{obligatory('X')} :- {undetermined_obligation('X')}.",
            f"not {holds('X')} :- {undetermined_obligation('X')}.",
            f"not {holds('-X')} :- {undetermined_obligation('X')}.",
            f"\n% Default obligation",
            f"{default_obligation('X')} :- not not {permitted('-X')}; {deontic('X')}.",
            f"{default_obligation('X')} :- {obligatory('X')}; {deontic('X')}.",
            f"{obligatory('X')} :- not {permitted('-X')}, {default_obligation('X')}.",
            f"\n% Violated prohibition",
            f"{violated_prohibition('X')} :- {forbidden('X')}, {holds('X')}.",
            f"{forbidden('X')} :- {violated_prohibition('X')}.",
            f"{holds('X')} :- {violated_prohibition('X')}.",
            f"\n% Fulfilled obligation",
            f"{fulfilled_prohibition('X')} :- {forbidden('X')}, {holds('-X')}.",
            f"{forbidden('X')} :- {fulfilled_prohibition('X')}.",
            f"{holds('-X')} :- {fulfilled_prohibition('X')}.",
            f"\n% Non-fulfilled prohibition",
            f"{non_fulfilled_prohibition('X')} :- {forbidden('X')}, not {holds('-X')}.",
            f"{forbidden('X')} :- {non_fulfilled_prohibition('X')}.",
            f"not {holds('-X')} :- {non_fulfilled_prohibition('X')}.",
            f"\n% Non-violated prohibition",
            f"{non_violated_prohibition('X')} :- {forbidden('X')}, not {holds('X')}.",
            f"{forbidden('X')} :- {non_violated_prohibition('X')}.",
            f"not {holds('X')} :- {non_violated_prohibition('X')}.",
            f"\n% Undetermined prohibition",
            f"{undetermined_prohibition('X')} :- {forbidden('X')}, not {holds('X')}, not {holds('-X')}.",
            f"{forbidden('X')} :- {undetermined_prohibition('X')}.",
            f"not {holds('X')} :- {undetermined_prohibition('X')}.",
            f"not {holds('-X')} :- {undetermined_prohibition('X')}.",
            f"\n% Default prohibition",
            f"{default_prohibition('X')} :- not not {permitted('X')}; {deontic('X')}.",
            f"{default_prohibition('X')} :- {forbidden('X')}; {deontic('X')}.",
            f"{forbidden('X')} :- not {permitted('X')}, {default_prohibition('X')}.",
            f"\n% Deontic",
            f"{deontic('X')} :- {obligatory('X')}.",
            f"{deontic('X')} :- {obligatory('-X')}.",
            f"{deontic('X')} :- {forbidden('X')}.",
            f"{deontic('X')} :- {forbidden('-X')}.",
        ]
        deontic_rules_as_string = "\n".join(deontic_rules) + '\n'
        self._add_string_to_program(deontic_rules_as_string)
