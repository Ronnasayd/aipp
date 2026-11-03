"""Batch-lint regression suite for hooks/scripts.

Fake tools are scripts that append their argv to a log and print canned output
(design.md Test Strategy). Each test runs in a temp git repo; the fake bin dir
is prepended to PATH so the real toolchain is never invoked.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error

HOOKS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(HOOKS_DIR))

import utils  # noqa: E402

LOG = logging.getLogger("test_lint_changed")


@dataclass(frozen=True)
class Fake:
    """Canned behaviour of one fake tool.

    `report` is jscpd JSON written into the `--output` dir; others leave it unset.
    """

    stdout: str = ""
    stderr: str = ""
    code: int = 0
    sleep: float = 0.0
    report: str | None = None


def _fake_script(log: Path, name: str, spec: Fake) -> str:
    # why: jscpd writes its report into the --output dir; other fakes never do
    report_block = ""
    if spec.report is not None:
        report_block = (
            "_args = sys.argv[1:]\n"
            "_out = _args[_args.index('--output') + 1]\n"
            "os.makedirs(_out, exist_ok=True)\n"
            "_path = os.path.join(_out, 'jscpd-report.json')\n"
            f"open(_path, 'w').write({spec.report!r})\n"
        )
    return (
        f"#!{sys.executable}\n"
        "import json, os, sys, time\n"
        f"with open({str(log)!r}, 'a') as _fh:\n"
        f"    _entry = {{'tool': {name!r}, 'argv': sys.argv[1:]}}\n"
        "    _fh.write(json.dumps(_entry) + '\\n')\n"
        f"{report_block}"
        f"time.sleep({spec.sleep!r})\n"
        f"sys.stdout.write({spec.stdout!r})\n"
        f"sys.stderr.write({spec.stderr!r})\n"
        f"sys.exit({spec.code!r})\n"
    )


class FakeRepo:
    """Temp git repo plus a bin dir of fake tools that logs every invocation."""

    def __init__(self, root: Path, bin_dir: Path, log: Path) -> None:
        self.root = root
        self.bin_dir = bin_dir
        self.log = log

    def write(self, rel: str, text: str = "") -> Path:
        """Write a file under the repo root, creating parent dirs.

        Args:
            rel: Path relative to the repo root.
            text: File content.

        Returns:
            Path: The written file.
        """
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def fake(self, name: str, spec: Fake = Fake(), dest: Path | None = None) -> Path:  # noqa: B008 - Fake is frozen
        """Install an executable fake tool that logs its argv.

        Args:
            name: Executable name.
            spec: Canned output and exit code.
            dest: Directory to install into; defaults to the PATH bin dir.

        Returns:
            Path: The installed script.
        """
        path = (dest or self.bin_dir) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_fake_script(self.log, name, spec), encoding="utf-8")
        path.chmod(0o755)
        return path

    def calls(self, tool: str) -> list[list[str]]:
        """Return the argv of every logged invocation of `tool`, in call order.

        Args:
            tool: Fake executable name.

        Returns:
            list[list[str]]: One argv list per call.
        """
        if not self.log.exists():
            return []
        entries = [
            json.loads(line) for line in self.log.read_text().splitlines() if line
        ]
        return [entry["argv"] for entry in entries if entry["tool"] == tool]

    def stage(self, *rels: str) -> None:
        """Stage the given paths so `git status --porcelain` lists them one by one.

        Args:
            *rels: Paths relative to the repo root.
        """
        subprocess.run(
            ["git", "add", "--", *rels], cwd=self.root, check=True, capture_output=True
        )

    def commit(self, message: str = "snapshot") -> None:
        subprocess.run(
            ["git", "add", "-A"], cwd=self.root, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-q", "--allow-empty", "-m", message],
            cwd=self.root,
            check=True,
            capture_output=True,
            env={
                **os.environ,
                "GIT_AUTHOR_NAME": "t",
                "GIT_AUTHOR_EMAIL": "t@t",
                "GIT_COMMITTER_NAME": "t",
                "GIT_COMMITTER_EMAIL": "t@t",
            },
        )


@pytest.fixture(autouse=True)
def _isolated_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # why: utils.tmp_project_dir writes jscpd reports under tempfile.gettempdir();
    # redirect it so tests never touch the real /tmp reports.
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(scratch))
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> FakeRepo:
    """Temp git repo with the fake bin dir first on PATH and cwd set to its root.

    Args:
        tmp_path: pytest temp dir.
        monkeypatch: pytest monkeypatch.

    Returns:
        FakeRepo: Helper bound to the new repo.
    """
    root = tmp_path / "repo"
    bin_dir = tmp_path / "bin"
    log = tmp_path / "calls.jsonl"
    root.mkdir()
    bin_dir.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=root, check=True, capture_output=True)
    fake = FakeRepo(root, bin_dir, log)
    fake.commit("init")
    monkeypatch.chdir(root)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    return fake


@dataclass
class TimeoutSpy:
    """Stand-in for run_command_cwd that records the timeout it receives."""

    timeouts: list[int] = field(default_factory=list)

    def __call__(self, cmd: str, cwd: str | None = None, timeout: int = 30) -> dict:
        """Record `timeout` and report an empty success.

        Args:
            cmd: Ignored command line.
            cwd: Ignored working directory.
            timeout: Timeout the caller passed (30 when it passed none).

        Returns:
            dict: A successful, empty command result.
        """
        self.timeouts.append(timeout)
        return {"success": True, "output": "", "error": ""}


def _jscpd_report(*pairs: tuple[str, str]) -> str:
    """Build a jscpd JSON report with one 20-line duplicate per pair.

    Args:
        *pairs: (first, second) relative file names.

    Returns:
        str: The report JSON.
    """
    return json.dumps(
        {
            "duplicates": [
                {
                    "firstFile": {"name": a, "start": 1, "end": 20},
                    "secondFile": {"name": b, "start": 30, "end": 49},
                    "lines": 20,
                }
                for a, b in pairs
            ]
        }
    )


def test_jscpd_keeps_pairs_touching_set(repo: FakeRepo) -> None:
    changed = [
        repo.write("a.py", "x = 1\n").resolve(),
        repo.write("b.py", "y = 1\n").resolve(),
    ]
    repo.fake(
        "npx",
        Fake(
            code=1,
            report=_jscpd_report(("a.py", "c.py"), ("d.py", "b.py"), ("e.py", "f.py")),
        ),
    )

    result = utils.run_jscpd(changed, str(repo.root), LOG, "T")

    assert result["success"] is False
    pairs = {(d["firstFile"], d["secondFile"]) for d in result["output"]["duplicates"]}
    assert pairs == {("a.py:1-20", "c.py:30-49"), ("d.py:1-20", "b.py:30-49")}


def test_jscpd_unrelated_pairs_pass(repo: FakeRepo) -> None:
    changed = [repo.write("a.py", "x = 1\n").resolve()]
    repo.fake("npx", Fake(code=1, report=_jscpd_report(("d.py", "e.py"))))

    result = utils.run_jscpd(changed, str(repo.root), LOG, "T")

    assert result["success"] is True
    assert result["output"] == ""


def test_jscpd_timeout_300(repo: FakeRepo, monkeypatch: pytest.MonkeyPatch) -> None:
    spy = TimeoutSpy()
    monkeypatch.setattr(utils, "run_command_cwd", spy)

    utils.run_jscpd([repo.write("a.py").resolve()], str(repo.root), LOG, "T")

    assert spy.timeouts == [300]
