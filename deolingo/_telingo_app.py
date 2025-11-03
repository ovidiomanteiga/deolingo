
import re
import sys

import clingo
import telingo
import tempfile

from clingo import ast, SymbolType, Function

from deolingo._translator import DeolingoTranslator
from deolingo._deontic_atom import DeonticAtoms, _DEOLINGO_ATOM_PREFIX


class DeolingoTelingoApp(telingo.TelApp):

    def run(self, program, files, weak=False, preprocess_theory_atoms=True):
        with ast.ProgramBuilder(program) as builder:
            transformer = DeolingoTranslator(builder.add, translate=True, temporal=True, weak=weak)
            if preprocess_theory_atoms:
                preprocessed_sources = DeolingoTelingoApp.preprocess_deontic_theory_atoms(files)
                transformer.transform_sources(preprocessed_sources)
            else:
                transformer.transform_sources(None, files)
        translated_program = transformer.translated_program
        if "--translate" in sys.argv:
            print(translated_program)
            return
        # Create a named temporary file (automatically deleted on close)
        with tempfile.NamedTemporaryFile(mode="w+t", delete=False) as temp_file:
            temp_file.write(translated_program)
            temp_file.seek(0)  # Rewind to the beginning of the file
            clingo.clingo_main(self, [temp_file.name])
            temp_file.close()  # Important: close the file first to release the handle
            import os
            os.remove(temp_file.name)

    @staticmethod
    def preprocess_deontic_theory_atoms(files) -> list[str]:
        sources = [open(file, "r").read() for file in files]
        preprocessed_sources = []
        for src in sources:
            for atom in DeonticAtoms.get_all_names():
                pattern = r"&" + atom + r"{(.+?)}"
                replacement = f"deolingo_{atom}(\\1)"
                src = re.sub(pattern, replacement, src)
            preprocessed_sources.append(src)
        return preprocessed_sources

    @staticmethod
    def get_deontic_atoms_to_print():
        return [ "obligatory", "permitted", "forbidden", "omissible"] + DeolingoTelingoApp.get_temporal_deontic_atoms_to_print()
    
    @staticmethod
    def get_temporal_deontic_atoms_to_print():
        return [ "maintain_obligation", "cancel_maintain_obligation",
                "maintain_default_obligation", "cancel_maintain_default_obligation",
                "achieve_obligation", "cancel_achieve_obligation",
                "maintain_permission", "cancel_maintain_permission",
                "maintain_default_permission", "cancel_maintain_default_permission",
                "achieve_permission", "cancel_achieve_permission",
                "maintain_prohibition", "cancel_maintain_prohibition",
                "maintain_default_prohibition", "cancel_maintain_default_prohibition",
                "achieve_prohibition", "cancel_achieve_prohibition",
                "maintain_omission", "cancel_maintain_omission",
                "maintain_default_omission", "cancel_maintain_default_omission",
                "achieve_omission", "cancel_achieve_omission", ]

    def print_model(self, model, printer):
        table = {}
        for sym in model.symbols(shown=True):
            if sym.type == SymbolType.Function and len(sym.arguments) > 0:
                table.setdefault(sym.arguments[-1].number, []).append(
                    Function(sym.name, sym.arguments[:-1], sym.positive))
        for step in range(self._TelApp__horizon + 1):
            symbols = table.get(step, [])
            sys.stdout.write(" State {}:".format(step))
            sig = None
            for sym in sorted(symbols):
                if not sym.name.startswith('__'):
                    import re
                    pattern = "^(-?)" + _DEOLINGO_ATOM_PREFIX + r"(\w+)\((.+)\)$"
                    # extract the first match group of the pattern from sym
                    m = re.match(pattern, str(sym))
                    if m is not None:
                        if m.group(2) in self.get_deontic_atoms_to_print() and m.group(1) != "-":
                            if m.group(2) in self.get_temporal_deontic_atoms_to_print():
                                npattern = "^(-?)" + _DEOLINGO_ATOM_PREFIX + r"(\w+)\((.+),(.+)\)$"
                                sym = re.sub(npattern, r"\1&\2(\4){\3}", str(sym))
                            else:
                                if m.group(3).startswith('-'):
                                    continue
                                sym = re.sub(pattern, r"\1&\2{\3}", str(sym))
                            sys.stdout.write("\n ")
                            sys.stdout.write(" {}".format(sym))
                        if m.group(2) == "inconsistency":
                            sym = re.sub(pattern, _DEOLINGO_ATOM_PREFIX + r"\2(\3)", str(sym))
                            sys.stdout.write("\n ")
                            sys.stdout.write(" {}".format(sym))
                    else:
                        if (sym.name, len(sym.arguments), sym.positive) != sig:
                            sys.stdout.write("\n ")
                            sig = (sym.name, len(sym.arguments), sym.positive)
                        sys.stdout.write(" {}".format(sym))
            sys.stdout.write("\n")
        return True
