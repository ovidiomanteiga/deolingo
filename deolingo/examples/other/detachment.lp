
% A car arrives at a crossroads...

% Where it is forbidden to turn left.
&forbidden{turn_left}.

% If you turn left, you must use the turning indicator.
&obligatory{left_indicator} :- turn_left.

% The car turns left without the indicator.
turn_left. -left_indicator.

% The car turns left with the indicator.
% turn_left. left_indicator.

% Check if the car violated the rules.
violated_turn_left :- &violated_prohibition{turn_left}.
violated_left_indicator :- &violated_obligation{left_indicator}.
