"""Tests for scripts/_link-with-backup.sh (link_with_backup helper)."""

from pathlib import Path
import subprocess

HELPER = Path(__file__).parent / "_link-with-backup.sh"


def _link(src, dst):
    # invariant: paths go in as positional args, never interpolated, so spaces stay safe
    return subprocess.run(
        [
            "bash",
            "-c",
            'source "$0"; link_with_backup "$1" "$2"',
            str(HELPER),
            str(src),
            str(dst),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def _src(tmp_path, name="src.json"):
    src = tmp_path / name
    src.write_text("repo", encoding="utf-8")
    return src


def test_missing_dst_gets_symlink_without_backup(tmp_path):
    src, dst = _src(tmp_path), tmp_path / "dst.json"
    result = _link(src, dst)
    assert result.returncode == 0
    assert dst.readlink() == src
    assert not Path(f"{dst}.bak").exists()


def test_symlink_dst_is_replaced_without_backup(tmp_path):
    src, dst = _src(tmp_path), tmp_path / "dst.json"
    other = tmp_path / "other.json"
    other.write_text("other", encoding="utf-8")
    dst.symlink_to(other)
    assert _link(src, dst).returncode == 0
    assert dst.readlink() == src
    assert not Path(f"{dst}.bak").exists()


def test_dangling_symlink_dst_is_replaced_without_backup(tmp_path):
    src, dst = _src(tmp_path), tmp_path / "dst.json"
    dst.symlink_to(tmp_path / "gone.json")
    assert _link(src, dst).returncode == 0
    assert dst.readlink() == src
    assert not Path(f"{dst}.bak").exists()


def test_regular_file_dst_is_backed_up_then_linked(tmp_path):
    src, dst = _src(tmp_path), tmp_path / "dst.json"
    dst.write_text("user data", encoding="utf-8")
    assert _link(src, dst).returncode == 0
    assert Path(f"{dst}.bak").read_text(encoding="utf-8") == "user data"
    assert dst.readlink() == src


def test_existing_bak_is_overwritten_by_current_file(tmp_path):
    src, dst = _src(tmp_path), tmp_path / "dst.json"
    Path(f"{dst}.bak").write_text("old backup", encoding="utf-8")
    dst.write_text("current", encoding="utf-8")
    assert _link(src, dst).returncode == 0
    assert Path(f"{dst}.bak").read_text(encoding="utf-8") == "current"


def test_directory_dst_is_untouched_and_fails(tmp_path):
    src, dst = _src(tmp_path), tmp_path / "dst"
    dst.mkdir()
    (dst / "keep.txt").write_text("keep", encoding="utf-8")
    result = _link(src, dst)
    assert result.returncode == 1
    assert result.stderr != ""
    assert dst.is_dir() and not dst.is_symlink()
    assert (dst / "keep.txt").read_text(encoding="utf-8") == "keep"


def test_missing_parent_dir_is_created(tmp_path):
    src, dst = _src(tmp_path), tmp_path / "a" / "b" / "dst.json"
    assert _link(src, dst).returncode == 0
    assert dst.readlink() == src


def test_backup_prints_notice_line(tmp_path):
    src, dst = _src(tmp_path), tmp_path / "dst.json"
    dst.write_text("user data", encoding="utf-8")
    result = _link(src, dst)
    assert result.stdout.strip() == f"backup: {dst} -> {dst}.bak"


def test_paths_with_spaces(tmp_path):
    src = _src(tmp_path, "my src.json")
    dst = tmp_path / "my dir" / "my dst.json"
    dst.parent.mkdir()
    dst.write_text("user data", encoding="utf-8")
    assert _link(src, dst).returncode == 0
    assert Path(f"{dst}.bak").read_text(encoding="utf-8") == "user data"
    assert dst.readlink() == src


def test_second_call_leaves_bak_unchanged(tmp_path):
    src, dst = _src(tmp_path), tmp_path / "dst.json"
    dst.write_text("user data", encoding="utf-8")
    _link(src, dst)
    result = _link(src, dst)
    assert result.returncode == 0
    assert result.stdout == ""
    assert Path(f"{dst}.bak").read_text(encoding="utf-8") == "user data"
    assert dst.readlink() == src
