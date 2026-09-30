#!/usr/bin/env python3
"""Steps 35-39: discovered articulation decomposition, exact singleton messages.

Unweighted finite simple graphs. One exceptional vertex PER ATOM in this
separate declared route; the earlier whole-graph cap-one solver is unchanged.
No brute force in the solver. Exhaustive truth is a bounded independent oracle.
"""
from __future__ import annotations
import copy
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import sys

BASE = Path(__file__).with_name('PNP_DEAN_PARITY_REPAIR_PROBE_2026-09-30.py')
spec = importlib.util.spec_from_file_location('parity_base', BASE)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
Graph, independent, truth = base.Graph, base.independent, base.truth


def components(g):
    unseen, answer = set(g.V), []
    while unseen:
        todo, seen = [min(unseen)], set()
        while todo:
            v = todo.pop()
            if v in seen:
                continue
            seen.add(v)
            todo.extend(g.adj[v]-seen)
        unseen -= seen
        answer.append(sorted(seen))
    return answer


def discover_tree(g):
    """Elementary charged discovery; no optimal-order or decomposition oracle."""
    bags, edges, cuts = [], [], 0
    def visit(h, attachment=None, parent=None):
        nonlocal cuts
        comps = components(h)
        if len(comps) > 1:
            assert parent is None
            node = len(bags); bags.append([])
            for c in comps:
                child = visit(h.induced(c))
                edges.append([node, child])
            return node
        for v in h.V:
            cuts += 1
            cs = components(h.induced(set(h.V)-{v}))
            if len(cs) > 1:
                node = len(bags); bags.append([v])
                for c in cs:
                    child = visit(h.induced(set(c)|{v}))
                    # Find a bag containing the separator. It need not be child root.
                    owned = reachable(child, edges)
                    target = next(i for i in sorted(owned) if v in bags[i])
                    edges.append([node, target])
                return node
        node = len(bags); bags.append(list(h.V))
        return node
    root = visit(g)
    return {'bags': bags, 'edges': edges, 'root': root, 'cut_tests': cuts}


def reachable(start, edges, allowed=None):
    adj = {}
    for u,v in edges:
        adj.setdefault(u,set()).add(v); adj.setdefault(v,set()).add(u)
    seen, todo = set(), [start]
    while todo:
        v = todo.pop()
        if v in seen or (allowed is not None and v not in allowed):
            continue
        seen.add(v); todo.extend(adj.get(v,set())-seen)
    return seen


def validate_tree(g, dec):
    bags, es, root = dec['bags'], dec['edges'], dec['root']
    t = len(bags)
    assert t >= 1 and type(root) is int and 0 <= root < t
    bs = [set(b) for b in bags]
    assert all(len(b)==len(s) and s <= set(g.V) for b,s in zip(bags,bs))
    assert set().union(*bs)==set(g.V)
    assert len(es)==t-1
    assert all(len(e)==2 and e[0]!=e[1] and all(type(v) is int and 0<=v<t for v in e) for e in es)
    assert len({tuple(sorted(e)) for e in es})==len(es)
    assert reachable(root,es)==set(range(t))
    assert all(len(bs[u]&bs[v])<=1 for u,v in es)
    assert all(any(u in b and v in b for b in bs) for u,v in g.E)
    for v in g.V:
        occ={i for i,b in enumerate(bs) if v in b}
        assert reachable(min(occ),es,occ)==occ
    adj={i:[] for i in range(t)}
    for u,v in es:
        adj[u].append(v); adj[v].append(u)
    parent={root:None}; order=[root]
    for i in order:
        for c in sorted(adj[i]):
            if c not in parent:
                parent[c]=i; order.append(c)
    children={i:[] for i in range(t)}
    sep={root:None}
    for i in order[1:]:
        p=parent[i]; children[p].append(i)
        s=bs[i]&bs[p]; sep[i]=next(iter(s)) if s else None
    return bs,order,children,sep


def local_problem(g,bag,children,sep,messages,i,state):
    b=bag[i]; s=sep[i]
    weights={v:int(v!=s) for v in b}; constant=0
    for c in children[i]:
        a=sep[c]
        if a is None:
            constant += messages[c]['free']['score']
        else:
            m0,m1=messages[c]['0']['score'],messages[c]['1']['score']
            assert m1 <= m0
            constant += m0; weights[a] += m1-m0
    assert all(type(w) is int and w<=1 for w in weights.values())
    chosen={s} if s is not None and state=='1' else set()
    blocked=set() if s is None else {s}
    if chosen:
        blocked |= g.adj[s]
    positive={v for v,w in weights.items() if w>0}-blocked
    assert all(weights[v]==1 for v in positive)
    return constant,weights,chosen,g.induced(positive)


