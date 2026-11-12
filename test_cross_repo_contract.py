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
        self.awa.joinpath("mcp", "docs", "interfaces").mkdir(parents=True)
        self.awa.joinpath("mcp", "workspace").mkdir(parents=True)
        self.awa.joinpath("AGENTS.md").write_text("# Agent\n")
        self.awa.joinpath("mcp", "workspace", "contract.md").write_text("# Workspace\n")
        self.awa.joinpath("mcp", "README.md").write_text(
            "awa-si/admin/core.yaml; AWA MCP never loads Admin project instructions.\n")
        self._write("mcp/tools/model.py", '''
SOURCE_REGISTRY = {
    "mcp": {"path": "mcp/README.md", "summary": "MCP gateway overview",
            "read_when": "When discovering MCP sources"},
    "workspace": {"path": "mcp/workspace/contract.md", "tool": "workspace_exec",
                  "summary": "Workspace technical contract",
                  "read_when": "Before workspace operations"},
}
''')
        self._write("mcp/instructions.py", '''
from .tools.model import SOURCE_REGISTRY, source_registry_fingerprint
class InstructionResolver:
    LOCAL_SOURCES = {topic: spec["path"] for topic, spec in SOURCE_REGISTRY.items()}
''')
        self._write("mcp/tools/instruction_tools.py", '''
async def mcp_instructions(topic=None, compact=False):
    return {}
''')
        self._write("mcp/tools/model_tools.py", '''
from .model import source_registry_fingerprint, technical_source_for_tool
_KNOWLEDGE_SOURCES = {"instructions": {"boundary": "ChatGPT_loads_Admin_and_project_rules_outside_MCP"}}
async def mcp_model(operation="schema"):
    return {}
''')
        self._write("mcp/docs/interfaces/browser.md", """
# Browser interface

## Browser vision

<!-- BEGIN GENERATED INTERFACE REFERENCE -->
## Adapter reference
<!-- END GENERATED INTERFACE REFERENCE -->
""")
        self._write("mcp/docs/tools/mcp_instructions.md", '''
| Argument | Required |
| --- | --- |
| topic | no |
| compact | no |

<!-- BEGIN MAINTAINED KNOWLEDGE CONTRACT -->
## MCP Knowledge Plane — maintained contract
<!-- END MAINTAINED KNOWLEDGE CONTRACT -->
''')
        self.admin = Path(__file__).resolve().parent

    def _write(self, path: str, content: str) -> None:
        self.awa.joinpath(path).write_text(content, encoding="utf-8")

    def test_matching_contract(self) -> None:
        result = check_contract(self.admin, self.awa)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["technical_topics"], ["mcp", "workspace"])

    def test_missing_source_guidance_fails(self) -> None:
        model = self.awa / "mcp/tools/model.py"
        model.write_text(model.read_text().replace(
            '"summary": "MCP gateway overview",', ""
        ), encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "invalid technical source fields"):
            check_contract(self.admin, self.awa)

    def test_unknown_registry_key_fails(self) -> None:
        model = self.awa / "mcp/tools/model.py"
        model.write_text(model.read_text().replace(
            '"read_when": "When discovering MCP sources"',
            '"read_when": "When discovering MCP sources", "allow": True'
        ), encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "invalid technical source fields"):
            check_contract(self.admin, self.awa)

    def test_missing_shared_registry_fails(self) -> None:
        self._write("mcp/instructions.py", "class InstructionResolver: pass\n")
        with self.assertRaisesRegex(ContractError, "not bound"):
            check_contract(self.admin, self.awa)

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

    def test_missing_knowledge_contract_section_fails(self) -> None:
        self._write("mcp/docs/tools/mcp_instructions.md", "| topic | no |\n| compact | no |\n")
        with self.assertRaisesRegex(ContractError, "Knowledge canonical document markers"):
            check_contract(self.admin, self.awa)

    def test_retired_knowledge_copy_fails(self) -> None:
        self._write("mcp/docs/knowledge.md", "# obsolete copy\n")
        with self.assertRaisesRegex(ContractError, "retired Knowledge contract path"):
            check_contract(self.admin, self.awa)

    def test_missing_browser_contract_fails(self) -> None:
        self.awa.joinpath("mcp/docs/interfaces/browser.md").unlink()
        with self.assertRaisesRegex(ContractError, "Browser canonical document markers"):
            check_contract(self.admin, self.awa)

    def test_retired_browser_vision_copy_fails(self) -> None:
        self._write("mcp/docs/browser-vision.md", "# obsolete copy\n")
        with self.assertRaisesRegex(ContractError, "retired Browser Vision path"):
            check_contract(self.admin, self.awa)

    def test_docs_schema_drift_fails(self) -> None:
        with self.awa.joinpath("mcp", "docs", "tools", "mcp_instructions.md").open("a") as file:
            file.write("| ref | no |\n")
        with self.assertRaisesRegex(ContractError, "obsolete argument"):
            check_contract(self.admin, self.awa)


if __name__ == "__main__":
    unittest.main()
