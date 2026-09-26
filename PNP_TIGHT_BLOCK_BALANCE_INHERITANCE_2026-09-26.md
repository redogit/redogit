# Tight-Block Balance Inheritance — 2026-09-26

**Program:** synchronized P vs NP proof program
**Predecessor:** `PNP_LOG_SURPLUS_TIGHT_EDGE_CLOSURE_2026-09-26.md`
**Status:** exact structural theorem
**Claim ceiling:** not universal P=NP

## 1. Parent state

Let F be a fully normalized linearly-lean residual with signed clause-variable matrix:

    M = M(F)

satisfying:

    rank(M)=n(F)
    y>0
    M^T y=0.

Let V be a nonempty minimum-surplus variable set and:

    G=F[V].

Let R=Gamma_F(V) be exactly the clauses touching V.

The signed matrix of G is:

    M_G = M[R,V]

after deleting literals outside V.

## 2. Full-column-rank inheritance

Claim:

    rank(M_G)=|V|.

Suppose instead there is a nonzero coefficient vector a on columns V with:

    M_G a = 0.

Extend a to all parent variables by zero outside V.

For rows R, the product is zero by assumption.

For every row outside R, all entries in columns V are zero by definition of R.

Hence:

    M a_extended = 0,

contradicting full column rank of M.

Therefore the tight block inherits full column rank.

## 3. Strict positive-balance inheritance

Restrict the parent positive balance vector y to touching clauses:

    y_R > 0.

For every column v in V, rows outside R have zero entry in that column.

Therefore:

    M_G^T y_R
      =
    M[:,V]^T y
      =
    0.

So G inherits a strictly positive left-kernel vector.

Thus every minimum-surplus tight block of the normalized parent is itself:

    FULL-COLUMN-RANK
    +
    STRICTLY POSITIVELY BALANCED.

## 4. Nullity equals edge thickness

Because V realizes surplus:

    c(G)-n(G)
      =
    |R|-|V|
      =
    sigma(F)
      =
    k.

And rank(M_G)=|V|.

Therefore:

    dim ker(M_G^T)=k.

The surplus thickness is exactly the positive-balance nullity dimension of the tight block.

This is the first exact identity joining the surplus-edge carrier and the positive-balance carrier.

## 5. Circuit-cover inheritance

Apply the positive balance-circuit decomposition theorem directly to G.

Its strictly positive balance vector decomposes into at most:

    k

support-minimal positive balance circuits whose union covers every clause of G.

Therefore every tight block carries:

    EDGE THICKNESS k
    =
    BALANCE NULLITY k
    >=
    NUMBER OF CIRCUITS NEEDED FOR A POSITIVE COVER (at most k).

More precisely:

    circuit-cover count t <= k.

Each positive circuit remains individually tractable by the previously admitted local-decision theorem.

## 6. Degree expansion inside the tight block

Because sigma(G)=k, every nonempty variable set S subseteq V satisfies:

    |Gamma_G(S)|-|S| >= k.

For singleton S={v}:

    vd_G(v) >= k+1

for every v in V.

The non-Mersenne theorem on the UNSAT/lean side supplies a variable with degree at most:

    nM(k)
    <=
    k+1+log2(k).

So in the obstruction door the tight block has a variable in the narrow degree band:

    k+1
    <=
    vd_G(v)
    <=
    k+1+log2(k).

For large k, the additive degree slack above the expansion floor is only logarithmic.

This is a new quantitative rigidity.

## 7. High-surplus reinterpretation

The superlogarithmic region is not merely:

    LARGE PARAMETER.

It is:

    HIGH HALL EXPANSION
    +
    FULL COLUMN RANK
    +
    k-DIMENSIONAL POSITIVE BALANCE NULLSPACE
    +
    <=k POSITIVE CIRCUITS COVERING EVERY CLAUSE
    +
    EACH VARIABLE DEGREE >=k+1.

Thus increasing k strengthens several structural constraints simultaneously.

The core-climb question should exploit this rigidity rather than treating 2^k as the only available cost.

## 8. Next one-degree target

For one tight block G of thickness k, define degree excess:

    e(v)=vd_G(v)-(k+1) >=0.

On the UNSAT/lean side there exists v with:

    e(v)<=log2(k).

Ask whether low excess plus positive-circuit coverage forces one of:

- concentration of v into few balance circuits;
- repeated/redundant opposite-polarity resolvents;
- a small signed separator;
- dominance/functional structure;
- or a projection whose materialized growth can be charged to the k-dimensional balance resource.

This is now the nearest mathematical edge.

## 9. Claim ceiling

    TIGHT BLOCK FULL-RANK INHERITANCE = EXACT
    TIGHT BLOCK POSITIVE-BALANCE INHERITANCE = EXACT
    NULLITY = SURPLUS THICKNESS = EXACT
    CIRCUIT COVER <= k = EXACT
    DEGREE FLOOR k+1 = EXACT
    UNSAT-SIDE LOW EXCESS <= log k = EXACT VIA NON-MERSENNE BOUND
    LOW EXCESS -> POLYNOMIAL PROJECTION = OPEN
    UNIVERSAL P=NP = OPEN
