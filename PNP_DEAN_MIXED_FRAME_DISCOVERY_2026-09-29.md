# Dean's fixed list — mixed-frame discovery and its linear boundary

**Status:** approved Step 14, a bounded continuation of [Step 13](PNP_DEAN_CLIQUE_OVERLAP_2026-09-29.md). The incompatibility graph is supplied and fixed. This step provides a sound polynomial route for a fixed-size catalog of clique and odd-cycle NO carriers, then gives an explicit connected NO graph on which even the complete clique/odd-cycle linear system is inconclusive. It is not an exact universal Dean solver or a resolution of P versus NP.

## 1. Object, obligation, and certificate

Let \(G=(V,E)\) be the supplied simple undirected incompatibility graph, \(n=|V|\), the requested independent-set size \(k\), and omission budget \(b=n-k\). For an integral omission vector \(y\in\{0,1\}^V\), every given edge needs an omitted endpoint. A verified clique \(S=K_q\) requires \(d(S)=q-1\) omissions; a verified simple odd cycle \(S=C_{2r+1}\) requires \(d(S)=r+1\). Verification checks vertex identity and the required input edges, not a reconstructed or changed edge list.

Given any finite list of such carriers \(S_i\) and nonnegative **rational** weights \(\lambda_i\), set

\[
L_v=\sum_{i:v\in S_i}\lambda_i,\qquad
B(\lambda)=\sum_i\lambda_i d(S_i)-\sum_{v\in V}\max(0,L_v-1).
\]

**Weighted overlap certificate.** Every valid integral omission set \(T\) satisfies \(|T|\ge B(\lambda)\). To prove it, multiply each local requirement by \(\lambda_i\) and sum:

\[
\sum_i\lambda_i d(S_i)\le\sum_v L_v1_T(v)
\le\sum_v\bigl(1+\max(0,L_v-1)\bigr)1_T(v)
\le |T|+\sum_v\max(0,L_v-1).
\]

Thus **\(B(\lambda)>b\)** is a sound NO receipt. A verifier checks each listed carrier, each rational weight and multiplicity, then compares exact rational numbers; its time is polynomial in the input and receipt bit lengths. Unit weights on a selected list give precisely Step 13's repeated-vertex correction. A single unit-weight carrier or the empty list gives its local bound or zero. No use of a solver's floating-point status is needed to validate an emitted certificate.

For a supplied carrier matrix \(A_{iv}=1_{v\in S_i}\), the strongest bound in this weighted class is the dual of

\[
\begin{array}{ll}
\text{minimize}&\sum_v y_v\\
\text{subject to}&Ay\ge d,\quad 0\le y\le1.
\end{array}
\]

Its explicit dual maximizes \(d^\top\lambda-\sum_v\mu_v\), with \(A^\top\lambda-\mu\le\mathbf1\) and \(\lambda,\mu\ge0\); at fixed \(\lambda\), the cheapest \(\mu_v\) is \(\max(0,L_v-1)\). The upper box bounds \(y_v\le1\) matter: in Step 13's \(K_4\) and triangle sharing one vertex, \(\lambda=(1,1)\) and a penalty of one on that shared vertex give \(B=3+2-1=4\), not the false uncorrected sum five. At the previously stated \(k=2,b=4\), this correctly leaves the YES instance intact.

## 2. A discoverable, bounded route

For a **fixed maximum carrier size**, enumerate every supplied-edge clique of size 2, 3 or 4 and every simple five-cycle. Testing five-vertex sets with the finitely many cyclic orders gives at most \(O(n^5)\) candidates and polynomial bit-size rows. Solve the displayed rational LP, export and independently check a rational dual. A bound above \(b\) returns NO; a separately supplied and checked independent set of size \(k\) returns YES; otherwise return **UNKNOWN**. This is a polynomial-total-cost partial NO procedure for this fixed catalog, not a complete exact algorithm or a polynomial YES search. A larger *fixed* clique rank and odd-cycle length also remain polynomial with exponents depending on those constants.