def solve_tree(g,dec):
    bags,order,children,sep=validate_tree(g,dec)
    admission={}
    for i,b in enumerate(bags):
        a=base.discover_one(g.induced(b))
        if a['status']!='ADMITTED':
            return {'status':'UNKNOWN','reason':'atom outside local cap one','bag':i,'rejection':a}
        admission[i]=a['X']
    messages={}
    for i in reversed(order):
        messages[i]={}
        for state in (['free'] if sep[i] is None else ['0','1']):
            constant,w,forced,h=local_problem(g,bags,children,sep,messages,i,state)
            x=sorted(set(admission[i])&set(h.V))
            cert=base.solve_given_transversal(h,x,cap=1)
            assert cert['status']=='EXACT'
            chosen=forced|set(cert['witness'])
            witness=chosen-({sep[i]} if sep[i] is not None else set())
            for c in children[i]:
                key='free' if sep[c] is None else str(int(sep[c] in chosen))
                witness |= set(messages[c][key]['witness'])
            score=constant+sum(w[v] for v in forced)+cert['alpha']
            assert score==len(witness)
            messages[i][state]={'score':score,'witness':sorted(witness),'local_selected':sorted(chosen),'constant':constant,'weights':[[v,w[v]] for v in sorted(w)],'residual':h.identity(),'certificate':cert}
        if sep[i] is not None:
            assert messages[i]['1']['score']<=messages[i]['0']['score']
    root=dec['root']; top=messages[root]['free']
    answer={'status':'EXACT','context':g.identity(),'decomposition':dec,'local_cap':1,'transversals':[[i,admission[i]] for i in range(len(bags))],'messages':[[i,messages[i]] for i in range(len(bags))],'alpha':top['score'],'witness':top['witness']}
    verify(g,answer)
    return answer


def verify(g,answer):
    assert answer['status']=='EXACT' and answer['context']==g.identity() and answer['local_cap']==1
    dec=answer['decomposition']; bags,order,children,sep=validate_tree(g,dec)
    rows=answer['transversals']; mr=answer['messages']
    assert [r[0] for r in rows]==list(range(len(bags)))
    assert [r[0] for r in mr]==list(range(len(bags)))
    xs=dict(rows); messages=dict(mr)
    for i,b in enumerate(bags):
        assert len(xs[i])<=1 and len(xs[i])==len(set(xs[i])) and set(xs[i])<=b
        assert base.bipartition(g.induced(b-set(xs[i])))['bipartite']
    for i in reversed(order):
        states=['free'] if sep[i] is None else ['0','1']
        assert set(messages[i])==set(states)
        for state in states:
            constant,w,forced,h=local_problem(g,bags,children,sep,messages,i,state)
            m=messages[i][state]
            assert m['constant']==constant and m['weights']==[[v,w[v]] for v in sorted(w)]
            assert m['residual']==h.identity()
            base.verify_answer(h,m['certificate'],cap=1)
            assert m['certificate']['X']==sorted(set(xs[i])&set(h.V))
            chosen=forced|set(m['certificate']['witness'])
            assert m['local_selected']==sorted(chosen)
            expected=chosen-({sep[i]} if sep[i] is not None else set())
            for c in children[i]:
                key='free' if sep[c] is None else str(int(sep[c] in chosen))
                expected |= set(messages[c][key]['witness'])
            assert m['witness']==sorted(expected)
            assert m['score']==constant+sum(w[v] for v in forced)+m['certificate']['alpha']==len(expected)
            assert independent(g,sorted(expected|forced))
            if sep[i] is not None:
                assert sep[i] not in expected
        if sep[i] is not None:
            assert messages[i]['1']['score']<=messages[i]['0']['score']
    top=messages[dec['root']]['free']
    assert answer['alpha']==top['score'] and answer['witness']==top['witness']
    assert len(answer['witness'])==answer['alpha'] and independent(g,answer['witness'])


def solve(g):
    return solve_tree(g,discover_tree(g))


def glue(a,b):
    # Both pieces have a vertex zero. Only zero is shared; all IDs are retained.
    mp={0:0,**{v:len(a.V)+v-1 for v in b.V if v!=0}}
    return Graph(set(a.V)|{mp[v] for v in b.V},list(a.E)+[(mp[u],mp[v]) for u,v in b.E])


def fails(fn):
    try:
        fn()
    except (AssertionError,KeyError,ValueError,TypeError):
        return True
    return False


def brute_messages(g,answer):
    bags,order,children,sep=validate_tree(g,answer['decomposition'])
    messages=dict(answer['messages']); subs={}
    for i in reversed(order):
        subs[i]=set(bags[i])
        for c in children[i]: subs[i]|=subs[c]
        s=sep[i]
        for state,m in messages[i].items():
            allowed=subs[i]-({s} if s is not None else set())
            if state=='1': allowed-=g.adj[s]
            assert m['score']==truth(g.induced(allowed))[0]


