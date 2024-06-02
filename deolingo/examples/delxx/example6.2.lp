
% C6 (Defeasible Deontic Detachment) (2nd example)

%!trace_rule {"There must be no fence"}
&obligatory{-fence}.

%!trace_rule {"The fence must be white if there is a fence"}
&obligatory{white} :- fence.

%!trace_rule {"There must be a fence if the cottage is by the sea"}
&obligatory{fence} :- sea.

%!trace_rule {"Then there must be a fence if there must be a white fence"}
&obligatory{fence} :- &obligatory{white}.

%!trace_rule {"We must put a street mailbox if we put a fence"}
&obligatory{mailbox | fence}.

%!trace_rule {"We must not put a street mailbox if we do not put a fence"}
&obligatory{-mailbox | -fence}.

% Fence or not fence.
1 {fence; -fence} 1.

%!trace {"There is a fence"} fence.
%!trace {"There is no fence"} -fence.

%!show_trace &obligatory{X}.
%!show_trace &forbidden{X}.
