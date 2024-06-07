
% Park when no evidence on a prohibition (implicit permission)
%!trace_rule {"Can park because it's not explicitly forbidden"}
park :- not &forbidden{park}.

%!show_trace park.
