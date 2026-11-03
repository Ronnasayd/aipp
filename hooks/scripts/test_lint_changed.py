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
from typing import TYPE_CHECKING

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error

# pylint: disable=protected-access

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import ModuleType

HOOKS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(HOOKS_DIR))

import golang_lint  # noqa: E402
import php_lint  # noqa: E402
import python_lint  # noqa: E402
import typescript_lint  # noqa: E402
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


def _success(result: dict, key: str) -> bool | None:
    """Return the `success` flag of one tool result, None when it did not run.

    Args:
        result: Dict returned by a `maybe_run_*` dispatcher.
        key: Tool result key.

    Returns:
        bool | None: The tool's success flag, or None for an unrun tool.
    """
    entry = result[key]
    return None if entry is None else entry["success"]


def _field(result: dict, key: str, name: str) -> object:
    """Return one field of one tool result.

    Args:
        result: Dict returned by a `maybe_run_*` dispatcher.
        key: Tool result key.
        name: Field of the tool result (`success`, `output`, `error`, `installed`).

    Returns:
        object: The field value.
    """
    return result[key][name]


def _dup_firsts(result: dict, key: str) -> list[str]:
    """Return `firstFile` of every duplicate pair reported under `key`.

    Args:
        result: Dict returned by a `maybe_run_*` dispatcher.
        key: Tool result key holding a jscpd result.

    Returns:
        list[str]: `name:start-end` of each pair's first file.
    """
    return [d["firstFile"] for d in result[key]["output"]["duplicates"]]


def test_single_file_mode_keys(repo: FakeRepo) -> None:
    target = repo.write("a.py", "import os\n")
    repo.fake("mypy")
    repo.fake("ruff", Fake(stdout='[{"code": "F401"}]', code=1))
    repo.fake("pylint")
    report = _jscpd_report(("a.py", "z.py"), ("x.py", "y.py"))
    repo.fake("npx", Fake(code=1, report=report))

    result = python_lint.maybe_run_python_lint([str(target)])

    assert set(result) == {"mypy", "ruff", "pylint", "jscpd"}
    assert _success(result, "ruff") is False
    assert _success(result, "mypy") is True
    assert _success(result, "pylint") is True
    assert [call[0] for call in repo.calls("npx")] == ["jscpd"]
    assert _success(result, "jscpd") is False
    assert _dup_firsts(result, "jscpd") == ["a.py:1-20"]


DISPATCHERS = [
    (python_lint.maybe_run_python_lint, {"mypy", "ruff", "pylint", "jscpd"}),
    (typescript_lint.maybe_run_typescript_lint, {"typescript", "eslint", "jscpd"}),
    (golang_lint.maybe_run_golang_lint, {"govet", "golangci_lint", "gofmt", "jscpd"}),
    (php_lint.maybe_run_php_lint, {"phpstan", "jscpd"}),
]


@pytest.mark.parametrize(
    ("maybe_run", "keys"), DISPATCHERS, ids=["python", "typescript", "go", "php"]
)
def test_maybe_run_empty_list_no_tools(
    repo: FakeRepo, maybe_run: Callable[..., dict], keys: set[str]
) -> None:
    result = maybe_run([])

    assert set(result) == keys
    assert all(entry is None for entry in result.values())
    assert not repo.log.exists()


@dataclass(frozen=True)
class Lang:
    """One language module under test and how to fake its tools."""

    id: str
    module: ModuleType
    maybe_run: Callable[..., dict]
    filename: str
    tools: tuple[str, ...]
    install: Callable[[FakeRepo], None]


def _install_python(repo: FakeRepo) -> None:
    for tool in ("mypy", "ruff", "pylint"):
        repo.fake(tool)


def _install_typescript(repo: FakeRepo) -> None:
    bin_dir = repo.root / "node_modules" / ".bin"
    for tool in ("tsc-files", "eslint"):
        repo.fake(tool, dest=bin_dir)


def _install_php(repo: FakeRepo) -> None:
    repo.fake("phpstan", dest=repo.root / "vendor" / "bin")


def _install_go(repo: FakeRepo) -> None:
    for tool in ("go", "golangci-lint", "gofmt"):
        repo.fake(tool)


