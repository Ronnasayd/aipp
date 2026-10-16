# Validation: readme-improvement - PASS (re-verified at HEAD 815e71f)

**Range**: 89212f7..HEAD (9 commits 4436e63..d2a7aff, branch feat/readme-improvement)
**Gate**: `uv run --with pytest pytest scripts/` -> 46 passed, 0 failed, exit 0 (14 in test_link_with_backup.py)
**Sensor**: 7 mutations in /tmp scratch, 7 killed, 0 survived. Real tree `git status --porcelain` identical to baseline (AGENTS.md, subagent-statusline.sh untouched).
(Scratch baseline lacked installer files so 4 installer-text tests fail in every mutant; kills counted above that baseline.)

| Mutation             | Killed by                                        |
| -------------------- | ------------------------------------------------ |
| swap -L/-f order     | symlink tests (+2)                               |
| drop mv (rm instead) | backup/overwrite/notice tests (+4)               |
| drop mkdir -p        | test_missing_parent_dir_is_created               |
| drop backup echo     | test_backup_prints_notice_line                   |
| dir return 1 -> 0    | test_directory_dst_is_untouched_and_fails        |
| unquote mv args      | test_paths_with_spaces                           |
| mv -f -> mv -n       | test_existing_bak_is_overwritten_by_current_file |

## P1 helper (scripts/test_link_with_backup.py)

| AC                       | Evidence                                                                                                                 | Result                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------ | -------------------------- |
| LINK-01 missing dst      | :32-37 `dst.readlink()==src`, `.bak` absent                                                                              | PASS                       |
| LINK-02 symlink/dangling | :40-47, :50-55 same asserts                                                                                              | PASS                       |
| LINK-03 regular file     | :58-63 `.bak` text=="user data", readlink==src                                                                           | PASS                       |
| LINK-04 old .bak         | :66-71 `.bak`=="current"                                                                                                 | PASS                       |
| LINK-05 dir              | :74-82 rc==1, stderr!="", dir+file intact                                                                                | PASS                       |
| LINK-06 parent           | :85-88 nested a/b created                                                                                                | PASS                       |
| LINK-07 message          | :91-95 stdout==`backup: {dst} -> {dst}.bak`                                                                              | PASS                       |
| LINK-08 call sites       | :132-153 text asserts helper call + no `rm` line with dst (claude, gemini, copilot x2); diff shows old rm blocks removed | PASS (text-level, no exec) |
| Edge: 2nd run            | :108-116 stdout=="" bak unchanged                                                                                        | PASS                       |
| Edge: spaces             | :98-105                                                                                                                  | PASS                       |
| FR-011 ln fail after mv  | helper `_link-with-backup.sh:19-20` mv precedes ln; code read only                                                       | PASS (read)                |

## P1 test command

- TEST-01: `git diff 89212f7..HEAD -- AGENTS.md` swaps `cd src && uv run pytest` for `uv run --with pytest pytest scripts/` - PASS
- TEST-02: gate above, 46 collected, exit 0 - PASS
- TEST-03: only the 1-line hunk committed; pending owner hunks still in working tree - PASS

## P2 reference tables

- REF-01/02: all 39 `|` rows of `git show 89212f7:README.md` found verbatim (11 in docs/environment.md, 28 in docs/external-tools.md); no extra table rows - PASS

## P2 README

- RE-VERIFY @815e71f: README.md:20-24 now `> [!WARNING]` blockquote, content unchanged (rc files, symlinks, `<path>.bak`, folder untouched); order, 10 flags, 7 aliases, links re-run: all OK; tree status unchanged. README-01/04 now PASS.
- (initial run) README-01 order: title, pitch, 2 badges, What's included, Requirements, warning, Quickstart, How it works, aliases, Uninstall, Directory, Reference - order PASS. BUT warning is a `## Warning:` heading, not a `> [!WARNING]` block (grep WARNING = 0) - **GAP (README-01/04 literal)**. Content of README-04 (rc files, symlink, `<path>.bak`) present at README.md "Warning" section - content PASS.
- README-02 no counts: none - PASS
- README-03: git, curl, uv, Node.js 24+, Claude CLI, "Tested on Linux. macOS support is partial" (paraphrase) - PASS
- README-05: stage 1 `bash install.sh`, stage 2 `aipp --claude`, flags table - PASS
- README-06: all 10 flags in install.sh case labels (install.sh:169-201, `--help|-h` :206) - PASS
- README-07: mif, mia, ats, ata, atr, lgh, aij all in .aipp.alias.zshrc (:66,:40,:32-34,:36,:52) - PASS
- README-08: scripted link check, 0 broken - PASS
- README-09: Uninstall states no .bak restore + `mv` example - PASS
- README-10: links CONTRIBUTING.md which documents the command - PASS

## P3 CONTRIBUTING

- CONTRIB-01 skill/agent frontmatter, 02 both index scripts + `mif` + "enter the catalog disabled", 03 hooks/scripts, claude/settings.json, hooks/README.md, /verify-hook, 04 test cmd + Conventional/no emoji/no AI/English, 05 links/paths resolve (scripted) - PASS. Note: skill path documented as `skills/<category>/<name>/SKILL.md` (matches real nested layout; spec text says `skills/<name>`). "disabled by default" claim not independently verified in code.

## Ranked gaps (resolved/updated at 815e71f)

0. Gap 1 below FIXED in 815e71f.

1. README.md has no `> [!WARNING]` blockquote (uses `## Warning` heading) - README-01/04 - README.md "Warning: what the installer changes"
2. LINK-08 verified by text match only; no executed fake-HOME installer run (spec Success Criterion 2) - tests/test_link_with_backup.py:122-129
3. CONTRIBUTING "new items enter disabled" unverified in code (minor)

4. Update: CONTRIB "new items enter disabled" VERIFIED by read: scripts/aipp_settings.py:316 `entry.setdefault(category, {}).setdefault(name, False)` (sync-catalog). Author fake-HOME claude installer smoke (symlink + byte-identical .bak, rc=0) reported by coordinator, not re-run by verifier.
