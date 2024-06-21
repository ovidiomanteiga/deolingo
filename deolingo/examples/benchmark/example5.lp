
person(1..6).
alcohol_value(0..10).

drive(P) :- person(P).
1 {alcohol(P, V): alcohol_value(V) } 1 :- person(P).
{resist(P)} :- person(P).

%!trace_rule {"% drove drunk", P}
drive_drunk(P) :- drive(P), alcohol(P,A), A>30, person(P).

%!trace_rule {"It is forbidden to drive drunk"}
&forbidden{drive_drunk(P)} :- person(P).

%!trace_rule {"% is punished because % violated prohibition to drive drunk", P, P}
punish(P) :- &violated_prohibition{drive_drunk(P)}, person(P).

%!trace_rule {"It is forbidden to resist to authority"}
&forbidden{resist(P)} :- person(P).

%!trace_rule {"% is punished because % violated the prohibition to resist to authority", P, P}
punish(P) :- &violated_prohibition{resist(P)}, person(P).

%!trace_rule {"% goes to prison",P}
sentence(P, prison) :- punish(P).

%!trace_rule {"% is innocent by default",P}
sentence(P, innocent) :- person(P), not punish(P).

%!trace {"% alcohol's level is %",P,A} alcohol(P,A).
%!trace {"% was drunk",P} alcohol(P,A).

%!show_trace sentence(P,S).