LANGS = [
    Lang(
        "python",
        python_lint,
        python_lint.maybe_run_python_lint,
        "a b.py",
        ("mypy", "ruff", "pylint"),
        _install_python,
    ),
    Lang(
        "typescript",
        typescript_lint,
        typescript_lint.maybe_run_typescript_lint,
        "a b.ts",
        ("tsc-files", "eslint"),
        _install_typescript,
    ),
    Lang(
        "php",
        php_lint,
        php_lint.maybe_run_php_lint,
        "a b.php",
        ("phpstan",),
        _install_php,
    ),
    Lang(
        "go",
        golang_lint,
        golang_lint.maybe_run_golang_lint,
        "a b.go",
        ("gofmt",),
        _install_go,
    ),
]


def _py_files(repo: FakeRepo, *names: str) -> list[str]:
    """Create small Python files under the repo root.

    Args:
        repo: Repo to write into.
        *names: File names relative to the repo root.

    Returns:
        list[str]: Resolved path of each file, in the given order.
    """
    return [str(repo.write(name, "x = 1\n").resolve()) for name in names]


def test_python_tools_called_once_with_all_files(repo: FakeRepo) -> None:
    files = _py_files(repo, "a.py", "b.py", "c.py")
    _install_python(repo)

    python_lint.maybe_run_python_lint(files, jscpd=False)

    for tool in ("mypy", "ruff", "pylint"):
        calls = repo.calls(tool)
        assert len(calls) == 1
        assert calls[0][-3:] == files


def test_crash_reports_raw_output(repo: FakeRepo) -> None:
    files = _py_files(repo, "a.py")
    _install_python(repo)
    repo.fake("ruff", Fake(stdout="Traceback boom", stderr="fatal crash", code=2))

    result = python_lint.maybe_run_python_lint(files, jscpd=False)

    assert _field(result, "ruff", "success") is False
    assert _field(result, "ruff", "output") == "Traceback boom"
    assert _field(result, "ruff", "error") == "fatal crash"


def test_missing_path_excluded(repo: FakeRepo) -> None:
    files = _py_files(repo, "a.py")
    gone = str(repo.root / "gone.py")
    _install_python(repo)

    python_lint.maybe_run_python_lint([gone, *files], jscpd=False)

    for tool in ("mypy", "ruff", "pylint"):
        assert gone not in repo.calls(tool)[0]
        assert files[0] in repo.calls(tool)[0]


def test_missing_tool_passes(repo: FakeRepo, monkeypatch: pytest.MonkeyPatch) -> None:
    files = _py_files(repo, "a.py")
    _install_python(repo)
    monkeypatch.setattr(python_lint, "_check_tool_installed", lambda *_: False)

    result = python_lint.maybe_run_python_lint(files, jscpd=False)

    for tool in ("mypy", "ruff", "pylint"):
        assert _field(result, tool, "success") is True
        assert _field(result, tool, "installed") is False
        assert repo.calls(tool) == []


@pytest.mark.parametrize("lang", LANGS, ids=lambda lang: lang.id)
def test_lint_exec_timeout_300(
    repo: FakeRepo, monkeypatch: pytest.MonkeyPatch, lang: Lang
) -> None:
    spy = TimeoutSpy()
    monkeypatch.setattr(lang.module, "run_command_cwd", spy)

    lang.module._exec("tool", ["arg"], cwd=str(repo.root))

    assert spy.timeouts == [300]


@pytest.mark.parametrize("lang", LANGS, ids=lambda lang: lang.id)
def test_path_with_space_single_arg(repo: FakeRepo, lang: Lang) -> None:
    path = str(repo.write(f"my dir/{lang.filename}", "x\n").resolve())
    lang.install(repo)

    lang.maybe_run([path], jscpd=False)

    for tool in lang.tools:
        assert path in repo.calls(tool)[0]


