#!/usr/bin/env python3
from fractions import Fraction
from itertools import product, combinations

def rank_q(M):
    A=[[Fraction(x) for x in row] for row in M]
    if not A: return 0
    r=0; m=len(A); n=len(A[0])
    for c in range(n):
        p=next((i for i in range(r,m) if A[i][c]),None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]
        pv=A[r][c]
        A[r]=[x/pv for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                f=A[i][c]
                A[i]=[A[i][j]-f*A[r][j] for j in range(n)]
        r+=1
    return r

def sat_clause(row, ass):
    return any(s*a==1 for s,a in zip(row,ass) if s)

def sat_formula(M, ass):
    return all(sat_clause(r,ass) for r in M)

def sat_count(M):
    return sum(sat_formula(M,a) for a in product((-1,1), repeat=len(M[0])))

def surplus(M):
    n=len(M[0]); best=None; witnesses=[]
    for k in range(1,n+1):
        for S in combinations(range(n),k):
            g=sum(any(row[j]!=0 for j in S) for row in M)
            val=g-k
            if best is None or val<best:
                best=val; witnesses=[S]
            elif val==best:
                witnesses.append(S)
    return best,witnesses

def project_xy(M3):
    out=[]
    for a in (-1,1):
        out.append(any(sat_formula(M3,(x,y,a))
                       for x,y in product((-1,1),repeat=2)))
    return tuple(out)

MA=((1,0,1),(0,1,0),(-1,-1,0),(0,0,-1))
MB=((1,0,1),(0,1,1),(-1,-1,-1),(0,0,-1))
AV=((1,0),(0,1),(-1,-1))
eA=(1,0,0)
eB=(1,1,-1)
z=(1,1,1)

assert tuple(eB[i]-eA[i] for i in range(3)) == tuple(r[1] for r in AV)
assert sum(eA[i]*z[i] for i in range(3)) == 1
assert sum(eB[i]*z[i] for i in range(3)) == 1
assert rank_q(MA)==rank_q(MB)==3
assert all(sum(MA[i][j] for i in range(4))==0 for j in range(3))
assert all(sum(MB[i][j] for i in range(4))==0 for j in range(3))
assert surplus(MA)[0]==surplus(MB)[0]==1
assert project_xy(MA[:3])==(False,True)  # a
assert project_xy(MB[:3])==(True,True)   # True
assert sat_count(MA)==0
assert sat_count(MB)==1

# Minimality below 3 parent variables.
# r=2 touched rows: exact rho is the boundary signed sum.
def project_one_x(signs,e):
    out=[]
    for a in (-1,1):
        out.append(any(
            all((sx*x==1) or (sa and sa*a==1)
                for sx,sa in zip(signs,e))
            for x in (-1,1)
        ))
    return tuple(out)

for signs in [(-1,1),(1,-1)]:
    groups={}
    for e in product((-1,0,1),repeat=2):
        if not any(e): continue
        groups.setdefault(sum(e),set()).add(project_one_x(signs,e))
    assert all(len(v)==1 for v in groups.values())

# n_parent=2,m_parent=4 tight r=3 case.
# Tightness forces boundary occurrence in >=2 touched clauses.
# WLOG internal signs (-,-,+).
groups={}
for e in product((-1,0,1),repeat=3):
    if sum(v!=0 for v in e)<2: continue
    rho_key=(e[0]+e[2],e[1]+e[2])
    groups.setdefault(rho_key,set()).add(project_one_x((-1,-1,1),e))
assert all(len(v)==1 for v in groups.values())

print("PASS")
print("interface_A =", project_xy(MA[:3]))
print("interface_B =", project_xy(MB[:3]))
print("sat_count_A =", sat_count(MA))
print("sat_count_B =", sat_count(MB))
print("surplus_A =", surplus(MA)[0])
print("surplus_B =", surplus(MB)[0])
