(* Mathematica Package *)

(* Created by the Wolfram Workbench 29-Nov-2007 *)

BeginPackage["CardDeck`"]

(* Exported symbols added here with SymbolName::usage *) 


NewDeck::usage = "NewDeck[] creates a new deck of cards."

Card::usage = "Card[{i,j}] represents a card."

ShuffleCards::usage = "ShuffleCards[ cards] shuffles a number of cards."

FormatCard::usage = "FormatCard[ card] formats a card visually."


Begin["`Private`"]
(* Implementation of the package *)


NewDeck[] :=
	Flatten[ Table[ Card[{i,j}], {i,13}, {j,4} ],1]

ShuffleCards[ cards_] :=
	RandomSample[ cards]



(*
  Formatting code
*)

getSuiteImage[1] := spadeImage
getSuiteImage[2] := clubImage
getSuiteImage[3] := heartImage
getSuiteImage[4] := diamondImage

getName[i_] := ToString[i]
getName[1] := "Ace"
getName[11] := "Jack"
getName[12] := "Queen"
getName[13] := "King"

DeckShuffle[ Cards[ d_]] :=
	Cards[ ]
	

loadImages[] :=
	(
	heartImage = Import[ToFileName[ {packageDir, "images"}, "heart.gif"]];
	clubImage = Import[ToFileName[ {packageDir, "images"}, "club.gif"]];
	spadeImage = Import[ToFileName[ {packageDir, "images"}, "spade.gif"]];
	diamondImage = Import[ToFileName[ {packageDir, "images"}, "diamond.gif"]];
	)

MakeBoxes[ Card[ {i_, j_}], fmt_] :=
	ToBoxes[ FormatCard[ {i,j}], fmt]


FormatCard[ {i_, j_}] :=
	Module[ {name, suiteImage},
		name = getName[i];
		suiteImage = getSuiteImage[j];
		Grid[{{
			Style[name, FontSize -> 18, FontFamily -> "Helvetica"], 
            suiteImage}}, 
 			Alignment -> Bottom,
 			Frame -> True, Spacings -> {{1, {0}, 1}, {1, {0}, 1}}]
	]
	
packageDir = DirectoryName[ System`Private`$InputFileName]
loadImages[]




End[]

EndPackage[]