def test_timeout_reported_no_retry(
    repo: FakeRepo, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = _py_files(repo, "a.py")
    _install_python(repo)
    repo.fake("ruff", Fake(sleep=3))
    monkeypatch.setattr(python_lint, "LINT_TIMEOUT_S", 1)

    result = python_lint.maybe_run_python_lint(files, jscpd=False)

    assert _field(result, "ruff", "success") is False
    assert "timed out" in str(_field(result, "ruff", "error"))
    assert len(repo.calls("ruff")) == 1


def test_typescript_tools_called_once(repo: FakeRepo) -> None:
    files = [str(repo.write(f"{n}.ts", "export {};\n").resolve()) for n in "ab"]
    _install_typescript(repo)

    typescript_lint.maybe_run_typescript_lint(files, jscpd=False)

    for tool in ("tsc-files", "eslint"):
        calls = repo.calls(tool)
        assert len(calls) == 1
        assert calls[0][-2:] == files


def test_phpstan_called_once(repo: FakeRepo) -> None:
    files = [str(repo.write(f"{n}.php", "<?php\n").resolve()) for n in "ab"]
    _install_php(repo)

    php_lint.maybe_run_php_lint(files, jscpd=False)

    calls = repo.calls("phpstan")
    assert len(calls) == 1
    assert calls[0][-2:] == files


GOLANGCI_RUN = ["run", "--output.json.path", "stdout"]


def _go_files(repo: FakeRepo, *rels: str) -> list[str]:
    """Create small Go files under the repo root.

    Args:
        repo: Repo to write into.
        *rels: File paths relative to the repo root.

    Returns:
        list[str]: Resolved path of each file, in the given order.
    """
    return [str(repo.write(rel, "package p\n").resolve()) for rel in rels]


def _issue_files(result: dict, key: str) -> list[str]:
    """Return the `Pos.Filename` of every golangci-lint issue under `key`.

    Args:
        result: Dict returned by `maybe_run_golang_lint`.
        key: Tool result key holding a golangci-lint result.

    Returns:
        list[str]: Reported file names, in report order.
    """
    return [issue["Pos"]["Filename"] for issue in result[key]["output"]["Issues"]]


def test_gofmt_called_once(repo: FakeRepo) -> None:
    files = _go_files(repo, "pkg/a.go", "pkg/b.go")
    _install_go(repo)

    golang_lint.maybe_run_golang_lint(files, jscpd=False)

    assert repo.calls("gofmt") == [["-l", *files]]


def test_go_packages_deduplicated(repo: FakeRepo) -> None:
    files = _go_files(repo, "pkg1/a.go", "pkg1/b.go", "pkg2/c.go")
    _install_go(repo)

    golang_lint.maybe_run_golang_lint(files, jscpd=False)

    assert repo.calls("go") == [["vet", "./pkg1", "./pkg2"]]
    assert repo.calls("golangci-lint") == [[*GOLANGCI_RUN, "./pkg1", "./pkg2"]]


def test_go_issues_filtered_to_changed(repo: FakeRepo) -> None:
    files = _go_files(repo, "pkg/a.go")
    _go_files(repo, "pkg/xa.go", "pkg/b.go")
    vet_stderr = (
        "# example/pkg\n./pkg/a.go:3:1: bad a\npkg/xa.go:4:2: bad xa\n"
        "pkg/b.go:1:1: bad b\n"
    )
    issues = {
        "Issues": [
            {"Pos": {"Filename": name}, "Text": "bad"}
            for name in ("./pkg/a.go", "pkg/xa.go", "pkg/b.go")
        ]
    }
    repo.fake("go", Fake(stderr=vet_stderr, code=1))
    repo.fake("golangci-lint", Fake(stdout=json.dumps(issues), code=1))
    repo.fake("gofmt")

    result = golang_lint.maybe_run_golang_lint(files, jscpd=False)

    assert _field(result, "govet", "success") is False
    assert _field(result, "govet", "error") == "./pkg/a.go:3:1: bad a"
    assert _field(result, "golangci_lint", "success") is False
    assert _issue_files(result, "golangci_lint") == ["./pkg/a.go"]


def test_go_generated_excluded(repo: FakeRepo) -> None:
    marker = "// Code generated by go-bindata. DO NOT EDIT.\npackage gen\n"
    generated = str(repo.write("gen/data.go", marker).resolve())
    files = _go_files(repo, "pkg/a.go")
    _install_go(repo)

    golang_lint.maybe_run_golang_lint([generated, *files], jscpd=False)

    assert repo.calls("gofmt") == [["-l", *files]]
    assert repo.calls("go") == [["vet", "./pkg"]]
    assert repo.calls("golangci-lint") == [[*GOLANGCI_RUN, "./pkg"]]
