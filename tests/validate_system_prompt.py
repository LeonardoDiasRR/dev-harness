from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).parents[1]
SOURCE_PATH = ROOT / "leaks" / "claude-code-fable-5.md"
PROMPT_PATH = ROOT / "prompts" / "system-prompt.md"
MAPPING_PATH = ROOT / "tests" / "fixtures" / "system_prompt_transformations.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def headings(text):
    return [match.group(1).strip() for match in re.finditer(r"^#{1,2}\s+(.+?)\s*$", text, re.MULTILINE)]


def heading_tree(text):
    return [
        (len(match.group(1)), match.group(2).strip())
        for match in re.finditer(r"^(#{1,3})\s+(.+?)\s*$", text, re.MULTILINE)
    ]


def section_body(text, heading):
    match = re.search(rf"^([#]{{1,2}})\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
    if not match:
        return ""
    level = len(match.group(1))
    tail = text[match.end():]
    end = re.search(rf"^#{{1,{level}}}\s+", tail, re.MULTILINE)
    return tail[:end.start()] if end else tail


class SystemPromptTransformationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE_PATH.read_text(encoding="utf-8")
        cls.mapping = load_json(MAPPING_PATH)
        cls.prompt = PROMPT_PATH.read_text(encoding="utf-8")
        cls.prompt_headings = headings(cls.prompt)
        cls.prompt_lower = cls.prompt.lower()

    def test_map_covers_every_source_top_level_heading_once(self):
        source_headings = [heading for heading in headings(self.source) if heading != "System prompt"]
        mapped_headings = [item["source_heading"] for item in self.mapping["sections"]]
        self.assertEqual(mapped_headings, source_headings)
        self.assertEqual(len(mapped_headings), len(set(mapped_headings)))

    def test_map_uses_only_approved_outcomes(self):
        allowed = {"preserve", "generalize", "placeholder", "remove"}
        outcomes = {item["outcome"] for item in self.mapping["sections"]}
        self.assertTrue(outcomes <= allowed)
        self.assertTrue(all(item["rationale"].strip() for item in self.mapping["sections"]))

    def test_map_records_transformation_traceability(self):
        required = {
            "source_locator", "target_locator", "replacement_category",
            "replacement_terms", "rationale"
        }
        missing = {
            row["source_heading"]: sorted(required - row.keys())
            for row in self.mapping["sections"]
            if required - row.keys()
        }
        self.assertFalse(missing, f"incomplete transformation records: {missing}")
        self.assertTrue(all(isinstance(row["replacement_terms"], list) for row in self.mapping["sections"]))

    def test_major_internal_rewrites_have_detailed_traceability(self):
        required = {"Artifact", "CronCreate", "DesignSync", "ScheduleWakeup", "TaskOutput", "WebFetch", "Workflow"}
        records = self.mapping["detailed_transformations"]
        covered = {
            record["source_locator"].split(":", 1)[1]
            for record in records
            if record["source_locator"].startswith("heading:")
        }
        self.assertTrue(required <= covered)
        for record in records:
            self.assertTrue(record["source_locator"])
            self.assertTrue(record["target_locator"])
            self.assertTrue(record["replacement_category"])
            self.assertTrue(record["replacement_terms"])
            self.assertTrue(record["rationale"])

    def test_target_headings_follow_the_transformation_map(self):
        required = [item["target_heading"] for item in self.mapping["sections"] if item["outcome"] != "remove"]
        missing = [heading for heading in required if heading not in self.prompt_headings]
        self.assertFalse(missing, f"missing target headings: {missing}")
        positions = [self.prompt_headings.index(heading) for heading in required]
        self.assertEqual(positions, sorted(positions))

    def test_target_has_no_unmapped_headings(self):
        section_renames = {
            row["source_heading"]: row["target_heading"]
            for row in self.mapping["sections"]
        }
        subsection_renames = self.mapping["subheading_renames"]
        expected = []
        for level, title in heading_tree(self.source):
            if level <= 2:
                title = section_renames.get(title, title)
            else:
                title = subsection_renames.get(title, title)
            expected.append((level, title))
        self.assertEqual(heading_tree(self.prompt), expected)

    def test_target_preserves_source_heading_count(self):
        self.assertEqual(len(heading_tree(self.source)), 99)
        self.assertEqual(len(heading_tree(self.prompt)), 99)

    def test_target_has_generic_identity_and_session_placeholders(self):
        self.assertIn("interactive software-development agent", self.prompt_lower)
        for value in ("<project-directory>", "<platform>", "<shell>", "<scratchpad-directory>", "<project-instructions>", "<current-date>"):
            self.assertIn(value, self.prompt)

    def test_target_has_no_source_identity_or_session_data(self):
        forbidden = (
            "claude", "anthropic", "fable", "mythos", "opus", "sonnet", "haiku",
            "asgeirtj", "@gmail.com", "darwin 25.5.0", "claude.ai", "/users/asgeirtj/",
            "claude-fable-5", "claude-opus-4-8", "claude-sonnet-5", "claude-haiku-4-5-20251001"
        )
        found = [value for value in forbidden if value in self.prompt_lower]
        self.assertFalse(found, f"source-specific content in target: {found}")

    def assert_no_patterns(self, key):
        matches = {
            pattern: re.findall(pattern, self.prompt)
            for pattern in self.mapping[key]
            if re.search(pattern, self.prompt)
        }
        self.assertFalse(matches, f"prohibited target content: {matches}")

    def test_target_has_no_source_runtime_coupling(self):
        self.assert_no_patterns("prohibited_target_patterns")

    def test_target_has_no_concrete_session_data(self):
        self.assert_no_patterns("prohibited_session_patterns")

    def test_target_keeps_required_operational_boundaries(self):
        required = (
            "authorized security testing", "destructive", "mass targeting",
            "permission", "denied", "retry verbatim", "verification",
            "hard to reverse", "outward-facing", "unknown"
        )
        missing = [value for value in required if value not in self.prompt_lower]
        self.assertFalse(missing, f"missing operational boundaries: {missing}")

    def test_required_portable_concepts_survive(self):
        missing = {}
        for heading, concepts in self.mapping["required_section_concepts"].items():
            body = section_body(self.prompt, heading).lower()
            absent = [concept for concept in concepts if concept.lower() not in body]
            if absent:
                missing[heading] = absent
        self.assertFalse(missing, f"missing portable concepts: {missing}")

    def test_abstract_capability_sections_name_their_contract(self):
        missing = {}
        for heading, term in self.mapping["abstract_capability_terms"].items():
            body = section_body(self.prompt, heading).lower()
            if term.lower() not in body:
                missing[heading] = term
        self.assertFalse(missing, f"missing abstract capability terms: {missing}")

    def test_generalized_sections_have_a_distinct_generic_destination(self):
        generalizations = [item for item in self.mapping["sections"] if item["outcome"] == "generalize"]
        self.assertTrue(generalizations)
        unchanged = [item["source_heading"] for item in generalizations if item["source_heading"] == item["target_heading"]]
        self.assertFalse(unchanged, f"untranslated generic sections: {unchanged}")

    def test_prompt_has_no_unresolved_placeholders(self):
        placeholders = re.findall(r"<([a-z][a-z0-9-]*)>", self.prompt)
        self.assertTrue(placeholders)
        self.assertNotRegex(self.prompt, r"(?im)^\s*(?:TBD|TODO|FIXME)\s*$")

    def test_removed_source_preamble_has_a_documented_reason(self):
        preamble = self.mapping["source_preamble"]
        self.assertEqual(preamble["identity_outcome"], "generalize")
        self.assertEqual(preamble["model_marketing_outcome"], "remove")
        self.assertTrue(preamble["model_marketing_rationale"].strip())

    def test_no_dangling_attribution_directives(self):
        self.assertNotIn("End git commit messages with:", self.prompt)
        self.assertNotIn("End PR bodies with:", self.prompt)

    def test_runtime_placeholders_use_lower_kebab_case(self):
        known_bad = ("<transcriptDir>", "<task-notification>", "<project-dir>", "<scratchpad-dir>")
        found = [value for value in known_bad if value in self.prompt]
        self.assertFalse(found, f"non-canonical runtime placeholders: {found}")
        tokens = re.findall(r"<([A-Za-z][A-Za-z0-9-]*)>", self.prompt)
        invalid = [token for token in tokens if not re.fullmatch(r"[a-z][a-z0-9-]*", token)]
        self.assertFalse(invalid, f"invalid placeholder names: {invalid}")

    def test_target_contains_no_mechanical_replacement_artifacts(self):
        artifacts = ("the the ", "a the agent", "this the agent", ".the agent", "the agent-code")
        found = [value for value in artifacts if value in self.prompt_lower]
        self.assertFalse(found, f"mechanical replacement artifacts: {found}")

    def test_json_fences_remain_valid(self):
        invalid = []
        for index, block in enumerate(re.findall(r"```json\s*\n(.*?)\n```", self.prompt, re.DOTALL), 1):
            try:
                json.loads(block)
            except json.JSONDecodeError as error:
                invalid.append((index, error.msg))
        self.assertFalse(invalid, f"invalid JSON fences: {invalid}")

    def test_each_tool_derived_section_retains_a_schema(self):
        rows = self.mapping["sections"]
        first = next(index for index, row in enumerate(rows) if row["source_heading"] == "Agent")
        missing = [
            row["target_heading"]
            for row in rows[first:]
            if "```json" not in section_body(self.prompt, row["target_heading"])
        ]
        self.assertFalse(missing, f"tool-derived sections without schemas: {missing}")

    def test_target_retains_substantial_source_detail(self):
        ratio = len(self.prompt.splitlines()) / len(self.source.splitlines())
        self.assertGreaterEqual(ratio, 0.7)


if __name__ == "__main__":
    unittest.main()
