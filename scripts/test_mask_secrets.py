"""Tests for scripts/mask-secrets."""

from pathlib import Path
import subprocess

SCRIPT = Path(__file__).parent / "mask-secrets"


def _mask(text: str) -> str:
    return subprocess.run(
        [str(SCRIPT)], input=text, capture_output=True, text=True, check=True
    ).stdout


def test_masks_secrets_and_keeps_plain_text():
    aws = "AKIA" + "IOSFODNN7EXAMPLE"
    out = _mask(f'hello world\nAWS_KEY={aws}\npassword = "hunter2abcXYZ"\n')
    assert aws not in out
    assert "hunter2abcXYZ" not in out
    assert "hello world\n" in out
    assert out.count("[REDACTED]") == 2


def test_passthrough_without_secrets():
    text = "nada aqui\nlinha 2\n"
    assert _mask(text) == text


def test_masks_whole_token_when_detector_reports_only_prefix():
    token = "ghp_" + "abcdefghijklmnopqrstuvwxyz0123456789"
    assert _mask(f"GITHUB_TOKEN={token}\n") == "GITHUB_TOKEN=[REDACTED]\n"


def test_masks_whole_pem_private_key_block():
    kind = "RSA " + "PRIVATE KEY"
    body = "MIIEpAIBAAKCAQEA1b2c3d4e5f6g7h8\nZmFrZWtleWJvZHlsaW5lMmZha2VrZXk=\n"
    pem = f"-----BEGIN {kind}-----\n{body}-----END {kind}-----"
    assert _mask(f"before\n{pem}\nafter\n") == "before\n[REDACTED]\nafter\n"
