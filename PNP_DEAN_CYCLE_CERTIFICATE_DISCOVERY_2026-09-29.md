# Dean's fixed exclusion list — checking versus finding a cycle witness

**Status:** Step 12, bounded exact theorem about one named certificate search. The supplied edge list stays fixed. This is not a universal Dean solver or a proof that P differs from NP.

## 1. Input and the sound checker

The Dean supplies a simple undirected incompatibility graph \(G=(V,E)\) and a target \(k\). Set \(n=|V|\) and the omission budget \(b=n-k\). A valid selection is an independent \(k\)-set. The checker receives a separate proposed witness: a list \(\mathcal C=(C_1,\ldots,C_s)\) of pairwise vertex-disjoint, simple odd cycles made entirely from edges in the *given* \(E\). It never adds, deletes, or repairs a Dean edge.

Let
\[
W(\mathcal C)=\sum_{i=1}^s\frac{|C_i|+1}{2}.
\]
An independent set can retain at most \((|C_i|-1)/2\) vertices from each \(C_i\); the vertices outside the cycles might all be retained. Hence
\[
\alpha(G)\le n-W(\mathcal C),\qquad
W(\mathcal C)>b\ \Longrightarrow\ \alpha(G)<k.
\]
Additional edges between cycles or outside them only strengthen this upper bound. For a partial cycle list, do **not** replace the displayed bound by \(\alpha\le(n-s)/2\). A connected \(C_5\) with one pendant leaf has \(n=6\), one displayed odd cycle, and \(\alpha=3>(6-1)/2\).

The older GYRO/DEAN §17 formula \(\alpha\le(n-c)/2\) uses a **spanning fractional-perfect-matching support frame**: disjoint weight-1 edges and weight-1/2 odd cycles cover *every* vertex, with \(c\) odd cycles. Its frame accounts for the vertices outside any listed odd cycles by explicit edges. For a spanning list of odd cycles alone, our formula reduces to \(\alpha\le(n-s)/2\). The old theorem must retain its spanning hypothesis.

A deterministic checker canonicalizes the \(m\) input edges, checks that every listed cycle has odd length at least three, distinct vertices, no vertex shared with another cycle, and each consecutive edge (including the closing edge) occurs in \(E\). It then computes \(W\) and tests \(W>b\). A list uses at most \(n\) vertex occurrences. Sorting and edge lookups take \(O((n+m)\log(n+m))\) word comparisons and \(O(n+m)\) memory; for \(O(\log n)\)-bit vertex labels, a conservative bit bound is \(O((n+m)\log(n+m)\log(n+1))\). The witness itself has \(O(n\log n)\) bits.

**Verify** means checking a supplied list. It says nothing yet about finding the list.

## 2. On the declared \(H_t\), discovery is cheap

[Step 11](PNP_DEAN_FIXED_LIST_C5_CHAIN_2026-09-29.md) declared \(t\) five-cycles joined in a path by bridges. They span \(n=5t\), so displaying the cycles yields \(W=3t\). At the separately declared target \(k=2t+1\), \(b=3t-1\), and the list proves NO.

For this explicitly structured family, a bridge search, removal of the bridges, a check that each remaining component is a five-cycle and that the bridge quotient is a path, and a walk around each cycle construct the witness in \(O(n+m)\) graph operations. This recognizes the stated shape even if vertex labels are permuted. Verification is also polynomial. The family's ease is a measured special-case fact, not a bound for arbitrary \(E\).

There is a choice *within the same input*. If \(t\) is even, take every other bridge in \(H_t\), match the four remaining vertices within each paired five-cycle, and obtain a perfect matching. Its weight-1 edges are a valid spanning fractional frame with \(c=0\), giving only \(\alpha\le n/2=5t/2\). At \(k=2t+1\) this does **not** prove NO. The all-cycle weight-1/2 frame has \(c=t\), giving \(\alpha\le(n-t)/2=2t\), which **does** prove NO. Finding *a* valid frame and selecting a **decisive** one are different obligations.

