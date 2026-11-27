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
