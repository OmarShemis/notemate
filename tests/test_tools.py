import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from notemate.tools import calculate, read_notes, save_note


class ToolsTests(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(calculate("23 * 7 + 1"), "162")
        self.assertEqual(calculate("-(2 + 3) / 2"), "-2.5")

    def test_unsafe_and_unbounded_expressions(self):
        for expression in [
            "2 ** 999999999",
            "__import__('os')",
            "1/0",
            "1e309",
            "True",
            "[1]",
            "9" * 257,
            "-" * 30 + "1",
        ]:
            with self.subTest(expression=expression):
                self.assertTrue(calculate(expression).startswith("Error:"))

    def test_notes_are_persistent_and_append_only(self):
        with (
            TemporaryDirectory() as folder,
            patch.dict(
                os.environ,
                {"NOTEMATE_NOTES_FILE": str(Path(folder) / "nested/notes.txt")},
            ),
        ):
            self.assertEqual(read_notes(), "No notes saved yet.")
            self.assertTrue(save_note(" ").startswith("Error:"))
            save_note("First")
            save_note("Second")
            self.assertEqual(read_notes(), "- First\n- Second\n")

    def test_agent_with_offline_model(self):
        from pydantic_ai.models.test import TestModel
        from notemate.agent import build_agent

        agent = build_agent(TestModel(call_tools=[], custom_output_text="Ready"))
        self.assertEqual(agent.run_sync("Hello").output, "Ready")


if __name__ == "__main__":
    unittest.main()
