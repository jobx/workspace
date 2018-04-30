(* Mathematica Test File *)

<<CardDeck`

deck = NewDeck[]


Test[
	Length[ deck]
	,
	52
	,
	TestID->"Test-20071129-S5T7T4"
]

Test[
	First[deck]
	,
	Card[{1,1}]
	,
	TestID->"Test-20071129-W2K8B3"
]

