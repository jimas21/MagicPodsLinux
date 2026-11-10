#!/bin/sh
# Install the MagicPods menu for Steam's VR UI for the current user (no root).
# Run from the unpacked release directory: ./frame/install.sh
set -eu
src="$(cd "$(dirname "$0")" && pwd)"
dest="$HOME/.local/share/magicpods-app/frame"
units="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"

if ! systemctl --user cat magicpodscore.service >/dev/null 2>&1; then
    echo "warning: magicpodscore.service not found; install MagicPodsCore first" >&2
fi
mkdir -p "$dest" "$units"
if [ "$src" != "$dest" ]; then
    for f in magicpods-menu.js magicpods-steamui.py magicpods-steamui.service install.sh uninstall.sh README.md; do
        cp -f "$src/$f" "$dest/$f.new" && mv -f "$dest/$f.new" "$dest/$f"
    done
fi
chmod 755 "$dest/magicpods-steamui.py" "$dest/install.sh" "$dest/uninstall.sh"
cp -f "$dest/magicpods-steamui.service" "$units/"
systemctl --user daemon-reload
systemctl --user enable magicpods-steamui.service
systemctl --user restart magicpods-steamui.service
systemctl --user --no-pager status magicpods-steamui.service | grep -E "Active:"
