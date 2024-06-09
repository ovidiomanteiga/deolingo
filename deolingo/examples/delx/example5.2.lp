
% C5 (Constitutive Norms) (2nd example: (2) ∪ (20) ∪ {f})

% (i) There must be no fence (f).
&forbidden{f}.

% (ii) If there is a fence, it must be a white (w) fence.
&obligatory{w} :- f, &forbidden{f}.

% (iii) If the cottage is by the sea (s), there must be a fence.
&obligatory{f} :- s.

% If white fence, then fence.
f :- w.

% No white fence if not fence.
-w :- -f.

% Obligatory fence if non violated obligation of white fence.
&obligatory{f} :- &obligatory{w}, not -w.

% Forbidden white fence if non violated prohibition of fence.
&forbidden{w} :- &forbidden{f}, not f.

% There is a fence.
f.
