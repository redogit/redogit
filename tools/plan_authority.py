#!/usr/bin/env python3
"""Offline planning-lineage projection and read-only action assessment.

No network, repository writes, command execution, admission, release or publication.
Input statements and permission labels remain caller declarations, not authenticated facts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

MAX_BYTES = 2 * 1024 * 1024
MAX_GRAPH_BYTES = 8 * MAX_BYTES
MAX_RECORDS = 128
PRIVACY = {'public', 'private', 'private-derived', 'unknown'}
OVERLAY_SCHEMA = 'rmal/plan-authority-overlay/v1'
GRAPH_SCHEMA = 'redogit/plan-lineage/v1'
SOURCE_KEYS = {'schema', 'date', 'predecessor', 'root_goal', 'global_rules',
               'shared_execution_stack', 'overrides', 'new_shared_machinery',
               'portfolio', 'retained_or_parked', 'priority_order_now'}
ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}\Z')
REVISION = re.compile(r'(?:[0-9a-f]{40}|[0-9a-f]{64})\Z')


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ValueError(code)


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for k, v in pairs:
        require(k not in result, 'DUPLICATE_JSON_KEY')
        result[k] = v
    return result


def _nonfinite(_: str) -> None:
    raise ValueError('NONFINITE_JSON_NUMBER')


def _check_depth(value: Any, depth: int = 0) -> None:
    require(depth <= 64, 'INPUT_NESTING_LIMIT')
    if isinstance(value, str):
        value.encode('utf-8', errors='strict')
    elif isinstance(value, dict):
        for k, v in value.items():
            _check_depth(k, depth + 1)
            _check_depth(v, depth + 1)
    elif isinstance(value, list):
        for v in value:
            _check_depth(v, depth + 1)


def load_json(raw: bytes, limit: int = MAX_BYTES) -> Any:
    require(type(raw) is bytes and len(raw) <= limit, 'INPUT_SIZE_OR_TYPE')
    try:
        value = json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs, parse_constant=_nonfinite)
        _check_depth(value)
        # A finite exponent such as 1e999 also overflows JSON's float representation.
        canonical(value)
        return value
    except (UnicodeError, json.JSONDecodeError, RecursionError, OverflowError) as exc:
        raise ValueError('INVALID_UTF8_JSON_OR_NESTING') from exc


def _strings(value: Any, code: str, *, nonempty: bool = True) -> None:
    require(isinstance(value, list) and len(value) <= 1024, code)
    require((not nonempty or bool(value)) and all(text(v) for v in value), code)


def _overlay(raw: bytes) -> dict[str, Any]:
    d = load_json(raw)
    require(isinstance(d, dict) and SOURCE_KEYS <= d.keys(), 'OVERLAY_FIELDS_MISSING')
    require(d['schema'] == OVERLAY_SCHEMA, 'UNSUPPORTED_OVERLAY_SCHEMA')
    require(text(d['date']) and text(d['root_goal']), 'OVERLAY_PURPOSE_REQUIRED')
    p = d['predecessor']
    require(isinstance(p, dict) and all(text(p.get(k)) for k in ('name', 'date', 'policy')), 'PREDECESSOR_DECLARATION_REQUIRED')
    require(isinstance(p.get('sha256'), str) and re.fullmatch('[0-9a-f]{64}', p['sha256']) is not None, 'PREDECESSOR_DIGEST_REQUIRED')
    for k in ('global_rules', 'shared_execution_stack', 'priority_order_now'):
        _strings(d[k], 'OVERLAY_ORDER_OR_RULES_INVALID')
    require(len(d['priority_order_now']) <= 64 and len(d['shared_execution_stack']) <= 64, 'ORDER_SIZE_LIMIT')
    for k in ('portfolio', 'retained_or_parked'):
        require(isinstance(d[k], list) and len(d[k]) <= MAX_RECORDS, 'PORTFOLIO_SIZE_OR_TYPE')
    require(bool(d['portfolio']), 'EMPTY_PORTFOLIO')
    for k in ('overrides', 'new_shared_machinery'):
        require(isinstance(d[k], dict) and len(d[k]) <= MAX_RECORDS, 'OVERLAY_MAP_SIZE_OR_TYPE')
        require(all(text(a) and isinstance(b, dict) for a, b in d[k].items()), 'OVERLAY_MAP_RECORD_INVALID')
    ids: set[str] = set()
    for item in d['portfolio']:
        require(isinstance(item, dict), 'PORTFOLIO_RECORD_INVALID')
        i = item.get('id')
        require(isinstance(i, str) and ID.fullmatch(i) is not None and i not in ids, 'PORTFOLIO_ID_INVALID_OR_DUPLICATE')
        ids.add(i)
        require(text(item.get('title')) and text(item.get('status')), 'PORTFOLIO_IDENTITY_REQUIRED')
        _strings(item.get('base_next'), 'BASE_OBLIGATIONS_REQUIRED')
        require(type(item.get('override_applied')) is bool, 'OVERRIDE_FLAG_NOT_BOOLEAN')
        require(item['override_applied'] == (i in d['overrides']), 'OVERRIDE_FLAG_MISMATCH')
    require(set(d['overrides']) <= ids, 'ORPHAN_OVERRIDE')
    names: set[str] = set()
    for item in d['retained_or_parked']:
        require(isinstance(item, dict) and all(text(item.get(k)) for k in ('name', 'status', 'rule')), 'RETAINED_RECORD_INVALID')
        require(item['name'] not in names, 'DUPLICATE_RETAINED_IDENTITY')
        names.add(item['name'])
    return d


def _escape(token: str) -> str:
    return token.replace('~', '~0').replace('/', '~1')


def resolve_pointer(value: Any, pointer: str) -> Any:
    require(isinstance(pointer, str) and (pointer == '' or pointer.startswith('/')), 'INVALID_SOURCE_POINTER')
    try:
        for token in pointer.split('/')[1:] if pointer else []:
            require(re.search(r'~(?![01])', token) is None, 'INVALID_POINTER_ESCAPE')
            token = token.replace('~1', '/').replace('~0', '~')
            if isinstance(value, list):
                require(re.fullmatch(r'0|[1-9][0-9]*', token) is not None, 'INVALID_POINTER_INDEX')
                value = value[int(token)]
            else:
                value = value[token]
        return value
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError('UNRESOLVED_SOURCE_POINTER') from exc


def compile_overlay(raw: bytes, *, privacy: str = 'private') -> dict[str, Any]:
    """Derive navigation only; retain the entire source verbatim for exact restoration."""
    require(isinstance(privacy, str) and privacy in PRIVACY, 'INVALID_PRIVACY_LABEL')
    d = _overlay(raw)
    nodes: list[dict[str, str]] = []
    edges: list[dict[str, str]] = []

    def node(i: str, pointer: str, kind: str, state: str) -> None:
        resolve_pointer(d, pointer)
        nodes.append({'id': i, 'pointer': pointer, 'kind': kind, 'state': state})

    def edge(a: str, b: str, relation: str) -> None:
        edges.append({'source': a, 'target': b, 'relation': relation})

    node('overlay', '', 'planning-source', 'current')
    node('predecessor', '/predecessor', 'unretrieved-predecessor-reference', 'historical')
    edge('overlay', 'predecessor', 'references_predecessor')
    for n, item in enumerate(d['portfolio']):
        i, ptr = item['id'], f'/portfolio/{n}'
        node(f'workstream:{i}', ptr, 'native-workstream-reference', 'coexisting')
        node(f'base-plan:{i}', ptr + '/base_next', 'base-planning-obligations',
             'historical' if item['override_applied'] else 'current')
        edge(f'workstream:{i}', f'base-plan:{i}', 'retains_base_plan')
        if item['override_applied']:
            node(f'base-priority:{i}', ptr + '/override_applied', 'base-only-priority', 'superseded')
            node(f'override:{i}', '/overrides/' + _escape(i), 'explicit-planning-overlay', 'current')
            edge(f'override:{i}', f'base-priority:{i}', 'supersedes_base_only_priority')
            edge(f'workstream:{i}', f'override:{i}', 'has_planning_overlay')
            edge(f'override:{i}', f'base-plan:{i}', 'preserves_predecessor_obligations')
    for i, name in enumerate(d['new_shared_machinery']):
        node(f'machinery:{i}', '/new_shared_machinery/' + _escape(name), 'machinery', 'coexisting')
        edge('overlay', f'machinery:{i}', 'references_without_authority_transfer')
    for i in range(len(d['retained_or_parked'])):
        node(f'retained:{i}', f'/retained_or_parked/{i}', 'retained-or-parked-lineage', 'retained')
        edge('overlay', f'retained:{i}', 'retains_without_reactivation')
    for i in range(len(d['shared_execution_stack'])):
        node(f'stage:{i}', f'/shared_execution_stack/{i}', 'declared-method-stage', 'coexisting')
        if i:
            edge(f'stage:{i-1}', f'stage:{i}', 'next_declared_stage_not_evidence_support')
    for i in range(len(d['priority_order_now'])):
        node(f'priority:{i+1}', f'/priority_order_now/{i}', 'declared-portfolio-priority', 'current')
        if i:
            edge(f'priority:{i}', f'priority:{i+1}', 'precedes_in_declared_plan')
    remainder = ['PREDECESSOR_BYTES_NOT_RETRIEVED', 'NATIVE_EVIDENCE_NOT_AUTHENTICATED',
                 'PLANNING_STATE_NOT_PROJECT_COMPLETION', 'NO_PUBLICATION_AUTHORITY']
    if set(d) - SOURCE_KEYS:
        remainder.append('UNINTERPRETED_SOURCE_FIELDS')
    return {
        'schema': GRAPH_SCHEMA,
        'source': {'schema': d['schema'], 'text': raw.decode('utf-8'),
                   'sha256': hashlib.sha256(raw).hexdigest(), 'privacy': privacy,
                   'authority': 'planning-only', 'externally_authenticated': False,
                   'predecessor_bytes_verified': False},
        'nodes': nodes, 'edges': edges, 'remainder': remainder}


def reconstruct(graph: dict[str, Any]) -> bytes:
    """Reject mismatched derived structures; return the unchanged original UTF-8 bytes."""
    require(isinstance(graph, dict) and graph.get('schema') == GRAPH_SCHEMA, 'UNSUPPORTED_GRAPH_SCHEMA')
    s = graph.get('source')
    require(isinstance(s, dict) and isinstance(s.get('text'), str), 'GRAPH_SOURCE_MISSING')
    try:
        raw = s['text'].encode('utf-8')
        expected = compile_overlay(raw, privacy=s.get('privacy'))
        require(canonical(graph) == canonical(expected), 'GRAPH_OR_SOURCE_TAMPERED')
        return raw
    except (UnicodeError, RecursionError) as exc:
        raise ValueError('INVALID_GRAPH_ENCODING') from exc


ACTION_KEYS = {'schema', 'id', 'node', 'priority', 'operation', 'expected_revision',
               'observed_revision', 'observed_state', 'permission', 'target_decision',
               'target_decision_ref', 'active_writer', 'privacy', 'bounded', 'reconstructible',
               'delta', 'dependencies', 'usefulness', 'expectation', 'observation',
               'counterprobe', 'way_back'}


def _validate_action(graph: dict[str, Any], a: dict[str, Any]) -> None:
    require(isinstance(a, dict) and set(a) == ACTION_KEYS, 'ACTION_FIELDS_INVALID')
    require(a['schema'] == 'redogit/action-proposal/v1', 'UNSUPPORTED_ACTION_SCHEMA')
    require(isinstance(a['id'], str) and ID.fullmatch(a['id']) is not None, 'ACTION_ID_INVALID')
    require(isinstance(a['node'], str) and a['node'] in {n['id'] for n in graph['nodes'] if n['kind'] == 'native-workstream-reference'}, 'ACTION_TARGET_NOT_NATIVE_WORKSTREAM')
    count = sum(n['kind'] == 'declared-portfolio-priority' for n in graph['nodes'])
    require(type(a['priority']) is int and 1 <= a['priority'] <= count, 'ACTION_PRIORITY_INVALID')
    for k, allowed in {
        'operation': {'inspect', 'repair', 'merge', 'release', 'publish'},
        'observed_state': {'unknown', 'open', 'merged', 'closed'},
        'permission': {'granted', 'denied', 'unknown'},
        'target_decision': {'accept', 'reject', 'pending'},
        'delta': {'zero', 'consequential', 'unknown'}, 'privacy': PRIVACY}.items():
        require(isinstance(a[k], str) and a[k] in allowed, 'ACTION_ENUM_INVALID')
    for k in ('expected_revision', 'observed_revision'):
        require(a[k] is None or (isinstance(a[k], str) and REVISION.fullmatch(a[k]) is not None), 'ACTION_REVISION_INVALID')
    for k in ('active_writer', 'bounded', 'reconstructible'):
        require(type(a[k]) is bool, 'ACTION_BOOLEAN_INVALID')
    for k in ('usefulness', 'expectation', 'observation', 'counterprobe', 'way_back'):
        require(text(a[k]), 'ACTION_MEANING_REQUIRED')
    require(a['target_decision_ref'] is None or text(a['target_decision_ref']), 'ACTION_DECISION_REFERENCE_INVALID')
    deps = a['dependencies']
    require(isinstance(deps, list) and len(deps) <= MAX_RECORDS, 'ACTION_DEPENDENCIES_INVALID')
    seen: set[str] = set()
    for dep in deps:
        require(isinstance(dep, dict) and set(dep) == {'id', 'satisfied'}, 'ACTION_DEPENDENCY_FIELDS_INVALID')
        require(text(dep['id']) and dep['id'] not in seen and type(dep['satisfied']) is bool, 'ACTION_DEPENDENCY_INVALID')
        seen.add(dep['id'])


def _assess(graph: dict[str, Any], a: dict[str, Any]) -> dict[str, Any]:
    _validate_action(graph, a)
    reject, defer, unchanged = [], [], []
    if a['permission'] == 'denied': reject.append('PERMISSION_DENIED')
    if a['target_decision'] == 'reject': reject.append('TARGET_REJECTED')
    if not a['bounded']: reject.append('UNBOUNDED_ACTION')
    if not a['reconstructible']: reject.append('RECOVERY_NOT_ESTABLISHED')
    if graph['source']['privacy'] != 'public' and a['privacy'] == 'public': reject.append('PRIVACY_DOWNGRADE')
    if a['privacy'] == 'unknown': defer.append('PRIVACY_UNRESOLVED')
    if a['permission'] == 'unknown': defer.append('PERMISSION_UNRESOLVED')
    if a['expected_revision'] is None or a['observed_revision'] is None:
        defer.append('REVISION_UNRESOLVED')
    elif a['expected_revision'] != a['observed_revision']:
        defer.append('REVISION_MOVED')
    if a['observed_state'] == 'unknown': defer.append('NATIVE_STATE_UNRESOLVED')
    if a['delta'] == 'unknown': defer.append('CONSEQUENTIAL_DELTA_UNRESOLVED')
    if a['delta'] == 'zero': unchanged.append('DELTA_ZERO')
    if a['observed_state'] == 'merged' and a['operation'] in {'repair', 'merge'}:
        unchanged.append('ALREADY_MERGED')
    if a['operation'] == 'repair':
        if a['target_decision'] != 'accept' or not a['target_decision_ref']:
            defer.append('TARGET_LOCAL_ACCEPTANCE_REQUIRED')
        if a['active_writer']: defer.append('ACTIVE_WRITER_CONFLICT')
        if a['observed_state'] == 'closed': defer.append('CLOSED_WORK_NOT_REACTIVATED')
    if any(not d['satisfied'] for d in a['dependencies']): defer.append('DEPENDENCY_UNRESOLVED')
    if a['operation'] in {'merge', 'release', 'publish'}:
        defer.append('SEPARATE_OPERATION_GATE_REQUIRED')
    # Stale observations cannot establish even a no-change decision.
    stale = any(r in defer for r in ('REVISION_UNRESOLVED', 'REVISION_MOVED', 'NATIVE_STATE_UNRESOLVED'))
    decision = 'reject' if reject else 'defer' if stale else 'no_change' if unchanged else 'defer' if defer else 'candidate'
    return {'id': a['id'], 'node': a['node'], 'priority': a['priority'], 'decision': decision,
            'reasons': reject + unchanged + defer,
            'executes': False, 'grants_authority': False, 'declarations_authenticated': False,
            'source_sha256': graph['source']['sha256'], 'proposal': json.loads(canonical(a))}


def assess_action(graph: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
    reconstruct(graph)
    return _assess(graph, action)


def select_next(graph: dict[str, Any], actions: list[dict[str, Any]]) -> dict[str, Any]:
    reconstruct(graph)
    require(isinstance(actions, list) and len(actions) <= MAX_RECORDS, 'ACTION_LIST_INVALID')
    results = [_assess(graph, a) for a in actions]
    require(len({r['id'] for r in results}) == len(results), 'DUPLICATE_ACTION_ID')
    results.sort(key=lambda r: (r['priority'], r['id']))
    return {'schema': 'redogit/action-assessment/v1',
            'selected': next((r['id'] for r in results if r['decision'] == 'candidate'), None),
            'assessments': results, 'executes': False, 'grants_authority': False,
            'priority_binding_authenticated': False}


def export_public(graph: dict[str, Any], *, approved: bool = False) -> dict[str, Any]:
    reconstruct(graph)
    require(type(approved) is bool and approved, 'PUBLIC_PROJECTION_APPROVAL_REQUIRED')
    require(graph['source']['privacy'] == 'public', 'NONPUBLIC_SOURCE_EXPORT_DENIED')
    # These labels are declarations. This function neither authenticates review nor publishes.
    return json.loads(canonical(graph))


def read_explicit(path: str, limit: int) -> bytes:
    p = Path(path).absolute()
    require(not any(q.is_symlink() for q in (p, *p.parents)), 'SYMLINK_INPUT_DENIED')
    with p.open('rb') as f:
        raw = f.read(limit + 1)
    require(len(raw) <= limit, 'INPUT_SIZE_LIMIT')
    return raw


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('graph', 'validate', 'restore', 'next', 'public'))
    parser.add_argument('input', help='One explicitly named overlay or graph JSON; no scanning.')
    parser.add_argument('--actions', help='Explicit action proposal array, required for next.')
    parser.add_argument('--privacy', choices=sorted(PRIVACY), default='private')
    parser.add_argument('--public-projection-approved', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'graph':
            result = compile_overlay(read_explicit(args.input, MAX_BYTES), privacy=args.privacy)
        else:
            graph = load_json(read_explicit(args.input, MAX_GRAPH_BYTES), MAX_GRAPH_BYTES)
            raw = reconstruct(graph)
            if args.command == 'restore':
                sys.stdout.buffer.write(raw)
                return 0
            if args.command == 'validate':
                result = {'valid': True, 'source_bytes': len(raw), 'nodes': len(graph['nodes']),
                          'edges': len(graph['edges']), 'authority': 'planning-only',
                          'externally_authenticated': False, 'remainder': graph['remainder']}
            elif args.command == 'next':
                require(args.actions is not None, 'ACTIONS_INPUT_REQUIRED')
                result = select_next(graph, load_json(read_explicit(args.actions, MAX_BYTES)))
            else:
                result = export_public(graph, approved=args.public_projection_approved)
        sys.stdout.buffer.write((json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8'))
        return 0
    except (OSError, ValueError, TypeError, RecursionError) as exc:
        # Never echo input contents, file paths, or third-party exception text.
        code = str(exc) if type(exc) is ValueError and re.fullmatch('[A-Z_]+', str(exc)) else 'INVALID_INPUT_OR_IO'
        print(f'PLAN_AUTHORITY_FAIL: {code}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
