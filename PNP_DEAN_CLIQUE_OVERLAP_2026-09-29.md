# Dean's fixed exclusion list — clique frame and the overlap seam

**Status:** Step 13, bounded exact extension of the [cycle-certificate result](PNP_DEAN_CYCLE_CERTIFICATE_DISCOVERY_2026-09-29.md). The Dean's incompatibility edges are supplied input and remain fixed. This gives sound, cheaply checkable NO receipts for stated families; it does not give a universal Dean solver.

## 1. One local obligation, with identity retained

Let \(G=(V,E)\) be the Dean's simple undirected graph, \(n=|V|\), target \(k\), and omission budget \(b=n-k\). Let \(y_v=1\) if candidate \(v\) is omitted and \(0\) if selected. An output of size \(k\) requires \(\sum_v y_v=b\). For each explicitly listed carrier \(S\), its edges are checked against the *given* \(E\):

| Carrier | Selection constraint | Required omissions \(d(S)\) |
| --- | --- | --- |
| Clique \(K_q\), all pairs incompatible | \(\sum_{v\in S}(1-y_v)\le1\) | \(q-1\) |
| Simple odd cycle \(C_{2r+1}\) | \(\sum_{v\in S}(1-y_v)\le r\) | \(r+1\) |

A supplied list of pairwise vertex-disjoint carriers gives
\[
\sum_{v\in V}y_v\ \ge\ \sum_S d(S).
\]
If this right-hand side exceeds \(b\), the fixed input is NO. The carrier checker verifies distinct vertex labels, all clique pairs or consecutive cycle edges, the cycles' odd lengths, disjointness, and the arithmetic. A witness with at most \(n\) disjoint carriers contains \(O(n\log n)\) vertex-label bits; verification is polynomial in \(n+m\). For example, sort \(E\), look up the required edges, mark vertices, then add integer obligations. Constructing and choosing useful carriers are separate costs.

## 2. Repair the explicit \(K_4\) chain

For \(t\ge2\), use the *same* connected \(K_4\) chain and target from Step 12. Vertices are \((i,a)\) for \(1\le i\le t\) and \(a\in\{0,1,2,3\}\); all six pairs within each block \(i\) are in \(E\), plus the bridges \(\{(i,3),(i+1,0)\}\) for \(i<t\). The input has \(n=4t\), \(m=7t-1\), maximum degree four, and \(\alpha=t\): at most one selection per block, attained by choosing \((i,1)\) in every block. Its minimum omissions are \(\tau=3t\) and its internal perfect matchings give \(\nu=2t\).

At the previously declared target \(k=2t\), the budget is \(b=2t\). The degree test cannot force an omission because \(\Delta\le4\le b\); matching reaches only \(\nu=b\); the Step 12 disjoint odd-cycle rule reaches at most \(W=2t\), since bridges cannot lie on a cycle and each \(K_4\) holds at most one disjoint triangle. The displayed \(t\) vertex-disjoint cliques instead require \(3t>b\) omissions and prove NO.

The labeled family is explicit. A bridge search and a check that deleting bridges leaves \(t\) copies of \(K_4\) in a path find this frame in \(O(n+m)\) graph operations even under a vertex relabeling. That is a special-case discovery bound. The general cost of selecting a decisive mixed frame has not been established.

| \(t\) | \(n\) | \(m\) | \(\alpha\) | \(\tau\) | Matching / cycle count | Clique count | Budget |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 8 | 13 | 2 | 6 | 4 | 6 | 4 |
| 3 | 12 | 20 | 3 | 9 | 6 | 9 | 6 |
| 4 | 16 | 27 | 4 | 12 | 8 | 12 | 8 |

The table's finite values were independently enumerated from the declared edges. The formulas above prove the family statement.

## 3. Pressure from overlap: the false NO and the repair

Take one \(K_4\) on \(\{0,1,2,3\}\) and one triangle \(\{3,4,5\}\), with no further edges. They meet at the *same vertex* \(3\). Here \(n=6\), \(m=9\), \(\alpha=2\) (for example, \(\{0,4\}\) is a valid selection), and \(\tau=4\). At target \(k=2\), \(b=4\), so the answer is YES. Summing the clique's three required omissions and the triangle's two as \(3+2=5>b\) would return a **false NO**: one omitted vertex can satisfy both constraints. Identity and overlap cannot be projected away.

