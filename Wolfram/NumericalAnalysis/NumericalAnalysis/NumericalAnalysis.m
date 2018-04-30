(* Mathematica Package *)

(* Created by the Wolfram Workbench 18-Jul-2007 *)

(*
  This package is a modified copy of the NumericalCalculus package, 
  that is provided to help with documentation generation.
*)

BeginPackage["NumericalAnalysis`"]

NumLimit::usage = "NumLimit[expr, x->x0] numerically finds the limiting \
value of expr as x approaches x0."

NumD::usage =
"NumD[expr, x, x0] gives a numerical approximation to the derivative of expr \
with respect to x at the point x0."

NumSeries::usage =
"NumSeries[f, {x, x0, n}] gives a numerical approximation to the series \
expansion of f about the point x == x0 through (x-x0)^n."


NumResidue::usage =
"NumResidue[expr, {x, x0}] uses NIntegrate to numerically find the residue \
of expr near the point x = x0."


Begin["`Private`"]
(* Implementation of the package *)


(*
 Utilities used elsewhere
*)

newre[re_, rat_] := If[MatchQ[re, {_, _}],
				{(re[[1]] - rat)/(1-rat), re[[2]]},
				(re - rat)/(1 - rat)];
				
es[seq_, ratiolist_] :=
    Module[{newseq=seq, rat, dd=1, ratpow=1, r1r, i, j, l=Length[seq], tmp},
	(* Transform the sequence of terms into a new sequence of terms based
	on the given ratio.  Recursively repeat the transform with the
	various values of ratio in the ratiolist.  Finally, sum the
	transformed sequence. *)
	If[l < 2,
		Message[EulerSum::short, seq];
		Return[$Failed]];
	rat = Apply[Plus, Abs[seq]];
	If[rat == 0., Return[rat]];
	rat = If[ratiolist === Automatic, Automatic, ratiolist[[1]]];
	If[rat === Automatic,
		rat = seq[[l]]/seq[[l-1]];
		If[!NumberQ[rat],
			Message[EulerSum::ernum, rat];
			Return[$Failed]
			],
	    (* else *)
		If[Head[rat] === List && Length[rat] == 2, {rat, dd} = rat];
		If[!IntegerQ[dd],
			Message[EulerSum::erpair, ratiolist[[1]]];
			Return[$Failed]
			]
		];
	If[rat == 0,
		Message[EulerSum::zrat];
		Return[$Failed];
		];
	ratpow = 1;
	Do[newseq[[i]] /= (ratpow *= rat), {i,2,l}];
	Do[Do[newseq[[j]]  = Together[newseq[[j]]-newseq[[j-1]]], {j,l,i,-1}],
		{i,2,l}];
	r1r = rat/(1-rat);
	ratpow = 1;
	Do[newseq[[i]] *= (ratpow *= r1r), {i, 2, l}];
	newseq = Together[newseq];
	If[(ratiolist === Automatic) || (Length[ratiolist] == 1),
		Apply[Plus, newseq]/(1-rat),
	    (* else *)
		r1r = Together[newre[#, rat]& /@ Drop[ratiolist, 1]];
		tmp = es[Drop[newseq, dd], r1r];
		If[!FreeQ[tmp, $Failed], Return[$Failed]];
		(Apply[Plus, Take[newseq, dd]] + tmp)/(1-rat)
		]
	];





(*
  NumD
*)


Options[NumD] = {WorkingPrecision -> MachinePrecision, Method -> NumEulerSum}

NumD[expr_, x_, x0_, opts___] := NumD[expr, {x, 1}, x0, opts] /; (Head[x] =!= List);

NumD[expr_, {x_, n_}, x0_, opts___] :=
    Module[{prec = WorkingPrecision  /. {opts} /. Options[NumD],
	h = SetPrecision[ 1, Infinity],
	terms = 7,
	meth = Method /. {opts} /. Options[NumD],
	nder},
	nder /; (nder = If[meth === NIntegrate,
			ndni[expr, x, n, x0, prec, h],
			nd[expr, x, n, x0, prec, h, terms]
			];
		$Failed =!= nder)
	]

ndni[f_, x_ , n_, x0_, prec_, r_] :=
    Module[{ft, t, z, ans},
	ft = f /. x -> (x0 + z);
	ans = NIntegrate[z = r E^(I t); ft/z^n, {t, 0, 2Pi},
		Method -> Trapezoidal, WorkingPrecision -> prec];
	If[!NumberQ[ans], Return[$Failed]];
	Gamma[n+1]/(2 Pi) ans
	];

nd[expr_ , x_ , n_, x0_, prec_, h_, terms_] :=
    Module[{seq, eseq, dseq, nx0, nh, i, j},
	(* form a sequence of divided differences and use Richardson
	extrapolation to eliminate most of the truncation error. *)
	nx0 = N[x0, prec];
	nh = N[2h, prec];
	eseq = Table[Null, {n+1}];
	seq = Table[Null, {terms}];
	Do[eseq[[i]] = N[expr /. x -> nx0+(i-1)nh, prec], {i,n/2+1}];
	Do[	Do[eseq[[2i-1]] = eseq[[i]], {i,Floor[n/2]+1,2,-1}];
		nh /= 2;
		Do[eseq[[i]]=N[expr /. x->nx0+(i-1)nh,prec],{i,2,n+1,2}];
		dseq = eseq;
		While[Length[dseq]>1,dseq=Drop[dseq,1]-Drop[dseq,-1]];
		seq[[j]] = dseq[[1]]/(nh^n), {j, terms}];
	Do[	j = 2^i;
		seq = (j Drop[seq,1] - Drop[seq,-1])/(j-1),
		{i, terms-1}];
	seq[[1]]
	];
	
(*
 NumSeries
*)


Options[NumSeries] = {WorkingPrecision -> MachinePrecision};

NumSeries[f_, {x_, x0_, n_Integer}, opts___] :=
    Module[{p, r, ans},
		ans /; (p = WorkingPrecision /. {opts} /. Options[NumSeries];
		r = 1;
		TrueQ[p > 0] && TrueQ[r > 0] && TrueQ[n > 0] &&
		    (ans = nseries0[f, {x, x0, n}, p, r]) =!= $Failed)
	];

nseries0[f_, {x_, x0_, n_}, p_, r_] :=
    Module[{data, m, k, nx0, n2pi},
	m = 2^(2 + Ceiling[Log[2, n]]);
	nx0 = N[x0, p];
	n2pi = N[2 Pi I, p]/m;
	data = Table[N[f /. x -> nx0 + r E^(k n2pi), p], {k, 0, m-1}];
	If[!VectorQ[data, NumberQ], Return[$Failed]];
	data = InverseFourier[data];
	data = Join[Take[data, -n], Take[data, n+1]] (r^Range[n, -n, -1]);
	SeriesData[x, x0, data m^(-1/2), -n, n+1, 1]
	];


(*
NumResidue
*)
NumResidue[f_, {x_, x0_}, opts___] :=
    Module[{ans},
    	ans = f;
		ans
	]


Options[NumResidue] = {
		     WorkingPrecision -> MachinePrecision,
		     PrecisionGoal -> Automatic};

NumResidue[f_, {x_, x0_}, opts___] :=
    Module[{ans},
	ans /; (ans = nres[f, x, x0, opts]) =!= $Failed
	];

NumResidue::rad = "Radius `1` is not a positive number."



nres[f_, x_, x0_, opts___] :=
    Module[{ft, r, t, z},
	r = 1/100;
	If[!NumericQ[r] || !TrueQ[r > 0],
		Message[NumResidue::rad, r];
		Return[$Failed]
		];
	ft = f /. x -> (x0 + z);
	If[Length[{opts}]===0,NIntegrate[Evaluate[z = r E^(I t); z ft], {t, 0, 2Pi}, Method -> Trapezoidal]/(2 Pi),NIntegrate[Evaluate[z = r E^(I t); z ft], {t, 0, 2Pi}, Method -> Trapezoidal,
		Evaluate[Sequence@@FilterRules[{opts}, Options[NIntegrate]]]]/(2 Pi)]
	];



(*
   NumLimit
*)

Options[NumLimit] = {Direction -> Automatic,
			WorkingPrecision -> MachinePrecision, 
			Method -> NumEulerSum, WynnDegree -> 1}


NumLimit[e_, x_ -> x0_, opts___] :=
    Module[{prec = WorkingPrecision  /. {opts} /. Options[NumLimit],
	dir = Direction /. {opts} /. Options[NumLimit],
	scale = SetPrecision[1, Infinity],
	terms = 7,
	meth = Method /. {opts} /. Options[NumLimit],
	degree = WynnDegree /. {opts} /. Options[NumLimit],
	limit},
	limit /; ((meth === SequenceLimit) || (meth === NumEulerSum)) &&
		(limit = If[Head[x0] === DirectedInfinity,
			infLimit[e,x,x0,prec,scale,terms,degree,meth],
			If[dir === Automatic, dir = -1];
			scale = -Sign[dir] Abs[scale];
			finLimit[e,x,x0,prec,scale,terms,degree,meth]];
		$Failed =!= limit)
	];

NumLimit::notnum = "The expression `1` is not numerical at the point `2` == `3`."

NumLimit::baddir = "Cannot approach `1` from the direction `2`."

NumLimit::noise = "Cannot recognize a limiting value.  This may be due to  \
noise resulting from roundoff errors in which case higher WorkingPrecision,  \
fewer Terms, or a different Scale might help."

infLimit[e_, x_, x0_, prec_, scale_, terms_, degree_, meth_] :=
    Module[{seq, ne, nx, i, dirscale, limit, tmp},
	(* form a sequence of values that approach the limit at infinity
	and the extrapolate *)
	If[Length[x0] != 1, Return[$Failed]];
	dirscale = N[x0[[1]], prec];
	dirscale = Abs[N[scale, prec]] dirscale/Abs[dirscale];
	If[!NumberQ[dirscale],
		Message[NumLimit::baddir, x0, dirscale];
		Return[$Failed]];
	seq = Table[Null, {terms}];
	tmp = Do[	nx = dirscale 10^(i-1);
		ne = N[e /. x -> nx, prec];
		If[!NumberQ[ne] || ne === Overflow[] || ne === Underflow[],
			Message[NumLimit::notnum, ne, x, nx];
			Return[$Failed]];
		seq[[i]] = ne, {i,terms}];
    If[tmp === $Failed, Return[$Failed]];
	limit = If[meth === NumEulerSum,
			tmp = es[Drop[seq,1] - Drop[seq,-1], Automatic];
			If[!FreeQ[tmp, $Failed], Return[$Failed]];
			seq[[1]] + tmp,
		    (* else *)
			SequenceLimit[seq, Method->{"WynnEpsilon", "Degree" -> degree}]];
	(*  we must check that we have a reasonable answer *)
	If[limit == seq[[1]] || (NumberQ[limit] &&
				Abs[limit-seq[[1]]] > Abs[limit-seq[[-1]]]),
		limit, Message[NumLimit::noise]; $Failed]
	];

finLimit[e_, x_, x0_, prec_, scale_, terms_, degree_, meth_] :=
    Module[{seq, ne, nx, nx0, i, dirscale, limit, tmp},
	(* form a sequence of values that approach the limit at x0 
	and the extrapolate *)
	nx0 = N[x0, prec];
	dirscale = N[scale, prec];
	If[!NumberQ[dirscale] || !NumberQ[nx0],
		Message[NumLimit::baddir, nx0, dirscale];
		Return[$Failed]];
	seq = Table[Null, {terms}];
	tmp = Do[	nx = nx0 + dirscale/10^(i-1);
		ne = N[e /. x -> nx, prec];
		If[!NumberQ[ne],
			Message[NumLimit::notnum, ne, x, nx];
			Return[$Failed]];
		seq[[i]] = ne, {i,terms}];
    If[tmp === $Failed, Return[$Failed]];
	limit = If[meth === NumEulerSum,
			tmp = es[Drop[seq,1] - Drop[seq,-1], Automatic];
			If[!FreeQ[tmp, $Failed], Return[$Failed]];
			seq[[1]] + tmp,
		    (* else *)
			SequenceLimit[seq, Method->{"WynnEpsilon", "Degree" -> degree}]];
	(*  we must check that we have a reasonable answer *)
	If[NumberQ[limit] && Abs[limit-seq[[1]]] > Abs[limit-seq[[-1]]],
		limit, Message[NumLimit::noise]; $Failed]
	];


End[]

EndPackage[]

