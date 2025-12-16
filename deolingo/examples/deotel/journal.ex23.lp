
#program always.

c :- deolingo_holds(c).
-c :- deolingo_holds(-c).
p :- deolingo_holds(p).
-p :- deolingo_holds(-p).

% (1) We perhaps decide to [p]ark , assuming no prohibition
{deolingo_holds(p)} :- not &forbidden{p}.

#program initial.
&tel{ &true ;> &true ;> &forbidden{p} ;> &forbidden{p} ;> deolingo_holds(c) }.


% HAD TO ADD sys.argv[1] (assuming it's the number of models) TO _telingo_app.py TO MAKE THIS WORK 
