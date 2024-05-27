person(1..15).
&forbidden{walk(P)} :- person(P).
&obligatory{walk(P,right)} :- walk(P).
walk(P) :- walk(P,right).
&obligatory{walk(P)} :- &obligatory{walk(P,right)}.
1 {walk(P); -walk(P)} 1 :- person(P).
1 {walk(P,right); -walk(P,right)} 1 :- person(P).