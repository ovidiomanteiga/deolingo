% I must normally work,
% On weekends, I have an explicit permission not to work
% It is not a weekend, I decided not to work
%!trace_rule {"% It's obligatory to work"}
&obligatory{work} :- not &omissible{work}.
&omissible{work} :- weekend.
-weekend.
-work.

%!trace {"% is omissible",X} &omissible{X}.
%!show_trace weekend.
%!show_trace work.
