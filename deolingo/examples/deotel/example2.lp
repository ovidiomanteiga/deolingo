
#program dynamic.
deolingo_maintain_obligation(Obligation,Until) :- 'deolingo_maintain_obligation(Obligation,Until), not deolingo_holds(Until).
deolingo_achieve_obligation(Obligation,Until) :- 'deolingo_achieve_obligation(Obligation,Until), not deolingo_holds(Until), not deolingo_fulfilled_obligation(Obligation).

#program always.
deolingo_obligatory(Obligation) :- deolingo_maintain_obligation(Obligation,Until), not deolingo_holds(Until).
deolingo_obligatory(Obligation) :- deolingo_achieve_obligation(Obligation,Until), not deolingo_holds(Until), not deolingo_fulfilled_obligation(Obligation).

deolingo_maintain_obligation(quarantine,negative) :- positive.
deolingo_achieve_obligation(report,report) :- positive, quarantine.
deolingo_forbidden(report) :- deolingo_violated_obligation(quarantine).
deolingo_holds(negative) :- negative.

#program initial.
positive.

&tel{ &true ;> &true ;> negative ;> &true }.

#program final.

%:- not negative.
