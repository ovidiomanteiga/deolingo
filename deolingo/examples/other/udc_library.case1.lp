
document("AIMA").
document("The Book of Why").
document("Think Fast. Think Slow.").
document("The Art of Loving").
document("The C Programming Language").
document("Causality").
document("Solving the Frame Problem").

member(udc, "Joe").
member(udc, "Ray").
member(udc_alumni, "Irene").

member(user_group(2), "Joe").
member(user_group(5), "Ray").
member(user_group(6), "Irene").

borrowed("AIMA", "Irene", 31).
borrowed("AIMA", "Irene").
borrowed("The Book of Why", "Irene").
borrowed("Think Fast. Think Slow.", "Irene").
borrowed("The Art of Loving", "Irene").
borrowed("The C Programming Language", "Irene").
borrowed("Causality", "Irene").
borrowed("Solving the Frame Problem", "Irene").

overdue("AIMA", "Irene").
-return("AIMA", "Irene").