A direct YES/NO counterpair also survives the cheaper summaries. \(H_2\) has \(n=10,m=11\), degrees \(3,3,2,\ldots,2\), matching number \(5\), and \(\alpha=4\). Form a second graph with top and bottom paths of five vertices each, plus rungs in columns \(1,3,5\). It has the same \(n,m\), degree multiset and matching number, but it is bipartite and has \(\alpha=5\). At \(k=5\), both the degree-omission and matching-omission checks are silent; the first input is NO and the second YES. This pair shows those summaries lose a consequential distinction. It does not show that the two instances are hard to distinguish: a bipartiteness check already separates them.

## 3. The exact discovery decision on arbitrary fixed lists

Define **CYCLE-WITNESS**: given the Dean's fixed \(G\) and \(b\), does there exist a vertex-disjoint odd-cycle list \(\mathcal C\) with \(W(\mathcal C)>b\)? Section 1 places this decision problem in NP.

It is NP-hard by a direct reduction from **Partition Into Triangles**, which is NP-complete even for graphs of maximum degree four [van Rooij, van Kooten Niekerk, and Bodlaender, Theorem 10](https://doi.org/10.1007/s00224-012-9412-5). Given a triangle-partition input with \(n=3q\), keep its graph exactly as supplied and choose \(b=2q-1\) (equivalently, Dean target \(k=q+1\)). For every odd cycle length \(\ell\ge3\),
\[
\frac{\ell+1}{2}\le\frac{2\ell}{3},
\]
with equality only for \(\ell=3\). The cycles are disjoint, so \(W\le 2n/3=2q\). Because \(W\) is an integer, \(W>b\) holds exactly when \(W=2q\); equality forces the cycles to cover every vertex and each cycle to be a triangle. Thus a decisive list exists **if and only if** the source graph has a triangle partition. The map changes the target between separately declared instances; it never edits a received edge list during solving. Membership plus hardness proves CYCLE-WITNESS is NP-complete, already at maximum degree four.

This is a statement about *this certificate-search decision*. It does not prove an exponential lower bound, a P-versus-NP separation, or that every Dean NO instance needs this certificate. If a polynomial algorithm decided this search on all inputs, it would solve the cited NP-complete source problem and hence imply P=NP.

## 4. Completeness guard and research lineage

The cycle rule cannot certify every NO. Join \(t\ge2\) disjoint copies of \(K_4\) in a path with bridges, using different bridge endpoints in each internal copy. Here \(n=4t\), \(\alpha=t\), matching number \(2t\), and maximum degree \(4\). At target \(k=2t\), \(b=2t\), so the true answer is NO. The degree and matching checks stop at the budget. No odd cycle crosses a bridge; each \(K_4\) contains at most one vertex-disjoint odd cycle, a triangle worth two omissions. Thus every cycle list has \(W\le2t=b\). A clique-component argument proves NO for this explicit family, but that is another certificate rule with its own discovery cost.

The earlier DEAN support-frame proof supplied the spanning hypothesis. The earlier C5 boundary-transfer CSV supplied a related \(n=5t,\alpha=2t\) progression but retained no generator or bridge endpoints, so \(H_t\) remains an independently declared analogous family. The user's LEARNED_LEDGER, ALL_PATHS_FRONTIER, and RELATIONAL_PATHING carrier-work/span notes already distinguished a short final carrier from its construction, recognition, selection, recovery and total work. This step makes that distinction an exact verifier, a cheap special-case finder, a hard general certificate-search decision, and an explicit completeness limit.

**Claim ceiling:** a supplied sound cycle list is cheaply checkable; \(H_t\)'s list is cheaply discoverable; deciding whether an arbitrary fixed list admits a decisive cycle list is NP-complete; the cycle rule is incomplete for Dean NO. No universal deterministic polynomial-time solver or proof of P=NP has been supplied.
