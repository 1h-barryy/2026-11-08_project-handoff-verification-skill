import asyncio
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from server import inspect_context
from smoke_client import inspect_over_stdio


class InspectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        self.write("main.py", 'from shared import validate\nif __name__ == "__main__":\n    validate()\n')
        self.write("worker.py", "from shared import validate\n")
        self.write("shared.py", "def validate():\n    return True\n")
        self.write("requirements.txt", "mcp==2.3.0\n")

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def snapshot(self):
        return {str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.root.rglob("*") if p.is_file()}

    def test_evidence_impact_and_no_mutation(self):
        before = self.snapshot()
        result = inspect_context(self.root, "change shared validation")
        self.assertEqual(before, self.snapshot())
        self.assertIn("main.py", result["assumptions"]["likely_entry_points"])
        shared = next(row for row in result["assumptions"]["shared_files_to_review"] if row["path"] == "shared.py")
        self.assertEqual(shared["possible_dependents"], ["main.py", "worker.py"])
        for match in result["verified_findings"]["task_matches"]:
            for evidence in match["evidence"]:
                actual = (self.root / evidence["path"]).read_text().splitlines()[evidence["line"] - 1]
                self.assertEqual(evidence["excerpt"], actual[:240])

    def test_exclusions_and_root_boundary(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (outside / "private.py").write_text("outside_secret = True")
        self.write(".env", "SECRET=hidden")
        self.write("node_modules/pkg/index.js", "secret dependency")
        self.write("large.py", "x" * (128 * 1024 + 1))
        link = self.root / "linked"
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)], check=True, capture_output=True)
            self.addCleanup(os.rmdir, link)
        else:
            link.symlink_to(outside, target_is_directory=True)
        result = inspect_context(self.root, "outside secret")
        structure = result["verified_findings"]["structure"]
        self.assertNotIn(".env", structure)
        self.assertFalse(any("private.py" in name or "node_modules" in name for name in structure))
        self.assertEqual(result["coverage"]["skipped"]["links"], 1)
        self.assertEqual(result["coverage"]["skipped"]["oversized_files"], 1)
        self.assertEqual(result["verified_findings"]["task_matches"], [])

    def test_js_relative_import(self):
        self.write("src/main.ts", "import { theme } from './shared/theme';\n")
        self.write("src/shared/theme.ts", "export const theme = 'light';\n")
        result = inspect_context(self.root, "theme")
        edges = result["assumptions"]["possible_local_dependencies_and_impact"]
        self.assertTrue(any(e["source"] == "src/main.ts" and e["target"] == "src/shared/theme.ts" for e in edges))

    def test_entry_point_is_code_not_string_and_identifiers_rank_first(self):
        self.write("notes.py", 'example = "if __name__ == \'__main__\':"\n')
        self.write("feature.py", "def inspect_project_context(task):\n    return task\n")
        result = inspect_context(self.root, "change inspect_project_context")
        self.assertNotIn("notes.py", result["assumptions"]["likely_entry_points"])
        self.assertEqual(result["assumptions"]["related_files"][0], "feature.py")

    def test_limits_and_invalid_input(self):
        with patch("server.MAX_FILES", 2):
            result = inspect_context(self.root, "shared")
        self.assertTrue(result["coverage"]["inventory_truncated"])
        self.assertLessEqual(result["coverage"]["inventoried_files"], 2)
        with self.assertRaises(ValueError):
            inspect_context(self.root, " ")
        with self.assertRaises(ValueError):
            inspect_context(self.root, "x" * 4001)
        with self.assertRaises(FileNotFoundError):
            inspect_context(self.root / "missing", "shared")

    def test_real_stdio(self):
        before = self.snapshot()
        result = asyncio.run(inspect_over_stdio(self.root, "shared validation"))
        self.assertEqual(result["project_root"], str(self.root.resolve()))
        self.assertIn("shared.py", result["assumptions"]["related_files"])
        self.assertEqual(before, self.snapshot())

    def test_constant_definitions_are_syntax_with_bounded_output(self):
        self.write("limits.py", '"MAX_FAKE = 1"\n# MAX_COMMENT = 2\nMAX_FILES: int = 1000\n'
                   'MAX_BYTES = 128 * 1024\nDECLARED_ONLY: int\n'
                   'def helper():\n    MAX_LOCAL = 3\n')
        self.write("node_modules/limits.py", "MAX_EXCLUDED = 4\n")
        result = inspect_context(self.root, "limits")
        definitions = result["verified_findings"]["python_constant_definitions"]
        self.assertEqual([(row["name"], row["path"], row["line"]) for row in definitions],
                         [("MAX_FILES", "limits.py", 3), ("MAX_BYTES", "limits.py", 4)])
        for row in definitions:
            self.assertEqual(row["excerpt"], (self.root / row["path"]).read_text().splitlines()[row["line"] - 1])
        self.assertFalse(result["coverage"]["output_truncated"]["constant_definitions"])
        with patch("server.MAX_RESULTS", 1):
            capped = inspect_context(self.root, "limits")
        self.assertEqual(len(capped["verified_findings"]["python_constant_definitions"]), 1)
        self.assertTrue(capped["coverage"]["output_truncated"]["constant_definitions"])

    def test_scan_limit_locations_over_real_stdio(self):
        root = Path(__file__).resolve().parents[1]
        result = asyncio.run(inspect_over_stdio(root, "Change the file scanning limits in our MCP server."))
        definitions = {row["name"]: row for row in result["verified_findings"]["python_constant_definitions"]
                       if row["path"] == "server.py"}
        lines = (root / "server.py").read_text().splitlines()
        for name in ("MAX_ENTRIES", "MAX_FILES", "MAX_BYTES", "MAX_TOTAL_BYTES"):
            row = definitions[name]
            self.assertTrue(lines[row["line"] - 1].startswith(name + " = "))
            self.assertEqual(row["excerpt"], lines[row["line"] - 1])
        self.assertEqual(result["coverage"]["limits"],
                         {"entries": 6000, "files": 1000, "bytes_per_file": 131072, "total_bytes": 4194304})


if __name__ == "__main__":
    unittest.main()
