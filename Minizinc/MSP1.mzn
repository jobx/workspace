include "globals.mzn";

% the sequence %
array[int] of int : seq = [5, 15, -30, 10, -5, 40, 10];
var 1..length(seq) : i;
var 1..length(seq) : j;

%constraint i <= j;

solve maximize sum ([seq[a] | a in i..j where i <= j]);

output ["i = \(i) ", "j = \(j) "];