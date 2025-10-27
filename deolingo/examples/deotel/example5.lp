
#program always.

&maintain_obligation(negative){quarantine} :- positive.
&achieve_obligation(negative){report} :- positive, quarantine.
&forbidden{report} :- &violated_obligation{quarantine}.

cannot_enter_country :- &violated_obligation{vaccine}.
public_health_criminal :- &violated_prohibition{virus}.
deolingo_holds(virus) :- virus.
deolingo_holds(-virus) :- -virus.
deolingo_holds(vaccine) :- vaccine.
deolingo_holds(-vaccine) :- -vaccine.

#program initial.

% Just to make quarantine and report deontic atoms.
&obligatory{vaccine}. &forbidden{virus}.

&tel{ 
    positive
    ;> &obligatory{vaccine} & -vaccine
    ;> &forbidden{virus} & virus
}.
