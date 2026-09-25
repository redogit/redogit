"""Synthetic regression controls. No user or repository data are embedded."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'tools' / 'plan_authority.py'


def overlay():
    return {
        'schema': 'rmal/plan-authority-overlay/v1', 'date': '2026-09-20',
        'predecessor': {'name': 'PREVIOUS.json', 'date': '2026-09-19',
                        'sha256': 'a' * 64, 'policy': 'PRESERVE_PREDECESSOR; APPLY_ONLY_EXPLICIT_OVERRIDES'},
        'root_goal': 'Help someone recover a plan without turning it into evidence.',
        'global_rules': ['PLAN != SOLUTION', 'UNKNOWN != ABSENT'],
        'shared_execution_stack': ['SUBJECT', 'CHECK', 'REMAINDER'],
        'overrides': {'sample': {'current_addendum': 'Reported failed probe stays reported.',
                                  'next_priority': ['Read exact native evidence first.']}},
        'new_shared_machinery': {'VIEW': {'status': 'ACTIVE_SUPPORT', 'next': 'Preserve roles.'}},
        'portfolio': [
            {'id': 'authority', 'title': 'Authority map', 'status': 'ACTIVE_CORE',
             'base_next': ['Build the local map.'], 'override_applied': False},
            {'id': 'sample', 'title': 'Sample lab', 'status': 'ACTIVE_RESEARCH',
             'base_next': ['Earlier bounded probe.'], 'override_applied': True}],
        'retained_or_parked': [{'name': 'Retained lab', 'status': 'RETAINED_LINEAGE',
                               'rule': 'No reactivation by inventory.'}],
        'priority_order_now': ['1. Preserve authority.', '2. Read sample evidence.']}


def source_bytes(value=None):
    return (json.dumps(overlay() if value is None else value, ensure_ascii=False, indent=2) + '\n').encode()


def action(**changes):
    a = {'schema': 'redogit/action-proposal/v1', 'id': 'probe', 'node': 'workstream:sample',
         'priority': 2, 'operation': 'inspect', 'expected_revision': 'a' * 40,
         'observed_revision': 'a' * 40, 'observed_state': 'open', 'permission': 'granted',
         'target_decision': 'pending', 'target_decision_ref': None, 'active_writer': False,
         'privacy': 'private', 'bounded': True, 'reconstructible': True, 'delta': 'consequential',
         'dependencies': [], 'usefulness': 'Avoid repeating an already settled probe.',
         'expectation': 'An exact receipt exists.', 'observation': 'Receipt not yet inspected.',
         'counterprobe': 'Compare the native revision and its receipt.',
         'way_back': 'Input is immutable; discard this assessment.'}
    a.update(changes)
    return a


class ModuleCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if MODULE.exists():
            spec = importlib.util.spec_from_file_location('plan_authority', MODULE)
            cls.api = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.api)
        else:
            cls.api = None

    def setUp(self):
        self.assertIsNotNone(self.api, 'The approved authority/lineage executable is missing')


class GraphTests(ModuleCase):
    def test_exact_bytes_round_trip_including_whitespace_unicode(self):
        b = source_bytes().replace(b'Help someone', 'Help quelqu’un'.encode()) + b'  \n'
        g = self.api.compile_overlay(b)
        self.assertEqual(self.api.reconstruct(g), b)
        self.assertEqual(g['source']['sha256'], hashlib.sha256(b).hexdigest())

    def test_compilation_is_deterministic_and_private_by_default(self):
        a = self.api.compile_overlay(source_bytes())
        self.assertEqual(a, self.api.compile_overlay(source_bytes()))
        self.assertEqual(a['source']['privacy'], 'private')
        self.assertFalse(a['source']['externally_authenticated'])
        self.assertEqual(a['source']['authority'], 'planning-only')

    def test_source_is_not_mutated(self):
        b = source_bytes()
        self.api.compile_overlay(b)
        self.assertEqual(b, source_bytes())

    def test_all_nodes_have_resolvable_source_pointer(self):
        g = self.api.compile_overlay(source_bytes())
        d = overlay()
        for n in g['nodes']:
            self.api.resolve_pointer(d, n['pointer'])
        ids = {n['id'] for n in g['nodes']}
        self.assertTrue(all(e['source'] in ids and e['target'] in ids for e in g['edges']))

    def test_priority_supersession_does_not_erase_base_route(self):
        g = self.api.compile_overlay(source_bytes())
        n = {n['id']: n for n in g['nodes']}
        self.assertEqual(n['base-plan:sample']['state'], 'historical')
        self.assertEqual(n['base-priority:sample']['state'], 'superseded')
        self.assertEqual(n['workstream:sample']['state'], 'coexisting')
        self.assertEqual(n['override:sample']['state'], 'current')
        self.assertIn('Earlier bounded probe.', self.api.reconstruct(g).decode())

    def test_missing_predecessor_remains_unresolved(self):
        g = self.api.compile_overlay(source_bytes())
        self.assertFalse(g['source']['predecessor_bytes_verified'])
        self.assertIn('PREDECESSOR_BYTES_NOT_RETRIEVED', g['remainder'])

    def test_parked_lineage_stays_nonactive(self):
        g = self.api.compile_overlay(source_bytes())
        self.assertEqual(next(n for n in g['nodes'] if n['id'] == 'retained:0')['state'], 'retained')

    def test_json_pointer_escaping(self):
        d = overlay(); d['new_shared_machinery'] = {'A/~B': {'status': 'ACTIVE_SUPPORT'}}
        g = self.api.compile_overlay(source_bytes(d))
        n = next(n for n in g['nodes'] if n['kind'] == 'machinery')
        self.assertEqual(self.api.resolve_pointer(d, n['pointer']), d['new_shared_machinery']['A/~B'])

    def test_tampered_source_fails_closed(self):
        g = self.api.compile_overlay(source_bytes()); g['source']['text'] += ' '
        with self.assertRaises(ValueError): self.api.reconstruct(g)

    def test_tampered_graph_edge_fails_closed(self):
        g = self.api.compile_overlay(source_bytes()); g['edges'][0]['relation'] = 'proves'
        with self.assertRaises(ValueError): self.api.reconstruct(g)

    def test_tampered_graph_state_fails_closed(self):
        g = self.api.compile_overlay(source_bytes()); g['nodes'][0]['state'] = 'scientifically-proved'
        with self.assertRaises(ValueError): self.api.reconstruct(g)

    def test_graph_extra_field_fails_closed(self):
        g = self.api.compile_overlay(source_bytes()); g['publication_approved'] = True
        with self.assertRaises(ValueError): self.api.reconstruct(g)

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError): self.api.compile_overlay(b'{"schema":"x","schema":"y"}')

    def test_nonfinite_json_rejected(self):
        for token in ('NaN', 'Infinity', '-Infinity'):
            with self.subTest(token=token), self.assertRaises(ValueError):
                self.api.compile_overlay(('{"x":'+token+'}').encode())

    def test_duplicate_project_ids_rejected(self):
        d = overlay(); d['portfolio'].append(copy.deepcopy(d['portfolio'][0]))
        with self.assertRaises(ValueError): self.api.compile_overlay(source_bytes(d))

    def test_orphan_override_rejected(self):
        d = overlay(); d['overrides']['missing'] = {'next': ['Do not guess.']}
        with self.assertRaises(ValueError): self.api.compile_overlay(source_bytes(d))

    def test_override_flag_mismatch_rejected(self):
        d = overlay(); d['portfolio'][1]['override_applied'] = False
        with self.assertRaises(ValueError): self.api.compile_overlay(source_bytes(d))

    def test_unknown_schema_rejected(self):
        d = overlay(); d['schema'] += '-future'
        with self.assertRaises(ValueError): self.api.compile_overlay(source_bytes(d))

    def test_unknown_source_fields_preserved_not_interpreted(self):
        d = overlay(); d['new_unknown_annotation'] = {'failed': ['keep me'], 'empty': []}
        g = self.api.compile_overlay(source_bytes(d))
        self.assertEqual(json.loads(self.api.reconstruct(g)), d)
        self.assertIn('UNINTERPRETED_SOURCE_FIELDS', g['remainder'])

    def test_input_size_limit(self):
        with self.assertRaises(ValueError): self.api.compile_overlay(b' ' * (self.api.MAX_BYTES + 1))

    def test_excessive_nesting_rejected(self):
        with self.assertRaises(ValueError): self.api.compile_overlay(b'[' * 150 + b'0' + b']' * 150)


class ActionTests(ModuleCase):
    def setUp(self):
        super().setUp(); self.g = self.api.compile_overlay(source_bytes())

    def result(self, **kw): return self.api.assess_action(self.g, action(**kw))

    def test_read_is_candidate_not_execution(self):
        r = self.result(); self.assertEqual(r['decision'], 'candidate')
        self.assertFalse(r['executes']); self.assertFalse(r['grants_authority'])

    def test_private_lineage_blocks_public_target_claim(self):
        r = self.result(privacy='public')
        self.assertEqual(r['decision'], 'reject')
        self.assertIn('PRIVACY_DOWNGRADE', r['reasons'])

    def test_permission_unknown_defers(self): self.assertEqual(self.result(permission='unknown')['decision'], 'defer')
    def test_permission_denied_rejects(self): self.assertEqual(self.result(permission='denied')['decision'], 'reject')
    def test_target_reject_is_preserved(self): self.assertEqual(self.result(target_decision='reject')['decision'], 'reject')
    def test_stale_revision_defers(self): self.assertIn('REVISION_MOVED', self.result(observed_revision='b'*40)['reasons'])
    def test_unknown_revision_defers(self): self.assertEqual(self.result(observed_revision=None)['decision'], 'defer')
    def test_unbounded_rejected(self): self.assertEqual(self.result(bounded=False)['decision'], 'reject')
    def test_no_recovery_rejected(self): self.assertEqual(self.result(reconstructible=False)['decision'], 'reject')
    def test_zero_delta_no_change(self): self.assertEqual(self.result(delta='zero')['decision'], 'no_change')
    def test_unknown_delta_defers(self): self.assertEqual(self.result(delta='unknown')['decision'], 'defer')
    def test_current_is_not_complete(self): self.assertEqual(self.result(observed_state='unknown')['decision'], 'defer')

    def test_merged_repair_is_not_requeued(self):
        r = self.result(operation='repair', observed_state='merged')
        self.assertEqual(r['decision'], 'no_change'); self.assertIn('ALREADY_MERGED', r['reasons'])

    def test_merge_release_publish_are_separate_decisions(self):
        for op in ('merge', 'release', 'publish'):
            with self.subTest(op=op):
                r = self.result(operation=op, target_decision='accept', target_decision_ref='native:decision')
                self.assertEqual(r['decision'], 'defer'); self.assertFalse(r['executes'])

    def test_native_acceptance_required_for_repair(self):
        self.assertEqual(self.result(operation='repair')['decision'], 'defer')
        self.assertEqual(self.result(operation='repair',target_decision='accept')['decision'], 'defer')
        self.assertEqual(self.result(operation='repair',target_decision='accept',target_decision_ref='native:decision')['decision'], 'candidate')

    def test_active_writer_blocks_repair_not_read(self):
        self.assertEqual(self.result(active_writer=True)['decision'], 'candidate')
        self.assertEqual(self.result(operation='repair',target_decision='accept',target_decision_ref='native:decision',active_writer=True)['decision'], 'defer')

    def test_dependency_gate(self):
        r = self.result(dependencies=[{'id':'native-receipt', 'satisfied':False}])
        self.assertIn('DEPENDENCY_UNRESOLVED', r['reasons']); self.assertEqual(r['decision'], 'defer')

    def test_no_coercion_of_false_strings(self):
        for k in ('bounded','reconstructible','active_writer'):
            with self.subTest(k=k), self.assertRaises(ValueError): self.result(**{k:'false'})

    def test_required_meaning_not_optional(self):
        for k in ('usefulness','expectation','observation','counterprobe','way_back'):
            with self.subTest(k=k), self.assertRaises(ValueError): self.result(**{k:''})

    def test_unknown_fields_rejected(self):
        with self.assertRaises(ValueError): self.result(force=True)

    def test_unknown_node_rejected(self):
        with self.assertRaises(ValueError): self.result(node='workstream:invented')

    def test_priority_is_explicit_in_range(self):
        for p in (0, 3, True, 1.5, '1'):
            with self.subTest(p=p), self.assertRaises(ValueError): self.result(priority=p)

    def test_selector_keeps_priority_and_all_reasons(self):
        actions=[action(id='second',priority=2),action(id='first',priority=1),action(id='blocked',priority=1,permission='denied')]
        original=copy.deepcopy(actions)
        r=self.api.select_next(self.g,actions)
        self.assertEqual(r['selected'],'first'); self.assertEqual(len(r['assessments']),3)
        self.assertEqual(actions,original)

    def test_no_ready_action_selects_none(self):
        self.assertIsNone(self.api.select_next(self.g,[action(delta='zero')])['selected'])

    def test_duplicate_actions_rejected(self):
        with self.assertRaises(ValueError): self.api.select_next(self.g,[action(),action()])

    def test_private_public_export_fails_closed(self):
        for privacy in ('private','private-derived','unknown'):
            with self.subTest(privacy=privacy), self.assertRaises(ValueError):
                self.api.export_public(self.api.compile_overlay(source_bytes(), privacy=privacy), approved=True)

    def test_public_label_does_not_grant_export_approval(self):
        g=self.api.compile_overlay(source_bytes(),privacy='public')
        with self.assertRaises(ValueError): self.api.export_public(g,approved=False)
        self.assertEqual(self.api.export_public(g,approved=True),g)


    def test_stale_zero_delta_requires_reobservation(self):
        r=self.result(delta='zero', observed_revision='b'*40)
        self.assertEqual(r['decision'],'defer')
        self.assertIn('REVISION_MOVED',r['reasons'])

    def test_stale_merged_observation_requires_reobservation(self):
        r=self.result(operation='repair',observed_state='merged',observed_revision='b'*40)
        self.assertEqual(r['decision'],'defer')

    def test_receipt_carries_reconstructible_proposal(self):
        a=action(); r=self.api.assess_action(self.g,a)
        self.assertEqual(r['proposal'],a)
        self.assertEqual(r['source_sha256'],self.g['source']['sha256'])
        r['proposal']['expectation']='changed'
        self.assertNotEqual(a['expectation'],'changed')

    def test_malformed_target_rejected_without_type_coercion(self):
        with self.assertRaises(ValueError): self.result(node=[])

    def test_graph_boolean_is_not_integer_equivalent(self):
        g=copy.deepcopy(self.g);g['source']['externally_authenticated']=0
        with self.assertRaises(ValueError): self.api.reconstruct(g)

    def test_large_exponent_is_not_finite_json(self):
        with self.assertRaises(ValueError): self.api.compile_overlay(b'{"x":1e999}')


class CLITests(ModuleCase):
    def runcli(self,*args): return subprocess.run([sys.executable,str(MODULE),*args],capture_output=True)
    def test_cli_roundtrip_and_read_only(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'source.json'; p.write_bytes(source_bytes()); before=p.read_bytes()
            out=self.runcli('graph',str(p));self.assertEqual(out.returncode,0,out.stderr)
            g=Path(td)/'graph.json';g.write_bytes(out.stdout)
            restored=self.runcli('restore',str(g));self.assertEqual(restored.returncode,0,restored.stderr)
            self.assertEqual(restored.stdout,before);self.assertEqual(p.read_bytes(),before)
            self.assertEqual(sorted(x.name for x in Path(td).iterdir()),['graph.json','source.json'])

    def test_invalid_input_errors_without_echoing_private_content(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'bad.json';p.write_bytes(b'{private-secret-unexpected')
            r=self.runcli('graph',str(p));self.assertNotEqual(r.returncode,0)
            self.assertEqual(r.stdout,b'');self.assertNotIn(b'private-secret-unexpected',r.stderr)

    def test_symlink_input_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'source.json';p.write_bytes(source_bytes())
            link=Path(td)/'link.json';link.symlink_to(p)
            self.assertNotEqual(self.runcli('graph',str(link)).returncode,0)


class WorkflowTests(unittest.TestCase):
    def test_read_only_exact_head_workflow_and_dependency_coverage(self):
        path=ROOT / '.github' / 'workflows' / 'plan-authority.yml'
        self.assertTrue(path.exists(), 'The new executable must have an exact-head CI gate')
        workflow=path.read_text()
        self.assertIn('permissions: {}',workflow)
        self.assertNotIn('pull_request_target',workflow)
        self.assertIn('github.event.pull_request.head.sha',workflow)
        for item in ('tools/plan_authority.py','tests/test_plan_authority.py','plan-authority/**','.github/workflows/plan-authority.yml'):
            self.assertEqual(workflow.count("- '"+item+"'"),2,item)
        self.assertIn('python3 -m unittest discover -s tests -v',workflow)
        self.assertIn('cmp plan-authority/example-overlay.json',workflow)


if __name__ == '__main__': unittest.main()
