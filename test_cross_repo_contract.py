"""Offline regression coverage for revision-bound Admin↔MCP contract checks."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cross_repo_contract import ContractError, check_contract


class CrossRepoContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.awa = Path(self.temp.name) / "awa"
        self.awa.joinpath("mcp", "tools").mkdir(parents=True)
        self.awa.joinpath("mcp", "docs", "tools").mkdir(parents=True)
        self.awa.joinpath("mcp", "workspace").mkdir(parents=True)
        self.awa.joinpath("AGENTS.md").write_text("# Agent\n")
        self.awa.joinpath("mcp", "workspace", "contract.md").write_text("# Workspace\n")
        self.awa.joinpath("mcp", "README.md").write_text(
            "awa-si/admin/core.yaml; AWA MCP never loads Admin project instructions.\n")
        self._write("mcp/instructions.py", '''
class InstructionSource:
    pass
class InstructionResolver:
    AWA_REPOSITORY = "awa-si/awa"
    LOCAL_SOURCES: dict = {
        "mcp": InstructionSource(AWA_REPOSITORY, "mcp/README.md", "local"),
        "workspace": InstructionSource(AWA_REPOSITORY, "mcp/workspace/contract.md", "local"),
    }
''')
        self._write("mcp/tools/instruction_tools.py", '''
async def mcp_instructions(topic=None, compact=False):
    return {}
''')
        self._write("mcp/tools/model_tools.py", '''
_KNOWLEDGE_SOURCES = {"instructions": {"boundary": "ChatGPT_loads_Admin_and_project_rules_outside_MCP"}}
async def mcp_model(operation="schema"):
    return {}
''')
        self._write("mcp/docs/tools/mcp_instructions.md", '''
| Argument | Required |
| --- | --- |
| topic | no |
| compact | no |
''')
        self.admin = Path(__file__).resolve().parent

    def _write(self, path: str, content: str) -> None:
        self.awa.joinpath(path).write_text(content, encoding="utf-8")

    def test_matching_contract(self) -> None:
        result = check_contract(self.admin, self.awa)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["technical_topics"], ["mcp", "workspace"])

    def test_obsolete_argument_fails(self) -> None:
        self._write("mcp/tools/instruction_tools.py", '''
async def mcp_instructions(topic=None, project=None, compact=False):
    return {}
''')
        with self.assertRaisesRegex(ContractError, "obsolete or altered"):
            check_contract(self.admin, self.awa)

    def test_missing_technical_source_fails(self) -> None:
        self.awa.joinpath("mcp", "workspace", "contract.md").unlink()
        with self.assertRaisesRegex(ContractError, "technical source missing"):
            check_contract(self.admin, self.awa)

    def test_docs_schema_drift_fails(self) -> None:
        with self.awa.joinpath("mcp", "docs", "tools", "mcp_instructions.md").open("a") as file:
            file.write("| ref | no |\n")
        with self.assertRaisesRegex(ContractError, "obsolete argument"):
            check_contract(self.admin, self.awa)


if __name__ == "__main__":
    unittest.main()
