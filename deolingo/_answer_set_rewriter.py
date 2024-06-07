import clingo

from deolingo._deontic_atom import DeonticAtoms, DeonticAtom


class DeonticAnswerSetRewriter:

    # <editor-fold desc="Initialization">

    def __init__(self, grouped=False):
        self._grouped = grouped

    # </editor-fold>

    # <editor-fold desc="Public methods">

    def rewrite_atoms(self, atoms):
        """Rewrites the atom by removing the prefix 'deolingo_' if present."""
        rewritten_atoms = []
        for atom in atoms:
            str_atom = str(atom)
            is_negated = str_atom.startswith("-")
            deontic_atom = DeonticAtoms.with_prefixed_name(atom.name)
            if deontic_atom is None:
                if self._grouped:
                    rewritten_atoms.append((str_atom, None))
                else:
                    rewritten_atoms.append(str_atom)
                continue
            deontic_atoms = [DeonticAtoms.OBLIGATORY, DeonticAtoms.FORBIDDEN,
                             DeonticAtoms.PERMITTED, DeonticAtoms.OMISSIBLE]
            if is_negated or deontic_atom not in deontic_atoms:
                continue
            str_atom = str_atom[1:] if is_negated else str_atom
            unprefixed = DeonticAtom.unprefix(str_atom)
            # remove the deontic atom name and the first parenthesis from str_atom
            str_atom_int = unprefixed.replace(deontic_atom.value.name, "", 1)[1:]
            is_negated_inside = str_atom_int.startswith("-")
            if is_negated_inside:
                continue
            rewritten = "&" + unprefixed.replace("(", "{", 1)
            rewritten = rewritten[::-1].replace(")", "}", 1)[::-1]
            rewritten = rewritten if not is_negated else "-" + rewritten
            if self._grouped:
                rewritten_atoms.append((rewritten, deontic_atom))
            else:
                rewritten_atoms.append(rewritten)
        if self._grouped:
            return self._group_atoms_by_worlds(rewritten_atoms)
        else:
            return rewritten_atoms, None, None

    def rewrite_model(self, model: clingo.Model):
        """Rewrites the atoms of the given model by removing the prefix '_deolingo_' if present."""
        atoms = model.symbols(shown=True)
        rewritten_atoms, obligations, prohibitions = self.rewrite_atoms(atoms)
        if not self._grouped:
            return rewritten_atoms
        return {'facts': list(rewritten_atoms),
                'obligations': list(obligations),
                'prohibitions': list(prohibitions)}


    # </editor-fold>

    # <editor-fold desc="Private methods">

    @staticmethod
    def _group_atoms_by_worlds(rewritten_atoms):
        facts_world = set()
        obligations_world = set()
        prohibitions_world = set()
        for atom_str, deontic_atom in rewritten_atoms:
            if deontic_atom in [DeonticAtoms.OBLIGATORY, DeonticAtoms.OMISSIBLE]:
                obligations_world.add(atom_str)
            elif deontic_atom in [DeonticAtoms.FORBIDDEN, DeonticAtoms.PERMITTED]:
                prohibitions_world.add(atom_str)
            else:
                facts_world.add(atom_str)
        return facts_world, obligations_world, prohibitions_world

    # </editor-fold>
