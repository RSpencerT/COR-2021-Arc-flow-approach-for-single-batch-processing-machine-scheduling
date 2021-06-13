# Arc-flow model proposed in:
# Trindade, R. S., de Araújo, O. C. B., Fampa, M. H. C. (2021). Arc-flow approach for single batch-processing machine scheduling. Computers & Operations Research, 134(2021), article 105394. 
# DOI: https://www.doi.org/10.1016/j.cor.2021.105394

param NumberJobs > 0;
param B > 0; 

param alpha > 0;
param MinP  > 0; 
param MaxP  > 0; 
param MinS  > 0; 
param MaxS  > 0; 

# set J := 1..NumberJobs;
set C := 0..B;
set T := 1..alpha;

set ArcJ within {C, C};
set ArcL within {C, C};
param P{T};
param NT{c in C, t in T};
param NTp{c in C, t in T};
param NJ{T};

var f{(i,j) in ArcJ, t in T}    integer >= 0 <= min(NJ[t],NTp[j-i,t]);
var y{(i,j) in ArcL, t in T}    integer >= 0 <= NJ[t];
var v{t in T}                   integer >= 0 <= NJ[t];
var z{c in C, t in T}           integer >= 0 <= NTp[c,t];

# obj function
minimize makespan: sum{t in T} P[t]*v[t];

s.t. FlowConservation{t in T, j in C } :
    (sum{(i,j) in ArcJ} f[i,j,t] + sum{(i,j) in ArcL} y[i,j,t]) -
    (sum{(j,i) in ArcJ} f[j,i,t] + sum{(j,i) in ArcL} y[j,i,t]) =
    if j = 0 then -v[t]
    else if j = B then v[t]
    else 0
    ;

s.t. JobsAssigned1{c in MinS..MaxS, t in T } :
    NT[c,t] - sum{(i,j) in ArcJ : j-i == c} f[i,j,t] =
    if t = 1 then z[c,t]
    else if t = alpha then -z[c,t-1]
    else z[c,t]-z[c,t-1]
    ;