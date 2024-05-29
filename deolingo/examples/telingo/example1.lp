
#program dynamic.
shoot | load | wait.

loaded :- load.
loaded :- 'loaded, not unloaded.
unloaded :- shoot, 'loaded, not broken.
unloaded :- 'unloaded, not loaded.
&obligatory{watch} :- &'obligatory{watch}.

:- load, 'loaded.

broken :- shoot, not not &tel { <* unloaded & < <? shoot }.
broken :- 'broken.

#program initial.
unloaded.
&obligatory{watch}.

:- &tel { >*(~loaded | ~shoot) }.
