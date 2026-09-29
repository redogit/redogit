# Dean's fixed list — one local rounding degree

**Status:** approved Step 15, a bounded repair of the exact 21-vertex integrality gap in [Step 14](PNP_DEAN_MIXED_FRAME_DISCOVERY_2026-09-29.md). The incompatibility graph and target are supplied and fixed. The only new carrier is a verified seven-vertex \(\overline{C_7}\) pattern. The result is a sound partial NO certificate, not a general rank separator, exact universal solver, or resolution of P versus NP.

## 1. The lost unit and the one-degree repair

Use selection variables \(x_v\in\{0,1\}\) and omissions \(y_v=1-x_v\). Label a candidate carrier \(H\) by \(0,\ldots,6\) modulo seven, with every pair **except consecutive labels** required to be an input edge. For \(i=0,\ldots,6\), the triple \(T_i=\{i,i+2,i+4\}\) is a clique. The seven existing clique inequalities each say \(x(T_i)\le1\), and every vertex occurs in exactly three triples. Sum them, then take **one local integer rounding step**:

\[
3x(H)\le7,\qquad x(H)\in\mathbb Z
\quad\Longrightarrow\quad x(H)\le\lfloor7/3\rfloor=2.
\]

Equivalently, the seven triangle requirements give \(3y(H)\ge14\); integrality yields \(y(H)\ge\lceil14/3\rceil=5\). This is the fixed odd-antihole rank inequality, already known in the stable-set literature; it is valid even if additional edges occur among the seven labels. It is **one rounding operation on the existing local rows**, not a new unrestricted rank-inequality engine. The fractional point \(x_v=1/3\) on \(H\) satisfies every triangle row exactly and has \(x(H)=7/3\), so it fails precisely the rounded inequality. The seven triangles collectively test all 14 required edges; some edges occur in more than one triangle.

For three separate occurrences, **round each block before adding**: \(5+5+5=15\). If instead the unrounded inequalities are first summed across all three blocks, they give \(3y(V)\ge42\), hence only \(y(V)\ge14\). This order of operations accounts for the missing unit in Step 14. No row is inferred for an unverified block.

## 2. Fixed-input admission and certificate cost

A supplied occurrence consists of seven **distinct** input vertex IDs \(\phi(0),\ldots,\phi(6)\). Admit it only after checking that each of the 14 unordered pairs \(\{\phi(i),\phi(j)\}\) with \(j\not\equiv i\pm1\pmod7\) is present in the fixed input edge set. Nonedges on consecutive labels need not be checked: extra input edges cannot invalidate this upper bound on selection. A local verifier performs 14 edge lookups after checking the seven identities, then checks the integer row \(d(H)=5\). A missing required edge rejects this occurrence.

The weighted overlap receipt of Step 14 is reused unchanged. For any finite supplied list of admitted occurrences, old verified clique/odd-cycle rows, and nonnegative rational weights \(\lambda_i\), its bound is

\[
L_v=\sum_{i:v\in S_i}\lambda_i,\qquad
B=\sum_i\lambda_i d_i-\sum_v\max(0,L_v-1).
\]

Here an admitted \(H\) has \(d_i=5\). Any integral omission set \(T\) satisfies \(\sum_i\lambda_i d_i\le\sum_v L_v1_T(v)\le |T|+\sum_v\max(0,L_v-1)\); therefore \(B>n-k\) is a checkable **NO**. An explicitly checked independent \(k\)-set is **YES**; otherwise return **UNKNOWN**. The verifier uses exact rational arithmetic with cost polynomial in the input, receipt length, and bit lengths.

The discovery scope is fixed to this one seven-vertex motif. Exhaustively testing seven-subsets and their finitely many label orders is formally \(O(n^7)\) adjacency work for fixed motif size, but this is not a practical blanket runtime promise. A resource-capped search or supplied-candidate workflow returns **UNKNOWN** on exhaustion. Neither all rank inequalities nor arbitrary useful carriers are separated here.

## 3. Exact NO, one-edge YES, and overlap counterprobes

