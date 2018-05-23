(* Mathematica Raw Program *)

BeginPackage["Test`"]

fun::usage = "fun[x] computes x^2"
ED::usage = "edit distance"
Kn::usage = "Knapsack with replacement"

Begin["`Private`"]

fun[x_]:= Module[
	{y},
	y = x^2;
	y
];

Clear[ED];
(* initialization *)
ED[i_, 0] :=
    i;
ED[0, j_] :=
    j;
x = "polynomial";
y = "exponential";
ED[i_, j_] :=
    ED[i, j] = Module[ {c1, c2, c3, best},
                   c1 = If[ Characters[x][[i]] == Characters[y][[j]],
                            0,
                            1
                        ] + 
                     ED[i - 1, j - 1];
                   c2 = 1 + ED[i, j - 1];
                   c3 = 1 + ED[i - 1, j];
                   best = Min[c1, c2, c3];
                   Switch[Position[{c1, c2, c3}, best] // Flatten // First,
                    1, xr[i] = Characters[x][[i]];
                       yr[j] = Characters[y][[j]],
                    2, xr[i] = "-",
                    3, yr[j] = "-"];
                   best
               ];
               
Kn[0] = 0;
Kn[w_] :=
    Kn[w] = Module[ {i, choices, best},
                i = Select[item, #[[1]] <= w &];
                If[ Length[i] == 0,
                    0,
                    choices = i /. {a_Integer, b_Integer} -> Kn[w - a] + b;
                    best = Max[choices]
                ]
            ];
                   
End[]

EndPackage[]