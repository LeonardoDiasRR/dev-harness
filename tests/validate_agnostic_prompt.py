from pathlib import Path
import re
import unittest

PROMPT_PATH = Path(__file__).parents[1] / "prompts" / "agnostic-software-development-system.md"

REQUIRED_HEADINGS = {
    "Identity and scope",
    "Communication",
    "Instruction precedence and trust boundaries",
    "Context discovery and planning",
    "Autonomy and authorization",
    "Abstract capability contracts",
    "Software-engineering workflow",
    "Security and dual-use work",
    "Memory and context management",
    "Completion and handoff",
}

REQUIRED_CAPABILITIES = {
    "project inspection",
    "file modification",
    "command execution",
    "version control",
    "web and documentation research",
    "delegated work",
    "reusable procedures",
    "scheduling and monitoring",
    "persistent memory",
    "artifact generation and publication",
    "user interaction",
}

FORBIDDEN_OPERATIONAL_IDENTIFIERS = (
    "claude code", "anthropic", "openai", "gpt-", "fable 5", "mythos 5",
    "/users/", "/home/", "@gmail.com", "claude.ai", "openai.com",
    "<project-dir>", "<scratchpad-dir>", "darwin", "zsh",
)

FORBIDDEN_GENDER_POLICY_TERMS = (
    "gender-neutral pronoun", "pronoun default", "infer pronouns",
    "they/them default", "gender inference", "neutral pronoun policy",
)

REQUIRED_PHRASES = (
    "capability is unavailable",
    "do not retry",
    "before deleting or overwriting",
    "authorized security testing",
    "denial-of-service",
    "fresh verification evidence",
    "do not claim completion",
)


def load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


class PromptContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prompt = load_prompt()
        cls.lower = cls.prompt.lower()

    def test_prompt_file_exists_and_is_nontrivial(self):
        self.assertTrue(PROMPT_PATH.is_file())
        self.assertGreater(len(self.prompt), 8000)

    def test_required_headings_exist(self):
        headings = {
            match.group(1).strip().lower()
            for match in re.finditer(r"^#{2,3}\s+(.+?)\s*$", self.prompt, re.MULTILINE)
        }
        missing = {heading.lower() for heading in REQUIRED_HEADINGS} - headings
        self.assertFalse(missing, f"missing headings: {sorted(missing)}")

    def test_all_abstract_capabilities_are_named(self):
        missing = {capability for capability in REQUIRED_CAPABILITIES if capability not in self.lower}
        self.assertFalse(missing, f"missing capabilities: {sorted(missing)}")

    def test_required_behavioral_boundaries_exist(self):
        missing = [phrase for phrase in REQUIRED_PHRASES if phrase not in self.lower]
        self.assertFalse(missing, f"missing behavioral phrases: {missing}")

    def test_no_operational_vendor_or_environment_coupling(self):
        found = [value for value in FORBIDDEN_OPERATIONAL_IDENTIFIERS if value in self.lower]
        self.assertFalse(found, f"operational identifiers found: {found}")

    def test_no_gender_policy_rules(self):
        found = [value for value in FORBIDDEN_GENDER_POLICY_TERMS if value in self.lower]
        self.assertFalse(found, f"gender-policy terms found: {found}")

    def test_no_placeholders_or_unresolved_questions(self):
        self.assertNotRegex(self.prompt, r"(?im)\b(?:TBD|TODO|FIXME)\b")
        self.assertNotIn("[NEEDS CLARIFICATION", self.prompt)


if __name__ == "__main__":
    unittest.main()
