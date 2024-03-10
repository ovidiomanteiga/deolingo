import clingo

from deolingo._deontic_atom import DeonticAtoms, unprefix


class DeonticAnswerSetRewriter:

    def rewrite_atoms(self, atoms):
        """
        Rewrites the atom by removing the prefix '_deolingo_' if present.
        """
        rewritten_atoms = []
        for atom in atoms:
            str_atom = str(atom)
            is_negated = str_atom.startswith("-")
            deontic_atom = DeonticAtoms.with_prefixed_name(atom.name)
            if deontic_atom is None:
                rewritten_atoms.append(str_atom)
                continue
            if is_negated or \
                    deontic_atom not in [DeonticAtoms.OBLIGATORY, DeonticAtoms.FORBIDDEN,
                                         DeonticAtoms.PERMITTED, DeonticAtoms.OMISSIBLE]:
                continue
            str_atom = str_atom[1:] if is_negated else str_atom
            unprefixed = unprefix(str_atom)
            # remove the deontic atom name and the first parenthesis from str_atom
            str_atom_int = unprefixed.replace(deontic_atom.value.name, "", 1)[1:]
            is_negated_inside = str_atom_int.startswith("-")
            if is_negated_inside:
                continue
            rewritten = "&" + unprefixed.replace("(", "{", 1)
            rewritten = rewritten[::-1].replace(")", "}", 1)[::-1]
            rewritten = rewritten if not is_negated else "-" + rewritten
            rewritten_atoms.append(rewritten)
        return rewritten_atoms

    def rewrite_model(self, model: clingo.Model):
        """
        Rewrites the atoms of the given model by removing the prefix '_deolingo_' if present.
        """
        atoms = model.symbols(shown=True)
        rewritten_atoms = self.rewrite_atoms(atoms)
        return rewritten_atoms
