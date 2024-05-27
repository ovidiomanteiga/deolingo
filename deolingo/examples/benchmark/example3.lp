fence(1..8).
color(white;black;red;green;blue;cyan;magenta;yellow).
&forbidden{fence(F)} :- not &permitted{fence(F)}, fence(F).
&obligatory{color(F,white)} :- fence(F), &forbidden{fence(F)}.
&permitted{fence(F)} :- sea(F), fence(F).
1 {fence(F); -fence(F)} 1 :- fence(F).
1 {color(F,C): color(C)} 1 :- fence(F).