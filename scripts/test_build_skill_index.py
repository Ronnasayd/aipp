"""Tests for scripts/build-skill-index.py manifest generation."""

import importlib.util
from pathlib import Path
import sys
import types

import pytest

SCRIPT = Path(__file__).with_name("build-skill-index.py")


@pytest.fixture(name="module")
def fixture_module(monkeypatch: pytest.MonkeyPatch) -> types.ModuleType:
    """Load build-skill-index.py with fastembed stubbed out.

    Args:
        monkeypatch: pytest fixture used to stub the fastembed module.

    Returns:
        types.ModuleType: The loaded build-skill-index module.
    """
    # why: fastembed is heavy and unused by build_manifest.
    monkeypatch.setitem(
        sys.modules, "fastembed", types.SimpleNamespace(TextEmbedding=object)
    )
    spec = importlib.util.spec_from_file_location("build_skill_index", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_build_manifest_skips_bytecode(
    module: types.ModuleType, tmp_path: Path
) -> None:
    """Manifest must not list __pycache__ dirs or .pyc files.

    Args:
        module: The loaded build-skill-index module.
        tmp_path: pytest temporary directory holding a fake skill tree.
    """
    skill = tmp_path / "demo"
    (skill / "scripts" / "__pycache__").mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: demo\n---\n", encoding="utf-8")
    (skill / "scripts" / "run.py").write_text("", encoding="utf-8")
    (skill / "scripts" / "__pycache__" / "run.cpython-312.pyc").write_bytes(b"")
    (skill / "scripts" / "stray.pyc").write_bytes(b"")

    manifest = module.build_manifest(tmp_path)

    assert manifest["demo"]["files"] == ["scripts/run.py"]
