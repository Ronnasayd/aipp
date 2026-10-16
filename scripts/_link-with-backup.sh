# Shared helper: symlink <dst> -> <src> without losing a regular file at <dst>.
# A regular file is moved to <dst>.bak (overwriting an older .bak); symlinks
# hold no user data and are replaced; a directory is refused.
# Source this file; do not execute it.

link_with_backup() {
  local src="$1" dst="$2"
  if [ -d "$dst" ] && [ ! -L "$dst" ]; then
    echo "link_with_backup: $dst is a directory, not touching it" >&2
    return 1
  fi
  mkdir -p "$(dirname "$dst")"
  # invariant: -L is tested before -f; -f follows symlinks and would back up the link target
  if [ -L "$dst" ]; then
    rm -f "$dst"
  elif [ -f "$dst" ]; then
    mv -f "$dst" "$dst.bak"
    echo "backup: $dst -> $dst.bak"
  fi
  # invariant: mv runs before ln, so an ln failure still leaves the original at $dst.bak
  ln -s "$src" "$dst"
}
