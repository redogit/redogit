// Exact finite checks for Dean Steps 26-29. No dependencies.
function runDeanComponentProbe() {
  "use strict";
  let assertions=0;
  function check(ok, message) { assertions++; if(!ok) throw new Error(message); }
  function pop(x){let n=0;while(x){x&=x-1;n++;}return n;}
  function graph(n,edges) {
    if(!Number.isInteger(n)||n<0)throw Error("invalid size");
    const seen=new Set(), es=[];
    for(const [a,b] of edges) {
      if(!Number.isInteger(a)||!Number.isInteger(b)||a<0||b<0||a>=n||b>=n||a===b)throw Error("invalid edge");
      const u=Math.min(a,b),v=Math.max(a,b),k=u+","+v;
      if(seen.has(k))throw Error("duplicate edge");
      seen.add(k);es.push([u,v]);
    }
    es.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
    const adj=Array.from({length:n},()=>new Set());
    for(const [u,v] of es){adj[u].add(v);adj[v].add(u);}
    return {n,edges:es,adj};
  }
  function independent(g,ids){const set=new Set(ids);return set.size===ids.length&&ids.every(v=>Number.isInteger(v)&&v>=0&&v<g.n)&&g.edges.every(([u,v])=>!set.has(u)||!set.has(v));}
  function brute(g,allowed=null) {
    const ids=allowed===null?Array.from({length:g.n},(_,i)=>i):allowed;
    if(ids.length>18)throw Error("finite oracle cap exceeded");
    let alpha=-1,witness=[],count=0;
    for(let mask=0;mask<2**ids.length;mask++) {
      const chosen=ids.filter((_,i)=>mask&(1<<i));
      if(independent(g,chosen)){count++;if(chosen.length>alpha){alpha=chosen.length;witness=chosen;}}
    }
    return {alpha,witness,independentSets:count,subsets:2**ids.length};
  }
  function context(g,S){return JSON.stringify({n:g.n,edges:g.edges,S});}
  function build(g,boundary) {
    const S=[...boundary].sort((a,b)=>a-b);
    if(new Set(S).size!==S.length||S.some(x=>!Number.isInteger(x)||x<0||x>=g.n))throw Error("invalid boundary");
    const bs=new Set(S),unseen=new Set(Array.from({length:g.n},(_,i)=>i).filter(x=>!bs.has(x))),components=[];
    while(unseen.size) {
      const first=unseen.values().next().value,q=[first];unseen.delete(first);
      for(let i=0;i<q.length;i++)for(const v of g.adj[q[i]])if(unseen.has(v)){unseen.delete(v);q.push(v);}
      q.sort((a,b)=>a-b);
      if(q.length>3)return {status:"UNKNOWN",reason:"private component exceeds three"};
      components.push(q);
    }
    const factors=components.map(C=>{
      const options=[];
      for(let mask=0;mask<2**C.length;mask++){
        const I=C.filter((_,i)=>mask&(1<<i));if(!independent(g,I))continue;
        const N=[...new Set(I.flatMap(v=>[...g.adj[v]].filter(w=>bs.has(w))))].sort((a,b)=>a-b);
        options.push({I,score:I.length,N});
      }
      return {C,options};
    });
    return {status:"ADMITTED",S,context:context(g,S),factors};
  }
  function evaluate(expr,sigma,g) {
    if(expr.status!=="ADMITTED")throw Error("unadmitted expression");
    if(expr.context!==context(g,expr.S))throw Error("stale source graph");
    if(!independent(g,sigma)||sigma.some(v=>!expr.S.includes(v)))throw Error("invalid boundary state");
    const selected=new Set(sigma),extension=[];
    for(const factor of expr.factors){
      let winner=null;
      for(const opt of factor.options)if(opt.N.every(v=>!selected.has(v))&&(!winner||opt.score>winner.score))winner=opt;
      if(!winner)throw Error("missing empty option");
      extension.push(...winner.I);
    }
    const witness=[...sigma,...extension].sort((a,b)=>a-b);
    return {value:extension.length,total:witness.length,witness};
  }
  function sourceGraphs(n) {
    const pairs=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)pairs.push([u,v]);
    return Array.from({length:2**pairs.length},(_,mask)=>graph(n,pairs.filter((_,i)=>mask&(1<<i))));
  }
  function encode(H) {
    const edges=[],components=[];
    H.edges.forEach(([u,v],i)=>{const a=H.n+2*i,b=a+1;edges.push([u,a],[a,b],[b,v]);components.push({edge:[u,v],a,b});});
    return {g:graph(H.n+2*H.edges.length,edges),S:Array.from({length:H.n},(_,i)=>i),components};
  }
  let allSmallGraphs=0,partitions=0,admitted=0,rejected=0,states=0;
  for(let n=0;n<=4;n++)for(const g of sourceGraphs(n)){
    allSmallGraphs++;
    for(let sm=0;sm<2**n;sm++){
      partitions++;
      const S=Array.from({length:n},(_,i)=>i).filter(i=>sm&(1<<i)),expr=build(g,S);
      if(expr.status!=="ADMITTED"){rejected++;continue;}admitted++;
      let best=-1;
      for(let sig=0;sig<2**S.length;sig++){
        const sigma=S.filter((_,i)=>sig&(1<<i));
        if(!independent(g,sigma)){
          let rejectedState=false;try{evaluate(expr,sigma,g);}catch{rejectedState=true;}
          check(rejectedState,"invalid state accepted");continue;
        }
        states++;
        const permitted=Array.from({length:n},(_,i)=>i).filter(v=>!S.includes(v)&&sigma.every(s=>!g.adj[s].has(v)));
        const expected=brute(g,permitted).alpha,actual=evaluate(expr,sigma,g);
        check(actual.value===expected,"component extension mismatch");
        check(independent(g,actual.witness)&&actual.total===sigma.length+expected,"component witness mismatch");
        best=Math.max(best,actual.total);
      }
      check(best===brute(g).alpha,"composed optimum mismatch");
    }
  }
  let reductions=0,transformedSubsets=0,reductionStates=0;
  for(let n=0;n<=4;n++)for(const H of sourceGraphs(n)){
    const {g,S}=encode(H),expr=build(g,S),base=brute(H),truth=brute(g);
    check(expr.status==="ADMITTED","reduction not admitted");
    check(truth.alpha===H.edges.length+base.alpha,"reduction identity");
    transformedSubsets+=truth.subsets;reductions++;
    for(let mask=0;mask<2**n;mask++){
      const sigma=S.filter(v=>mask&(1<<v)),inside=H.edges.filter(([u,v])=>(mask&(1<<u))&&(mask&(1<<v))).length;
      const actual=evaluate(expr,sigma,g);
      check(actual.value===H.edges.length-inside,"factor penalty identity");
      check(independent(g,actual.witness),"reduction extension witness");
      const repaired=new Set(sigma);
      for(const [u,v] of H.edges)if(repaired.has(u)&&repaired.has(v))repaired.delete(v);
      check(independent(H,[...repaired])&&repaired.size>=sigma.length-inside,"source witness recovery");
      reductionStates++;
    }
  }
  function bipartiteSolve(g,S) {
    const bs=new Set(S),U=Array.from({length:g.n},(_,i)=>i).filter(v=>!bs.has(v));
    if(S.length!==bs.size||S.some(v=>!Number.isInteger(v)||v<0||v>=g.n))throw Error("invalid bipartition");
    if(g.edges.some(([u,v])=>bs.has(u)===bs.has(v)))return {status:"UNKNOWN",reason:"edge within a side"};
    const rightMatch=new Map();
    function augment(u,seen){
      for(const v of g.adj[u]){
        if(seen.has(v))continue;seen.add(v);
        if(!rightMatch.has(v)||augment(rightMatch.get(v),seen)){rightMatch.set(v,u);return true;}
      }
      return false;
    }
    for(const u of S)augment(u,new Set());
    const leftMatch=new Map([...rightMatch].map(([v,u])=>[u,v]));
    const ZS=new Set(S.filter(u=>!leftMatch.has(u))),ZU=new Set(),q=[...ZS];
    for(let i=0;i<q.length;i++){
      const u=q[i];
      for(const v of g.adj[u]){
        if(leftMatch.get(u)===v||ZU.has(v))continue;
        ZU.add(v);
        if(rightMatch.has(v)&&!ZS.has(rightMatch.get(v))){ZS.add(rightMatch.get(v));q.push(rightMatch.get(v));}
      }
    }
    const cover=[...S.filter(u=>!ZS.has(u)),...U.filter(v=>ZU.has(v))].sort((a,b)=>a-b);
    const cs=new Set(cover),witness=Array.from({length:g.n},(_,i)=>i).filter(v=>!cs.has(v));
    const matching=[...rightMatch].map(([v,u])=>[u,v]).sort((a,b)=>a[0]-b[0]);
    return {status:"ADMITTED",alpha:witness.length,matching,cover,witness};
  }
  let bipartiteGraphs=0,bipartiteSubsets=0;
  for(const [p,q] of [[0,0],[0,3],[3,0],[1,1],[2,2],[3,3]]){
    const pairs=[];for(let u=0;u<p;u++)for(let v=p;v<p+q;v++)pairs.push([u,v]);
    for(let mask=0;mask<2**pairs.length;mask++){
      const g=graph(p+q,pairs.filter((_,i)=>mask&(1<<i))),S=Array.from({length:p},(_,i)=>i);
      const solved=bipartiteSolve(g,S),truth=brute(g),cs=new Set(solved.cover);
      check(solved.alpha===truth.alpha,"matching alpha mismatch");
      check(independent(g,solved.witness),"matching witness mismatch");
      check(g.edges.every(([u,v])=>cs.has(u)||cs.has(v)),"not a vertex cover");
      check(solved.cover.length===solved.matching.length,"cover matching mismatch");
      const endpoints=solved.matching.flat();
      check(new Set(endpoints).size===endpoints.length&&solved.matching.every(([u,v])=>g.adj[u].has(v)),"invalid matching");
      bipartiteGraphs++;bipartiteSubsets+=truth.subsets;
    }
  }
  check(bipartiteSolve(graph(3,[[0,1],[1,2],[0,2]]),[0]).status==="UNKNOWN","nonbipartite admitted");
  check(build(graph(4,[[0,1],[1,2],[2,3]]),[]).status==="UNKNOWN","overcap component admitted");
  const triangle=graph(3,[[0,1],[0,2],[1,2]]),enc=encode(triangle),before=build(enc.g,enc.S);
  const removed=[0,3],changed=graph(enc.g.n,enc.g.edges.filter(([u,v])=>u!==removed[0]||v!==removed[1]));
  const after=build(changed,enc.S),b=brute(enc.g),a=brute(changed),sigma=[0,1],ev=evaluate(after,sigma,changed);
  check(b.alpha===4&&a.alpha===5&&ev.total===5&&independent(changed,ev.witness),"one-edge decision flip");
  let staleRejected=false;try{evaluate(before,sigma,changed);}catch(e){staleRejected=e.message==="stale source graph";}
  check(staleRejected,"stale expression accepted");
  const changedFactors=before.factors.map((f,i)=>JSON.stringify(f)!==JSON.stringify(after.factors[i])).filter(Boolean).length;
  check(changedFactors===1,"repair changed multiple factors");
  check(JSON.stringify(before.factors.map(f=>f.C))===JSON.stringify(after.factors.map(f=>f.C)),"component IDs changed");
  const control=graph(9,[[0,1],[0,3],[1,4],[3,4],[4,5],[2,6],[2,7],[6,7],[7,8]]);
  const controlExpr=build(control,[0,1,2]);
  check(controlExpr.status==="ADMITTED"&&controlExpr.factors.every(f=>f.C.length===3),"three-vertex control");
  for(const sigma of [[],[0],[1],[2],[0,2],[1,2]]){
    const remaining=Array.from({length:9},(_,i)=>i).filter(v=>![0,1,2].includes(v)&&sigma.every(s=>!control.adj[s].has(v)));
    check(evaluate(controlExpr,sigma,control).value===brute(control,remaining).alpha,"three-vertex extension");
  }
  return {
    schema:"dean-component-expression-finite-result-v1",status:"PASS",arithmetic:"exact small integers; no random sampling",
    assertions,
    componentExpression:{sourceGraphs:allSmallGraphs,partitions,admitted,rejected,feasibleStatesChecked:states,maxSourceVertices:4,privateComponentCap:3,additionalThreeVertexComponentStates:6},
    reduction:{sourceGraphs:reductions,maxSourceVertices:4,maxTransformedVertices:16,transformedSubsetsChecked:transformedSubsets,boundaryStatesChecked:reductionStates},
    bipartite:{graphs:bipartiteGraphs,subsetsChecked:bipartiteSubsets,dimensions:[[0,0],[0,3],[3,0],[1,1],[2,2],[3,3]],algorithm:"one augmenting-path search per left vertex; alternating-reachability cover"},
    oneEdgeRepair:{n:9,beforeEdges:9,afterEdges:8,removedEdge:removed,target:5,omissionBudget:4,beforeAlpha:b.alpha,afterAlpha:a.alpha,witness:ev.witness,changedFactors,unchangedFactors:2,staleExpressionRejected:staleRejected},
    claimCeiling:"Finite exact corroboration only. Symbolic proofs are separate. No unrestricted polynomial independent-set solver or P-versus-NP resolution."
  };
}

const result = runDeanComponentProbe();
console.log(JSON.stringify(result, null, 2));
