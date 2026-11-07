# Troubleshooting

| Symptom                                                                        | Cause                                                                                      | Fix                                                  |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| Missing `.specs/features/{FEATURE}/checks.md`, or `validate_checks.py` red     | Feature never finished planning                                                            | Report it and stop -- run `sd-lean-planning` first   |
| `check_proofs.py` exits non-zero with `**Tree**: dirty` naming `docs/`         | A docs change was left uncommitted; only `.specs/` is exempt                               | Commit it, then run `check_proofs.py` again          |
| `validate_verification.py`: `proofs.md was written at <sha> and HEAD is <sha>` | A commit landed after the last `check_proofs.py`, even one touching only `.specs/` or docs | Run `check_proofs.py` again at `HEAD`, then the gate |