For two carriers \(A,B\) requiring \(d_A,d_B\) omissions, the safe bound is
\[
\tau(G)\ \ge\ \max\{d_A,d_B,d_A+d_B-|A\cap B|\}.
\]
Indeed, \(\sum_{v\in A\cup B}y_v=\sum_{v\in A}y_v+\sum_{v\in B}y_v-\sum_{v\in A\cap B}y_v\), and the last sum is at most \(|A\cap B|\). In this example the repaired value is \(\max\{3,2,3+2-1\}=4\), exactly the true omission minimum, so it does not falsely reject the valid target.

For a longer supplied mixed list \(S_1,\ldots,S_s\), let \(r_v=|\{i:v\in S_i\}|\). Summing all local obligations while charging each repeated vertex at most \(r_v-1\) extra times yields the sound, possibly weak bound
\[
\tau(G)\ \ge\
\max\!\left\{0,\max_i d(S_i),\sum_i d(S_i)-\sum_{v:r_v>0}(r_v-1)\right\}.
\]
The checker can compute multiplicities directly from stable vertex IDs. Pairwise disjoint frames are the \(r_v\le1\) case. This corrects the arithmetic for supplied overlapping carriers; it does **not** assert an efficient procedure to find the best ones.

## 4. Relation to optimization and the world

These are the clique and odd-cycle inequalities of the stable-set formulation: \(x_v=1-y_v\) is a binary selection variable. [de Vries and Perscheid](https://optimization-online.org/wp-content/uploads/2019/09/7365.pdf) give the odd-cycle inequalities and a polynomial-time separation/extended-formulation route for the **fractional LP relaxation**. That task differs from Step 12's NP-complete decision about a sufficiently strong *vertex-disjoint integral cycle list*. Neither statement cancels the other. Their paper also exhibits the \(K_4\) gap: the fractional vector \(x_v=1/3\) satisfies edge and odd-cycle inequalities but violates the clique inequality \(\sum_{v\in K_4}x_v\le1\).

The distinction can be seen on the declared \(K_4\) chain. The vector \(x_v=1/3\) on all \(4t\) vertices is feasible for every edge and odd-cycle inequality and has value \(4t/3\), whereas the true \(\alpha=t\). At a **separately declared** target \(k=t+1\), this fractional witness prevents the full odd-cycle LP bound from proving NO for \(t\ge3\); the clique list proves NO. This is an integrality-gap witness for that relaxation, not a complexity lower bound and not a change to the earlier \(k=2t\) input.

The same pairwise-conflict model occurs in [wireless link scheduling](https://pmc.ncbi.nlm.nih.gov/articles/PMC4704814/): interfering transmissions form conflict edges, a simultaneous feasible schedule is an independent set, and cliques represent mutually exclusive transmissions. That application assigns weights and may derive a new graph at each time slot. The mathematical transfer here is the validity of the local inequalities for each fixed graph, not a claim to solve the weighted or changing scheduling task.

## 5. Provenance and claim ceiling

Step 11 supplied the explicit connected \(C_5\) family. Step 12 supplied the cycle-list verifier and a \(K_4\) chain that escaped that particular certificate. This step keeps Step 12's target and exact edges for the repair, then gives a separately specified overlap graph and target as the adversarial test. The older GYRO/DEAN frame theorem always had a spanning hypothesis; the historical \(C_5\) CSV without a retained generator is still analogous evidence, not a rerun.

**Admitted:** the clique and mixed overlap bounds are sound; the \(K_4\) family has a linear-time recognizable decisive frame; the naive mixed sum is refuted by a six-vertex YES instance. **Open:** whether a complete, exact, uniformly polynomial-total-cost carrier construction exists for arbitrary Dean \(E,k\). The NP-completeness of the *cycle-only* witness search cannot simply be transferred to the expanded clique/cycle search without a separate reduction. No P-versus-NP resolution follows.
