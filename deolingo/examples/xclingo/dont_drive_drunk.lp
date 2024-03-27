% examples/dont_drive_drunk.lp

person(gabriel;clare).

drive(gabriel).
alcohol(gabriel, 40).
resist(gabriel).

drive(clare).
alcohol(clare, 50).

%!trace_rule {"% drove drunk", P}
&obligatory{punish(P)} :- drive(P), alcohol(P,A), A>30, person(P).

%!trace_rule {"% resisted to authority", P}
&obligatory{punish(P)} :- resist(P), person(P).

%!trace_rule {"% goes to prison",P}
sentence(P, prison) :- &obligatory{punish(P)}.

%!trace_rule {"% is innocent by default",P}
sentence(P, innocent) :- person(P), not &obligatory{punish(P)}.

%!trace {"% alcohol's level is %",P,A} alcohol(P,A).
%!trace {"% was drunk",P} alcohol(P,A).
%!trace {"It is obligatory to punish %",P} &obligatory{punish(P)}.

%!show_trace sentence(P,S).