There is a separate polynomial route for **all** odd-cycle rows. After checking edge inequalities, the edge weights \(w_{uv}=y_u+y_v-1\) are nonnegative. On an odd cycle \(C\), \(\sum_{uv\in C}w_{uv}=2\sum_{v\in C}y_v-|C|\); its row is violated exactly when this sum is less than one. Shortest paths between opposite parity copies of a vertex find a minimum odd closed walk; removing repeated subwalks yields a violated simple odd cycle when one exists. This is the known polynomial separation construction; the cited paper separately supplies a polynomial-size extended formulation for the full odd-cycle LP, even though there may be exponentially many odd cycles. An informal add-one-row-and-resolve loop has no polynomial iteration bound asserted here. [de Vries and Perscheid, *A smaller extended formulation for the odd cycle inequalities of the stable set polytope*](https://optimization-online.org/wp-content/uploads/2019/09/7365.pdf).

Unbounded clique separation is different. At the fractional selection vector \(x_v=1/(r-1)\), \(r\ge3\), every edge inequality holds and a clique row \(\sum_{v\in Q}x_v\le1\) is violated exactly if \(|Q|\ge r\). An algorithm separating arbitrary clique rows would decide the standard CLIQUE problem. Fixed \(K_4\) enumeration is not affected by this reduction. Exact **integral** optimization over even all supplied edge \(K_2\) rows is Vertex Cover. Neither observation proves that the decision “some unrestricted mixed-frame bound crosses this budget” is NP-complete; that question is not classified by this step. [Karp, *Reducibility Among Combinatorial Problems*](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf).

## 3. Counterprobes against discovery and overlap

| Fixed graph and declared target | Exact result | What the frame route actually shows |
| --- | --- | --- |
| \(K_4\) on \(a,b,c,d\), plus \(e\) adjacent exactly to \(a,b\) and \(f\) adjacent exactly to \(c,d\); \(n=6,m=10,k=3,b=3\). | \(\alpha=2,\tau=4\): NO. | Any first carrier of maximum omission weight three (the \(K_4\) or a five-cycle) leaves no residual carrier, so a disjoint greedy score stays three. Disjoint triangles \(a,b,e\) and \(c,d,f\) require four. The fixed catalog finds them. |
| Odd wheel with a \(C_5\) rim \(0,1,2,3,4\) and hub \(h\) adjacent to all rim vertices; \(n=6,m=10,k=3,b=3\). | \(\alpha=2,\tau=4\): NO. | Even the best **vertex-disjoint** clique/odd-cycle list reaches only three. A rational mix of overlapping rim and triangle rows gives \(B=19/5>b\), so the weighted route proves NO. |
| \(K_4(a,b,c,d)\) joined by one bridge to \(C_5(e,f,g,h,i)\); \(n=9,m=12,k=4,b=5\). | \(\alpha=3,\tau=6\): NO. | The disjoint mixed \(K_4\) and \(C_5\) rows require \(3+3=6>b\); neither row alone crosses the budget. |
| Step 13's \(K_4(0,1,2,3)\) and triangle \((3,4,5)\); \(n=6,k=2,b=4\). | \(\alpha=2,\tau=4\): YES. | The weighted penalty for vertex 3 turns the naive false-NO score five into the sound score four. |
| \(K_4(a,b,c,d)\) and \(C_5(a,b,c,e,f)\) sharing \(a,b,c\); \(n=6,k=3,b=3\). | \(\alpha=2,\tau=4\): NO. | Unit weighting of only these two rows gives \(3+3-3=3\), which is sound but inconclusive. The short catalog finds the disjoint \(K_4(a,b,c,d)\) and edge \(K_2(e,f)\), reaching four. The overlap correction for the chosen pair need not be tight. |

The first graph is connected and the winning two triangles are vertex-disjoint. The declared greedy policy selects a remaining carrier with highest local omission weight, removes all its vertices, and repeats. A first \(K_4\) leaves two nonadjacent vertices; a first weight-three five-cycle leaves one vertex. Either tie choice stops at three. This is a failure of that policy, not an impossibility theorem for every greedy rule. The last example distinguishes a safe bound from a complete one; adding other verified rows may recover what a chosen pair misses.

The odd wheel isolates the gain from fractional overlap accounting. The rim five-cycle has omission requirement three. Each of the five triangles \((h,i,i+1\bmod5)\) has requirement two. Put weight \(3/5\) on the rim and \(1/5\) on **each** triangle. A rim vertex lies in two hub triangles, so its load is \(3/5+2/5=1\); the hub lies in five triangles, so its load is also one. There is no penalty and

\[
B=(3/5)3+5(1/5)2=19/5>3.
\]

Every clique has at most three vertices. A disjoint frame choosing the rim cycle uses five vertices and scores three; a triangle uses the hub and two adjacent rim vertices, after which the remaining three rim vertices contain at most one disjoint edge; other five-cycles use five vertices. Thus **every vertex-disjoint frame** scores at most three. Conversely the fractional LP point \(y_h=4/5\), \(y_i=3/5\) on all five rim vertices satisfies every clique and odd-cycle row and totals \(19/5\), so the displayed rational dual is optimal for this wheel. This is a strict improvement over the Step 12/13 disjoint-list rule on this input, while remaining an exact rational NO receipt.

## 4. Even all clique and odd-cycle rows leave one unit hidden

Let \(H=\overline{C_7}\), with vertices \(0,\ldots,6\): two labels are adjacent in \(H\) exactly when they are not consecutive modulo seven. Make three copies \(H_0,H_1,H_2\), and add only bridges \((H_0,0)(H_1,0)\) and \((H_1,0)(H_2,0)\). The connected graph has \(n=21\) and \(m=3(21-7)+2=44\). Each block permits at most two selections, because an independent set in \(H\) is a clique in \(C_7\). Selecting labels 2 and 3 in each block avoids the bridges and attains \(\alpha=6\). Hence \(\tau=15\); at \(k=7,b=14\), the answer is **NO**.

Nevertheless, put \(x_v=1/3\) for every selection variable, or \(y_v=2/3\) for every omission variable. A clique in each \(H_i\) has size at most three, since it is an independent set in \(C_7\); a cross-block clique is at most a bridge edge. Every clique inequality therefore holds. Every cycle lies inside one block because bridges are cut edges. For every odd cycle of length \(\ell\ge3\), \(\ell/3\le(\ell-1)/2\), so **every** odd-cycle selection inequality holds too. Yet \(\sum_v y_v=14=b\). No weighted certificate from even the complete collection of these rows can cross the budget.

The gap is exactly certified, not just observed numerically. Each \(H_i\) has seven triangles and each vertex belongs to three of them. Assign weight \(1/3\) to each of the 21 triangle rows. Every vertex has load one, so the penalty is zero and \(B=21(2/3)=14\). The fractional \(y\) attains 14, while the integral optimum is 15. The missing distinction is integrality. For each block the valid rank inequality \(\sum_{v\in H_i}x_v\le2\) would close the example, but discovering and charging a new family of rank carriers is a **later** question, not part of this step.

## 5. Finite check and world connection

A disposable Python 3.12.14 / SciPy 1.17.0 probe enumerated independent sets on the graphs of at most nine vertices, enumerated the fixed \(K_2,K_3,K_4,C_5\) catalog, evaluated displayed dual weights with exact `Fraction` arithmetic, and solved the bounded catalog LP. The 21-vertex \(\alpha\) and all-length-cycle claims follow from the proof above; a separate exact branch search also obtained \(\alpha=6\). Results: greedy-six \((\tau,B_\mathrm{LP},B_\mathrm{largest})=(4,4,3)\); odd wheel \((\tau,B_\mathrm{LP},B_\mathrm{weighted})=(4,19/5,19/5)\); mixed \(K_4+C_5=(6,6)\); shared-vertex YES \((4,4)\); loose selected overlap \((4,4,3)\); and anti-\(C_7\) chain \((15,14,14)\). The finite script was a disposable research probe, not a reusable solver; SHA-256: script `e7b8882cc1d9195740cad15e5a8f505160398252a0ccedd714f2b8c230c29809`, output `feed91b4533ac6207e2d96f760da4a3adc39e5600d5a0055883806dabfcf900f`, Mathbox version-1 manifest `4afae06741a09da59f14ac9519d0cc86f1963ad1476efc7cb3867678d52a972e`. The manifest validated under the installed checker; its legacy provenance limits and the LP's floating arithmetic remain distinct from the exact proofs and rational receipts.

For a fixed symmetric wireless interference graph, a requested simultaneous batch of \(k\) links is an independent-set obligation. A sound \(B>b\) receipt says the requested batch cannot fit under those pairwise conflicts; **UNKNOWN** says nothing about whether it can. Reweighting links, changing the graph between time slots, or using interference beyond pairwise conflicts needs its own model and verification. The graph analogy does not transfer an algorithmic guarantee to the dynamic system.

## 6. Claim ceiling and Homeward

**Admitted:** checked rational weighted receipts are sound; fixed-size mixed catalogs and their LP are polynomial; the greedy rule has a six-vertex failure; weighted overlap closes the six-vertex wheel when every disjoint list stalls; the full clique/odd-cycle linear family has a connected 21-vertex integrality gap at an actual NO target. **Not admitted:** that the chosen catalog is complete, that arbitrary useful clique discovery is polynomial, that a numeric LP status proves NO without a checked dual, or that any general Dean instance is decided in polynomial time. The source graph, target, counterexamples, finite probe scope, and failed rule remain recoverable. `P ?= NP` remains open.
