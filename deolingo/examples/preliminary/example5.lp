% (Normally) there must be no fence
% But if you do put a fence, it must be white
% By the sea, you can put a fence
% You decide to put a fence
&forbidden{fence} :- not &permitted{fence}.
&obligatory{white} :- fence, &forbidden{fence}.
&permitted{fence} :- sea.
fence.
% Should I paint it in white? (Yes)
sea.
% Should I paint it in white by the sea? (No)