# Dean's fixed list — a frozen LP wheel gap and its existing local repair

**Status:** approved Step 17 after the [fixed nine-vertex Step 16](PNP_DEAN_NINE_VERTEX_LOCAL_ROUNDING_2026-09-29.md). This counterprobe freezes all verified clique and odd-cycle rows and the exact seven- and nine-vertex positive-edge rows of Steps 15–16. It distinguishes a gap in their **unrounded linear relaxation** from an existing Step 14 local rational proof that already resolves the graph after integer rounding. No new carrier or general discovery rule is introduced. The Dean's graph and target are supplied and fixed.

## 1. One connected NO graph that the frozen rows leave open

Let \(W\) be the six-vertex odd wheel: rim \(0,1,2,3,4\) forms a \(C_5\), and hub \(h\) is adjacent to every rim vertex. Make five disjoint copies \(W_0,\ldots,W_4\), then add only the four hub-to-hub bridges \((W_i,h)(W_{i+1},h)\) for \(i=0,1,2,3\). There are \(n=30\) vertices and \(m=5(5+5)+4=54\) input edges. Each wheel selects at most two vertices: selecting the hub excludes its whole rim, while an independent set on the \(C_5\) rim has size two. Choosing rim labels 0 and 2 in every block avoids the bridges and attains \(\alpha(G)=10\), so the minimum omissions are \(\tau=20\). At the declared \(k=11,b=n-k=19\), the answer is **NO**.

Yet the complete frozen linear system admits \(x_h=1/5\) and \(x_i=2/5\) on each rim vertex in every wheel, or \(y_h=4/5\) and \(y_i=3/5\). Every clique row holds: a rim edge sums to \(4/5\), a hub triangle to one, and a clique crossing a hub bridge has at most two hubs. Every odd-cycle row holds: bridges occur in no cycle; within a wheel the triangles have selection sum one, the bare rim \(C_5\) sums to two, and a five-cycle using the hub and four rim vertices sums to \(9/5\le2\). Thus the fractional selection is \(5(1/5+5\cdot2/5)=11=k\), with fractional omissions \(19=b\).

No Step 15 or Step 16 row can be admitted in this graph, even under their permissive **required-positive-edges only** verifiers. Every vertex of \(\overline{C_7}\) needs four required neighbors among its occurrence, and every vertex of \(\overline{C_9}\) needs six. Each of the 25 rim vertices has ambient degree three, leaving only five hubs as possible mapped vertices: fewer than seven or nine distinct IDs. Equivalently, either required pattern is bridgeless and cannot span a bridge; one six-vertex wheel is too small. The exact-edge admission check therefore supplies zero rows of either kind, not an unrecorded cut.

The fractional optimum is exact. In each wheel, the rim \(C_5\) requires three omissions, and each of the five hub triangles requires two. Give the rim row weight \(3/5\) and each triangle weight \(1/5\). A rim vertex has load \(3/5+2/5=1\), and the hub load is \(5/5=1\); the overlap penalty is zero. The **already recorded Step 14** bound is \((3/5)3+5(1/5)2=19/5\) per wheel, hence \(B=19\) over five blocks, attained by the displayed fractional \(y\). Because that point satisfies **every** frozen row at \(b=19\), no nonnegative rational weighting of these rows can yield \(B>19\). This proves a gap in the globally unrounded LP certificate, not a failure of all prior local reasoning.

Indeed, omissions within each of the five vertex-disjoint wheels are integral. Its checked \(19/5\) bound therefore already implies at least \(\lceil19/5\rceil=4\) omissions **inside that wheel**. Sum the five local integer conclusions to obtain \(20>19\), a sound **NO** using only the existing Step 14 clique/cycle evidence. Rounding the global unrounded score \(19\) once would remain \(19\); rounding five local scores first retains the lost unit. This is a scoped composition of existing proofs, not an independently discovered wheel carrier or an asserted polynomial procedure for finding useful blocks.

The five-block count is necessary **within this symmetric construction at its first impossible target**, not globally minimal. With \(t\) such wheels and hub bridges, the integer maximum is \(2t\), so the target \(k=2t+1\) has budget \(4t-1\). The same old dual gives \(B=19t/5\), exceeding the budget by \(1-t/5\) for \(t<5\) and tying it at \(t=5\). No broader graph minimality or asymptotic barrier is inferred.

## 2. One-edge opposite and exact scope

Delete only rim edge \((W_0,4)(W_0,0)\), keeping every other vertex, edge, bridge, and the **same** \(k=11,b=19\). This turns the first rim into a five-vertex path. Its independent set \(\{0,2,4\}\) has size three; the other four wheels each still permit two. An explicit independent eleven-set is

\[
\{(W_0,0),(W_0,2),(W_0,4)\}
\cup\bigcup_{i=1}^{4}\{(W_i,1),(W_i,3)\}.
\]

It avoids every hub bridge. The per-block upper bounds are \(3+4(2)=11\), so the modified graph has \(n=30,m=53,\alpha=11,\tau=19\): **YES**. The Step 14 rim-\(C_5\) row is not admissible on the broken first rim; applying the five old local rounded conclusions would falsely say NO. Carrying that row forward without checking its input edge would lose source identity. The other four intact wheels still give their local bounds. The prior clique, odd-cycle, and exact seven-/nine-vertex verifiers stay sound; this step adds no proposed wheel inequality.

## 3. Cost, finite check, world relation, and remainder

The exact wheel construction and the five-block LP primal/dual are short rational proofs above. A disposable Python 3.12.14 probe enumerated all 64 local selections per wheel, checked the four bridges with a two-state dynamic program, verified the one-edge witness and degree obstruction, and printed `PASS exact Step 17 wheel counterprobe`. Command: `python3 step17_wheel_counterprobe.py`; script SHA-256 `f59a03dcc436a7f49d0b7741089b0a14118dd6ac6bdaa3ade62c8ea6c09b6ca5`. The probe checks this finite fixture; it does not establish a general runtime claim.

For a fixed pairwise conflict roster, five small scheduling groups can each have an integral capacity of two while their fractional relaxation offers \(11/5\). Across five groups the fractional excess becomes one whole requested place; checking and rounding each group's existing evidence preserves its real capacity. This is an analogy under the supplied pairwise edges, not a claim about changing schedules, weights, or real operations.

**Admitted:** this connected 30-vertex NO at \(k=11\), exact frozen-LP optimum 19, absence of both fixed rank carriers, a NO certificate obtained by local rounding of the *existing* Step 14 wheel evidence, and the one-edge YES at the same target. **Not admitted:** failure of all earlier reasoning on this graph, any new wheel carrier or discovery rule, a practical 400-vertex solver, a universal polynomial bound, or any result settling `P ?= NP`. The catalog remains frozen. A subsequent repair or generalization needs a separate approved step.
