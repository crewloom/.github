import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('sync_docs', Path(__file__).with_name('sync-docs.py'))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=test', '-c', 'user.email=test@example.invalid',
                        'commit', '--allow-empty', '-qm', 'fixture'], check=True)
        (self.root / 'package.json').write_text(json.dumps({'name': 'existing-name', 'version': '1.2.3'}))
        (self.root / '.agents/skills/a').mkdir(parents=True)
        (self.root / '.agents/skills/a/SKILL.md').write_text('fixture')
        (self.root / 'registry.json').write_text('{"tools": [{"id": "one"}, {"id": "two"}]}')
        self.project = {'id': 'test', 'repository': 'bridge', 'ref': 'main', 'version_file': 'package.json',
                        'format': 'json', 'output': 'docs/CREWLOOM_FACTS.md',
                        'counts': {'skills': {'glob': '.agents/skills/*/SKILL.md'},
                                   'tools': {'json_file': 'registry.json', 'key': 'tools'}}}

    def test_structural_counts_and_distinct_versions(self):
        facts = sync.collect(self.project, self.root, {'tag': 'v1.0.0'})
        self.assertEqual(facts['counts'], {'skills': 1, 'tools': 2})
        self.assertEqual(facts['source_version'], '1.2.3')
        rendered = sync.render([facts])
        self.assertIn('v1.0.0', rendered)
        self.assertIn('1.2.3', rendered)
        self.assertEqual(rendered, sync.render([facts]))

    def test_changed_source_updates_output(self):
        first = sync.render([sync.collect(self.project, self.root, None)])
        (self.root / 'package.json').write_text('{"name":"existing-name","version":"1.2.4"}')
        self.assertNotEqual(first, sync.render([sync.collect(self.project, self.root, None)]))

    def test_missing_source_fails(self):
        (self.root / 'package.json').unlink()
        with self.assertRaises(FileNotFoundError):
            sync.collect(self.project, self.root, None)

    def test_unsafe_paths_rejected(self):
        for path in ('../README.md', '/tmp/README.md'):
            with self.assertRaises(ValueError):
                sync.relative(path)

    def test_symlink_escape_rejected(self):
        (self.root / 'package.json').unlink()
        (self.root / 'package.json').symlink_to('/etc/passwd')
        with self.assertRaises(ValueError):
            sync.collect(self.project, self.root, None)

    def test_markup_is_data(self):
        self.assertEqual(sync.safe('<x>|`\n'), '&lt;x&gt;&#124;&#96; ')

    def test_manifest_output_allowlist(self):
        manifest = {'schema_version': 1, 'organization': 'crewloom', 'projects': [self.project]}
        path = self.root / 'manifest.json'
        path.write_text(json.dumps(manifest))
        sync.load_manifest(path)
        self.project['output'] = 'README.md'
        path.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            sync.load_manifest(path)

    def test_publish_unchanged_has_no_git_write(self):
        output = self.root / self.project['output']
        output.parent.mkdir()
        output.write_text('same')
        self.assertEqual(sync.publish(self.root, self.project['output'], 'same', 'crewloom/bridge'), 'unchanged')

    def test_open_sync_pr_is_not_rewritten(self):
        with patch.object(sync, 'run', return_value='[{"headRefName":"bot/manifest-docs-sync-old","url":"test"}]') as command:
            self.assertIn('existing sync PR', sync.publish(self.root, self.project['output'], 'new', 'crewloom/bridge'))
            self.assertEqual(command.call_count, 1)

    def test_publish_stages_only_allowlisted_output(self):
        calls = []
        def command(*args, cwd=None):
            calls.append(args)
            if args[:3] == ('gh', 'pr', 'list'):
                return '[]'
            if args[:4] == ('git', 'diff', '--cached', '--name-only'):
                return 'docs/CREWLOOM_FACTS.md'
            if args[:3] == ('gh', 'pr', 'create'):
                return 'review-pr'
            return ''
        with patch.object(sync, 'run', side_effect=command):
            self.assertEqual(sync.publish(self.root, self.project['output'], 'new', 'crewloom/bridge'), 'review-pr')
        self.assertIn(('git', 'add', '--', 'docs/CREWLOOM_FACTS.md'), calls)
        self.assertFalse(any('--force' in str(call) or 'merge' in call for call in calls))
        self.assertEqual((self.root / self.project['output']).read_text(), 'new')

    def test_unexpected_staged_file_aborts_before_push(self):
        calls = []
        def command(*args, cwd=None):
            calls.append(args)
            if args[:3] == ('gh', 'pr', 'list'):
                return '[]'
            if args[:4] == ('git', 'diff', '--cached', '--name-only'):
                return 'package.json'
            return ''
        with patch.object(sync, 'run', side_effect=command):
            with self.assertRaises(ValueError):
                sync.publish(self.root, self.project['output'], 'new', 'crewloom/bridge')
        self.assertFalse(any('push' in call for call in calls))

    def test_offline_preview_is_not_a_missing_release_claim(self):
        rendered = sync.render([sync.collect(self.project, self.root, 'offline')])
        self.assertIn('Not checked (offline preview)', rendered)
        self.assertNotIn('No stable GitHub release found', rendered)

    def test_toml_project_version(self):
        (self.root / 'pyproject.toml').write_text('[project]\nname="core"\nversion="0.9.24"\n')
        self.project.update(format='toml', version_file='pyproject.toml')
        self.assertEqual(sync.collect(self.project, self.root, None)['source_version'], '0.9.24')


if __name__ == '__main__':
    unittest.main()
