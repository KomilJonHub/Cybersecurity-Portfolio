"""Regression coverage for validating repository-owned documentation only."""

import contextlib
import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'check_portfolio.py'
spec = importlib.util.spec_from_file_location('check_portfolio', SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

FOOTER = ('\n> **Author:** Komiljon Karimov<br>\n'
          + checker.MISSION + '\n')


class RepositoryValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '--quiet', str(self.root)], check=True)
        self.write('.gitignore', '.venv/\n__pycache__/\n')
        self.write('README.md', '# Portfolio\n\n[Domain](01_Test/README.md)\n' + FOOTER)
        self.write('01_Test/README.md', '# Domain\n\n[Home](../README.md)\n' + FOOTER)
        subprocess.run(['git', 'add', '.'], cwd=self.root, check=True)
        self.root_patch = patch.object(checker, 'ROOT', self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def validate(self):
        output, errors = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            result = checker.main()
        return result, output.getvalue(), errors.getvalue()

    def test_tracked_documentation_retains_existing_checks(self):
        result, output, errors = self.validate()
        self.assertFalse(result)
        self.assertIn('2 Markdown files', output)
        self.assertIn('2 README pages: 0 errors', output)
        self.assertEqual(errors, '')

    def test_ignored_venv_and_cache_readmes_are_not_portfolio_pages(self):
        for folder in ['07_Scripting_Automation/Python/Keylogger/.venv/lib/package',
                       '01_Test/__pycache__']:
            self.write(folder + '/README.md', '# Dependency\n[Guide](missing.md)\n')
        result, output, errors = self.validate()
        self.assertFalse(result)
        self.assertIn('2 Markdown files', output)
        self.assertEqual(errors, '')

    def test_untracked_nonignored_documentation_is_validated(self):
        self.write('01_Test/new guide.md', '# New guide\n[Home](../README.md)\n')
        result, output, errors = self.validate()
        self.assertFalse(result)
        self.assertIn('3 Markdown files', output)
        self.assertEqual(errors, '')
        # A typo in an untracked document must still fail before it is staged.
        self.write('01_Test/new guide.md', '# New guide\n[Missing](not-here.png)\n')
        result, _, errors = self.validate()
        self.assertTrue(result)
        self.assertIn('new guide.md: missing target not-here.png', errors)

    def test_tracked_document_still_checked_after_matching_ignore_rule(self):
        self.write('.gitignore', '.venv/\n__pycache__/\n01_Test/\n')
        self.write('01_Test/README.md', '# Domain\n[Missing](not-here.pdf)\n' + FOOTER)
        result, _, errors = self.validate()
        self.assertTrue(result)
        self.assertIn('01_Test/README.md: missing target not-here.pdf', errors)

    def test_anchor_footer_and_reachability_failures_are_retained(self):
        self.write('README.md', '# Portfolio\n[Domain](01_Test/README.md#missing)\n' + FOOTER)
        self.write('01_Test/README.md', '# Domain\n[Home](../README.md)\n')
        self.write('01_Test/Orphan/README.md', '# Orphan\n' + FOOTER)
        result, _, errors = self.validate()
        self.assertTrue(result)
        self.assertIn('missing anchor 01_Test/README.md#missing', errors)
        self.assertIn('01_Test/README.md: expected one standard author/mission footer', errors)
        self.assertIn('01_Test/Orphan/README.md: unreachable from portfolio homepage', errors)


if __name__ == '__main__':
    unittest.main()
