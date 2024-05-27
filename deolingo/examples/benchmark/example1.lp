person(1..20).
&obligatory{work(P)} :- not &omissible{work(P)}, person(P).
&omissible{work(P)} :- weekend, person(P).
weekend; -weekend.
1 {work(P); -work(P)} 1 :- person(P).