from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).parents[1]
PROMPT_PATH = ROOT / "prompts" / "agnostic-software-development-system.md"
MAPPING_PATH = ROOT / "tests" / "fixtures" / "expanded_prompt_sections.json"


def load_data():
    return json.loads(MAPPING_PATH.read_text(encoding="utf-8"))


def markdown_headings(text):
    return [m.group(1).strip() for m in re.finditer(r"^#{2,3}\s+(.+?)\s*$", text, re.MULTILINE)]


def section_text(text, heading, next_heading=None):
    start = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
    if not start:
        return ""
    tail = text[start.end():]
    if next_heading:
        end = re.search(rf"^##\s+{re.escape(next_heading)}\s*$", tail, re.MULTILINE)
        return tail[:end.start()] if end else tail
    return tail


class ExpandedPromptContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_data()
        cls.prompt = PROMPT_PATH.read_text(encoding="utf-8")
        cls.headings = markdown_headings(cls.prompt)
        cls.lower = cls.prompt.lower()

    def test_prompt_is_present_and_expanded(self):
        self.assertTrue(PROMPT_PATH.is_file())
        self.assertGreaterEqual(len(self.prompt.splitlines()), 600)

    def test_required_headings_exist_in_order(self):
        expected = [row["abstract_heading"] for row in self.data["sections"]]
        missing = [heading for heading in expected if heading not in self.headings]
        self.assertFalse(missing, f"missing abstract sections: {missing}")
        positions = [self.headings.index(heading) for heading in expected]
        self.assertEqual(positions, sorted(positions))

    def test_each_section_has_common_contract(self):
        fields = self.data["common_contract_fields"]
        missing = {}
        for row in self.data["sections"]:
            body = section_text(self.prompt, row["abstract_heading"]).lower()
            absent = [field for field in fields if field.lower() not in body]
            if absent:
                missing[row["abstract_heading"]] = absent
        self.assertFalse(missing, f"missing contract fields: {missing}")

    def test_task_operations_are_separate(self):
        task_heads = [row["abstract_heading"] for row in self.data["sections"] if row["source_boundary"].startswith("Task")]
        self.assertEqual(len(task_heads), 6)
        for heading in task_heads:
            self.assertIn(heading, self.headings)

    def test_no_source_specific_operational_coupling(self):
        forbidden = ("claude code", "anthropic", "openai", "gpt-", "fable 5", "/home/", "/users/", "@gmail.com", "zsh")
        found = [value for value in forbidden if value in self.lower]
        self.assertFalse(found, f"forbidden identifiers in prompt: {found}")

    def test_no_gender_or_unresolved_policy_content(self):
        forbidden = ("gender-neutral pronoun", "pronoun default", "gender inference", "infer pronouns", "they/them default")
        found = [value for value in forbidden if value in self.lower]
        self.assertFalse(found, f"forbidden policy terms: {found}")
        self.assertNotRegex(self.prompt, r"(?im)\b(?:TBD|TODO|FIXME)\b")

    def test_required_state_and_completion_boundaries_exist(self):
        for phrase in ("unavailable", "denied", "failed", "timed out", "partially completed", "unknown", "authorization boundary", "retry policy", "verification"):
            self.assertIn(phrase, self.lower)
        self.assertIn("local completion", self.lower)
        self.assertIn("external completion", self.lower)


if __name__ == "__main__":
    unittest.main()
