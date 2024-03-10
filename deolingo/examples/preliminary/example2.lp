% I must normally work,
% On weekends, I have an explicit permission not to work
% It is not a weekend, I decided not to work
&obligatory{work} :- not &omissible{work}.
&omissible{work} :- weekend.
-weekend.
-work.