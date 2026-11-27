"""Tests for gghget in scripts/update-external-tools.sh (mirror of an upstream dir)."""

import hashlib
import json
from pathlib import Path
import subprocess

SCRIPT = Path(__file__).parent / "update-external-tools.sh"
URL = "https://github.com/o/r/tree/main/skills/demo"


def _blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _gghget(out_dir: Path, response: str, http_code: int = 200):
    # why: curl and the scanner are stubbed so the test never reaches the network or uv
    stub = (
        'source "$1"; '
        'curl() { printf "%s\\n%s" "$FAKE_BODY" "$FAKE_CODE"; }; '
        "_scan_skill_dir() { :; }; "
        'gghget "$2" "$3"'
    )
    return subprocess.run(
        ["bash", "-c", stub, "test", str(SCRIPT), URL, str(out_dir)],
        capture_output=True,
        text=True,
        check=False,
        env={
            "PATH": "/usr/bin:/bin",
            "FAKE_BODY": response,
            "FAKE_CODE": str(http_code),
        },
    )


def _tree(tmp_path: Path) -> tuple[Path, str]:
    out = tmp_path / "skill"
    (out / "olddir").mkdir(parents=True)
    (out / "olddir" / "x.md").write_text("old", encoding="utf-8")
    (out / "__pycache__").mkdir()
    (out / "__pycache__" / "keep.cpython-312.pyc").write_bytes(b"pyc")
    (out / "keep.py").write_bytes(b"keep\n")
    (out / "orphan.py").write_bytes(b"orphan\n")
    listing = json.dumps(
        [
            {
                "type": "file",
                "name": "keep.py",
                "download_url": "",
                "sha": _blob_sha(b"keep\n"),
            }
        ]
    )
    return out, listing


def test_files_removed_upstream_are_deleted_locally(tmp_path):
    out, listing = _tree(tmp_path)
    result = _gghget(out, listing)
    assert result.returncode == 0, result.stderr
    assert (out / "keep.py").exists()
    assert not (out / "orphan.py").exists()
    assert not (out / "olddir").exists()


def test_pycache_is_never_pruned(tmp_path):
    out, listing = _tree(tmp_path)
    _gghget(out, listing)
    assert (out / "__pycache__" / "keep.cpython-312.pyc").exists()


def test_api_error_deletes_nothing(tmp_path):
    out, _ = _tree(tmp_path)
    _gghget(out, '{"message": "rate limited"}', http_code=403)
    assert (out / "orphan.py").exists()
    assert (out / "olddir" / "x.md").exists()


def test_unparseable_listing_deletes_nothing(tmp_path):
    out, _ = _tree(tmp_path)
    _gghget(out, "not json")
    assert (out / "orphan.py").exists()
    assert (out / "keep.py").exists()


def _scan(cwd: Path, skill_dir: str, exit_code: int):
    # why: uv is stubbed to write a fake --output report so the scan never runs for real
    stub = (
        'source "$1"; '
        "uv() { while [[ $# -gt 0 ]]; do "
        '[[ "$1" == --output ]] && echo "FAKE REPORT" > "$2"; shift; done; '
        'return "$FAKE_EXIT"; }; '
        '_scan_skill_dir "$2"'
    )
    return subprocess.run(
        ["bash", "-c", stub, "test", str(SCRIPT), skill_dir],
        capture_output=True,
        text=True,
        check=False,
        cwd=cwd,
        env={"PATH": "/usr/bin:/bin", "FAKE_EXIT": str(exit_code)},
    )


def test_quarantined_skill_carries_skillspector_report(tmp_path):
    (tmp_path / "skills/vendor/demo").mkdir(parents=True)
    (tmp_path / "skills/vendor/demo/SKILL.md").write_text("x", encoding="utf-8")
    _scan(tmp_path, "skills/vendor/demo", exit_code=1)
    quarantined = tmp_path / "skills/.quarantine/skills/vendor/demo"
    assert (quarantined / "SKILL.md").exists()
    assert (quarantined / "SKILLSPECTOR_REPORT.md").read_text() == "FAKE REPORT\n"


def test_clean_scan_leaves_no_report(tmp_path):
    (tmp_path / "skills/vendor/demo").mkdir(parents=True)
    _scan(tmp_path, "skills/vendor/demo", exit_code=0)
    assert not (tmp_path / "skills/vendor/demo/SKILLSPECTOR_REPORT.md").exists()
    assert not (tmp_path / "skills/.quarantine").exists()
