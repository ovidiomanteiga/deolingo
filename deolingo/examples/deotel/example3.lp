
#program dynamic.
deolingo_maintain_obligation(Obligation,Until) :- 'deolingo_maintain_obligation(Obligation,Until), not deolingo_holds(Until).
deolingo_achieve_obligation(Obligation,Until) :- 'deolingo_achieve_obligation(Obligation,Until), not deolingo_holds(Until), not deolingo_holds(Obligation).

#program always.
deolingo_obligatory(Obligation) :- deolingo_maintain_obligation(Obligation,Until), not deolingo_holds(Until).
deolingo_obligatory(Obligation) :- deolingo_achieve_obligation(Obligation,Until), not deolingo_holds(Until), not deolingo_holds(Obligation).

deolingo_maintain_obligation(quarantine,negative) :- positive.
deolingo_achieve_obligation(report,negative) :- positive, quarantine.
deolingo_forbidden(report) :- deolingo_violated_obligation(quarantine).

deolingo_holds(negative) :- negative.
deolingo_holds(report) :- report.

#program initial.
positive.

&tel{ &true 
    ;> positive & quarantine 
    ;> &true
    ;> &true
    ;> negative
    ;> &true }.

#program final.

%:- not negative.
