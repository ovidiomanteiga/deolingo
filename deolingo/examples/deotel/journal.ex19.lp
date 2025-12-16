
#program always.

e :- deolingo_holds(e).
-e :- deolingo_holds(-e).

% (F) In case of emergency , permission to not quarantine -oblig(q)
&omissible{q} :- deolingo_holds(e).

#program initial. 
&tel{ deolingo_holds(p) ;> deolingo_holds(q) ;> deolingo_holds(p) ;> deolingo_holds(e) ;>
    deolingo_holds(r) ;> &true ;> deolingo_holds(n) ;> -deolingo_holds(q) }.


% I HAD TO ADD THIS TO journal.common.lp TO AVOID CONTRADICTION IN THE OBLIGATION
% (Deriv) Derivation from temporal obligations
% oblig(L) :- maintain(L,_), not -oblig(L).
% BUT THIS WAS ACTUALLY BECAUSE THE PAPER USES THE DEFEASIBLE VERSIONS
% OF THE DEONTIC TEMPORAL OPERATORS (defaults) => ALREADY CORRECTED.
