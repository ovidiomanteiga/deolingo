
import clingo

ex1 = """
park :- not forbidden(park).
"""

ex2 = """
obligatory(work) :- not -obligatory(work).
-obligatory(work) :- reality(weekend).
reality(-weekend).
reality(-work).
"""

ex3 = """
obligatory(fight).
forbidden(fight).
"""

ex4 = """
forbidden(walk).
obligatory(walk_right) :- reality(walk).
reality(walk) :- reality(walk_right).
obligatory(walk) :- obligatory(walk_right).
reality(walk).
reality(walk_right).
"""

ex5 = """
forbidden(fence) :- not -forbidden(fence).
obligatory(white) :- reality(fence).%, forbidden(fence).
-forbidden(fence) :- reality(sea).
reality(fence).
reality(sea).
"""

def run_deolingo(prog=ex1):
    print(f'Hi, Deolingo!')
    ctl = clingo.Control()
    ctl.configuration.solve.models = 0
    prog += "deontic(X) :- obligatory(X)."
    prog += "deontic(X) :- forbidden(X)."
    prog += "contrary_to_duty(X) :- obligatory(X), forbidden(X)."
    prog += "-reality(X):- reality(-X)."
    prog += "reality(-X):- -reality(X)."
    prog += "violation(X) :- obligatory(X), reality(-X)."
    prog += "violation(X) :- forbidden(X), reality(X)."
    prog += "fulfilled(X) :- obligatory(X), reality(X)."
    prog += "fulfilled(X) :- forbidden(X), -reality(X)."
    prog += ":- contrary_to_duty(X), not violation(X)."
    prog += "no_evidence(X) :- not reality(X), deontic(X)."
    prog += "implicit_permission(-X) :- not obligatory(X), deontic(X)."
    prog += "implicit_permission(X) :- not forbidden(X), deontic(X)."
    ctl.add("base", [], prog)
    models = []
    def on_model(m):
        nonlocal models
        models += [m.symbols(shown=True)]
    ctl.ground([("base", [])])
    solved = ctl.solve(on_model=on_model)
    for m in models:
        print("Answer: " + str(m))
    return models


if __name__ == '__main__':
    run_deolingo()