Take Step 14's connected graph: three copies \(H_0,H_1,H_2\) of \(\overline{C_7}\), joined only by bridges \((H_0,0)(H_1,0)\) and \((H_1,0)(H_2,0)\). It has \(n=21,m=44\). The local row allows at most two selected vertices in each block, while labels 2 and 3 in each block give six selections and avoid the bridges. Thus \(\alpha=6,\tau=15\). At the declared \(k=7,b=n-k=14\), unit weight on each of the three verified \(H\) rows gives \(B=15>14\): **NO**. The old complete clique/odd-cycle LP reaches exactly 14 using \(x_v=1/3\); the new local rounding closes its one-unit gap.

Now delete only the required edge \((H_0,0)(H_0,2)\). The graph has \(n=21,m=43\), and the first block admits labels 0, 1, 2 together. An explicit independent seven-set is

\[
\{(H_0,0),(H_0,1),(H_0,2),(H_1,3),(H_1,4),(H_2,3),(H_2,4)\}.
\]

At the **same** \(k=7,b=14\), the answer is **YES** (indeed \(\alpha=7,\tau=14\)). A rule admitting the altered first block merely because it resembles \(\overline{C_7}\) would charge three false \(d=5\) rows and announce \(B=15>b\), a false NO. The 14-edge verifier rejects that block; it admits only the remaining genuine copies. This counterprobe forces the admission condition, not a wider carrier family.

For the overlap check, glue two genuine \(H\) copies at their label-0 vertex and add no other cross edges. There are 13 vertices; each copy allows two selections, and labels 2 and 3 in each give \(\alpha=4,\tau=9\). At \(k=4,b=9\), naive \(5+5=10\) would falsely announce NO. The existing overlap penalty charges one for the shared vertex of load two, giving \(B=5+5-1=9\), correctly inconclusive on this YES graph. No new overlap rule is needed.

## 4. Check, relation to the world, and claim ceiling

The proof above uses only the fixed edges, seven local triangle rows, integrality, and the earlier checked overlap inequality. A disposable Python 3.12.14 counterprobe enumerated all independent sets of the 21-vertex one-edge deletion (3,492 sets), found \(\alpha=7\) and the displayed witness, and tested all 14 single required-edge deletions against the strict occurrence check; it printed `PASS exact one-edge counterprobe`. Script SHA-256: `6e536c83e8d7bfd050363fdb7a38ac5800e96b88033dca8e9d90bb9a161a9cca`. The finite computation checks these fixtures, while the counting proof establishes the carrier inequality for every admitted occurrence.

For a **fixed symmetric pairwise wireless-interference graph**, a seven-link conflict pattern of this form forbids selecting more than two links in one simultaneous batch. A scheduler can use the checked local bound to reject an impossible requested batch, while an UNKNOWN result must remain undecided. Mobility, changing interference, weights, and higher-order effects are separate models; no physical deployment or universal algorithm is inferred.

The rank inequality is established, not novel: Euler, Jünger and Reinelt discuss odd-anticycle inequalities and their earlier attribution to Padberg in [*Generalizations of Cliques, Odd Cycles and Anticycles and Their Relation to Independence System Polyhedra*](https://pubsonline.informs.org/doi/10.1287/moor.12.3.451) (1987). The wider rank-separation problem is separate; see Coniglio and Gualandi, [*On the exact separation of rank inequalities for the maximum stable set problem*](https://optimization-online.org/2014/08/4514/) (2014). No facet assertion is made for this embedded occurrence in an arbitrary larger graph.

**Admitted:** the exact seven-label carrier and its single local rounding step; polynomial verification of supplied rows and rational weighted NO receipts; this three-block NO, one-edge YES, and shared-vertex YES; fixed-size discovery as a formal high-degree polynomial bound with UNKNOWN on an operational cap. **Not admitted:** a general rank separator, a complete Dean procedure, a polynomial practical bound for large unrestricted inputs, or a P-versus-NP conclusion. `P ?= NP` remains open. Stop at this one repair degree; any further carrier or generalization needs its own approval.
