
#program dynamic.
deo_maintain_obligation(Obligation,Until) :- 'deo_maintain_obligation(Obligation,Until), not deolingo_holds(Until).
deo_achieve_obligation(Obligation,Until) :- 'deo_achieve_obligation(Obligation,Until), not deolingo_holds(Until), not deolingo_holds(Obligation).

#program always.
deolingo_obligatory(Obligation) :- deo_maintain_obligation(Obligation,Until), not deolingo_holds(Until).
deolingo_obligatory(Obligation) :- deo_achieve_obligation(Obligation,Until), not deolingo_holds(Until), not deolingo_holds(Obligation).

deo_maintain_obligation(quarantine,negative) :- positive.
deo_achieve_obligation(report,negative) :- positive, quarantine.
deolingo_forbidden(report) :- deolingo_violated_obligation(quarantine).

deolingo_holds(negative) :- negative.
deolingo_holds(report) :- report.

#program initial.
positive.

% Just to make quarantine and report deontic atoms.
&obligatory{quarantine}. &obligatory{report}.

&tel{ 
    &true 
    ;> positive & quarantine 
    ;> quarantine
    ;> report
    ;> &true
    ;> negative 
    ;> &true
}.

#program final.
%:- not negative.
