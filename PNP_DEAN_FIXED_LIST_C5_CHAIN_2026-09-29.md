# Dean's given exclusion list — connected five-cycle progression

**Status:** bounded exact result for an explicit graph family. The universal deterministic polynomial-time algorithm required for $P=NP$ remains open.

## The fixed obligation

For each test input, the Dean supplies candidates $X$, an exclusion list $E$, and a required count $k$. The list is read as given. A valid output is one set $G\subseteq X$ with $|G|=k$ and no listed pair wholly in $G$. Deriving an omitted set $D=X\setminus G$ or looking at the pairs still relevant to $X\setminus D$ does not edit $E$. Different test inputs below are declared separately; no solver rewrites a received list.

Let $\alpha$ be the largest valid selection, $\tau=|X|-\alpha$ the minimum omissions needed to break all listed pairs, and $\nu$ the maximum number of pairwise disjoint listed pairs. A matching gives the sound lower bound $\nu\le\tau$, but equality is not guaranteed on general graphs. Maximum matching can be computed in polynomial time [Edmonds, *Paths, Trees, and Flowers* (1965)](https://doi.org/10.4153/CJM-1965-045-4).

## One explicit connected input family

For each $t\ge1$, give cycle $i$ five distinct candidates $v_{i,0},\ldots,v_{i,4}$. Its listed pairs are $\{v_{i,j},v_{i,(j+1)\bmod 5}\}$ for $j=0,\ldots,4$. For $i=1,\ldots,t-1$, also list exactly one bridge pair $\{v_{i,2},v_{i+1,0}\}$. Call this fixed list $E_t$. It has $5t$ candidates, $6t-1$ pairs, is connected, and has maximum degree at most three.

The exact bounds follow without a search experiment:

1. Each five-cycle contains at most two mutually compatible candidates. Selecting $v_{i,1}$ and $v_{i,3}$ in every cycle avoids every cycle pair and every bridge. Hence $\alpha(E_t)=2t$ and $\tau(E_t)=3t$.
2. Pair cycles $1$ and $2$, $3$ and $4$, and so on. For each pair, use its bridge and two disjoint internal pairs from the remaining four vertices of each cycle. This gives five disjoint pairs per paired block. If $t$ is odd, take two internal pairs from the remaining cycle. Since no matching can use more than half the vertices, $\nu(E_t)=\lfloor5t/2\rfloor$.
3. Therefore $\tau-\nu=\lceil t/2\rceil$. The **additive** gap grows; the ratio does not grow without bound.

| Cycles $t$ | Candidates | $\alpha$ | $\tau$ | $\nu$ | $\tau-\nu$ |
|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 2 | 3 | 2 | 1 |
| 2 | 10 | 4 | 6 | 5 | 1 |
| 3 | 15 | 6 | 9 | 7 | 2 |
| 4 | 20 | 8 | 12 | 10 | 2 |
| 5 | 25 | 10 | 15 | 12 | 3 |
| $t$ | $5t$ | $2t$ | $3t$ | $\lfloor5t/2\rfloor$ | $\lceil t/2\rceil$ |

## Two declared requirements, different test outcomes

- **Keep the earlier requirement $k=3t$:** The omission budget is $b=2t$. For every $t\ge2$, $\nu> b$, so the disjoint-pair rule already proves $\mathrm{NO}$. The connected bridge makes this rule stronger here. We do not claim it remains inconclusive.
- **Use the first impossible requirement $k=2t+1$:** Now $b=3t-1$. The degree rule is silent (degree at most three, with the $t=1$ boundary degree two and budget two), and $\nu\le b$, so maximum matching is inconclusive. Still $\tau=3t>b$, and the vertex-disjoint five-cycles prove $\mathrm{NO}$. The distance between the true omission count and this budget is one; the distance from the matching lower bound is $\lceil t/2\rceil$.

The two requirements are different inputs. The exclusion list stays unchanged *within* each input. A checkable $\mathrm{NO}$ receipt for this explicit family consists of the $t$ vertex-disjoint five-cycles spanning $X$: any valid selection takes at most two from each, so $k=2t+1$ is impossible. Checking the listed cycles and the count costs polynomial work. No polynomial procedure to discover a comparably decisive carrier on **every arbitrary** given $E$ has been proved here.

## Relation to earlier work and cost

The earlier DEAN support-frame argument already bounded an independent set by $(n-c)/2$ when a certified frame contains $c$ disjoint odd cycles. Here $n=5t$ and $c=t$, giving $2t$; the explicit selection proves tightness even across the bridge pairs. That earlier analysis warned that cross-component exclusions must be kept as compatibility constraints. The bridges are precisely such cross constraints, and the witness above checks them.

A September 11 connected-five-cycle boundary-transfer table recorded the same $n=5t$, $\alpha=2t$, and first impossible $k=2t+1$ for $t=1,\ldots,8$. Its retained table does not specify bridge endpoints or the generator/seed. The explicit $E_t$ here is a freshly specified mathematical model, **not** a claimed byte-identical reconstruction or rerun of those historical operation counts. An earlier semantic-repair record likewise kept old C5 measurements historical when their generator/seed could not be recovered.

For this declared family, constructing and checking the graph, the exhibited selection, matching witness, and cycle-based $\mathrm{NO}$ argument take $O(t)$ graph operations (or $O(t\log t)$ bit work with ordinary indexed vertex labels). This cost bound is for the explicit family and witnesses. For arbitrary $E$, discovery, construction, branch choice, verification, output, trace, and Homeward reconstruction all count. A compact final representation is not evidence that it was cheap to find.

`GENERATE != VERIFY != ADMIT`. The exact family proof is admitted at its declared scope. The universal clean-selection/NO procedure and one fixed worst-case polynomial total bound remain **UNRESOLVED**.
