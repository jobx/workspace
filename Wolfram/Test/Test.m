(* Mathematica Raw Program *)

BeginPackage["Test`"]

fun::usage = "fun[x] computes x^2"

Begin["`Private`"]

fun[x_]:= Module[
	{y},
	y = x^2;
	y
];

End[]

EndPackage[]