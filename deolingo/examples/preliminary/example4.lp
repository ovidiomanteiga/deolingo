% Contrary to Duty (CTD)
% I must not walk in the street
% If I walk in the street, I must walk on the right side of the street
&fb{walk}.
&ob{walk_right} :- walk.
walk :- walk_right.
&ob{walk} :- &ob{walk_right}.
walk.
walk_right.