def main(output):
    counts={'graphs_0_to_5':0,'admitted':0,'unknown':0,'shared_vertex_pairs':0,'pairs_admitted':0,'pairs_unknown':0,'root_order_checks':0,'message_checks':0}
    for n in range(6):
        for g in base.graphs(n):
            ans=solve(g); counts['graphs_0_to_5']+=1
            if ans['status']=='EXACT':
                counts['admitted']+=1
                assert ans['alpha']==truth(g)[0]
                brute_messages(g,ans); counts['message_checks']+=sum(len(m) for _,m in ans['messages'])
            else:
                counts['unknown']+=1
    pieces=[g for n in range(1,5) for g in base.graphs(n)]
    for a,b in product(pieces,repeat=2):
        g=glue(a,b); ans=solve(g); counts['shared_vertex_pairs']+=1
        if ans['status']=='EXACT':
            counts['pairs_admitted']+=1
            assert ans['alpha']==truth(g)[0]
            brute_messages(g,ans); counts['message_checks']+=sum(len(m) for _,m in ans['messages'])
            dec=copy.deepcopy(ans['decomposition']); dec['root']=len(dec['bags'])-1
            alt=solve_tree(g,dec)
            assert alt['alpha']==ans['alpha']; counts['root_order_checks']+=1
        else:
            counts['pairs_unknown']+=1
    # A star forces the signed boundary contribution: m0=2, m1=0, w(center)=-1.
    star=Graph([10,20,30],[(10,20),(10,30)])
    dec={'bags':[[10],[10,20],[10,30]],'edges':[[0,1],[0,2]],'root':0,'cut_tests':0}
    star_ans=solve_tree(star,dec)
    assert star_ans['alpha']==2
    assert dict(dict(star_ans['messages'])[0]['free']['weights'])[10]==-1
    # Nonmonotone/noninteger objective and wider separators are outside theorem.
    controls={}
    for label,edit in [
        ('missing_conditional_state',lambda a:dict(a['messages'])[1].pop('1')),
        ('inflated_root_score',lambda a:dict(a['messages'])[0]['free'].__setitem__('score',3)),
        ('wrong_boundary_weight',lambda a:dict(a['messages'])[0]['free'].__setitem__('weights',[[10,1]])),
        ('changed_shared_identity',lambda a:a['decomposition']['bags'][1].__setitem__(0,30)),
        ('duplicate_message',lambda a:a['messages'].append(a['messages'][0])),
    ]:
        damaged=copy.deepcopy(star_ans); edit(damaged)
        controls[label]=fails(lambda:verify(star,damaged)); assert controls[label]
    changed=Graph([10,20,30],[(10,20),(10,30),(20,30)])
    controls['stale_graph']=fails(lambda:verify(changed,star_ans)); assert controls['stale_graph']
    controls['missing_cross_edge']=fails(lambda:validate_tree(changed,dec)); assert controls['missing_cross_edge']
    wide={'bags':[[10,20],[10,20,30]],'edges':[[0,1]],'root':0}
    controls['separator_too_wide']=fails(lambda:validate_tree(star,wide)); assert controls['separator_too_wide']
    badrun={'bags':[[10],[20],[10]],'edges':[[0,1],[1,2]],'root':0}
    controls['running_intersection']=fails(lambda:validate_tree(Graph([10,20],[]),badrun)); assert controls['running_intersection']
    k4=Graph(range(4),list(combinations(range(4),2)))
    controls['k4_UNKNOWN']=solve(k4)['status']=='UNKNOWN'; assert controls['k4_UNKNOWN']
    chain=base.triangle_chain(12); chain_ans=solve(chain)
    assert chain_ans['alpha']==12 and base.discover_one(chain)['status']=='UNKNOWN'
    # Large atom family: disjoint K(p,p)+apex pieces, joined by apex bridges.
    t,p=10,12; edges=[]; bagsize=2*p+1
    for i in range(t):
        off=i*bagsize; apex=off+2*p
        edges += [(off+a,off+p+b) for a in range(p) for b in range(p)]
        edges += [(v,apex) for v in range(off,apex)]
        if i: edges.append((apex-bagsize,apex))
    large=Graph(range(t*bagsize),edges); la=solve(large)
    assert la['status']=='EXACT' and la['alpha']==t*p
    assert base.discover_one(large)['status']=='UNKNOWN'
    verify(large,json.loads(json.dumps(la)))
    result={'status':'PASS','base_commit':'3a6607a005d3376b2949b1e4ab3a43f37bf52a32','scope':'unweighted independent set; discovered articulation tree; local odd-cycle-transversal cap one','counts':counts,'counterprobes':controls,'negative_weight_star':star_ans,'triangle_chain':{'vertices':len(chain.V),'edges':len(chain.E),'alpha':chain_ans['alpha'],'minimum_global_transversal':12,'bags':len(chain_ans['decomposition']['bags'])},'large_family':{'pieces':t,'p':p,'vertices':len(large.V),'edges':len(large.E),'alpha':la['alpha'],'minimum_global_transversal':t,'bags':len(la['decomposition']['bags']),'cut_tests':la['decomposition']['cut_tests'],'certificate':la},'ceiling':'Scoped deterministic polynomial procedure and finite implementation checks; universal cover/local-cost/mass and P versus NP remain open.'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ['status','counts','counterprobes','triangle_chain']}))


if __name__=='__main__':
    main(sys.argv[1])
