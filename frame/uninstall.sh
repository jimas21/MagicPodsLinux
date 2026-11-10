#!/bin/sh
# Remove the MagicPods menu from Steam's VR UI. MagicPodsCore and its settings are left alone.
set -u
dest="$HOME/.local/share/magicpods-app/frame"
units="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"

# Stopping the service removes the menu from Steam's pages; --teardown covers the case
# where the service was not running.
systemctl --user disable --now magicpods-steamui.service 2>/dev/null
if [ -f "$dest/magicpods-steamui.py" ]; then
    python3 -I "$dest/magicpods-steamui.py" --teardown 2>/dev/null
fi
rm -f "$units/magicpods-steamui.service"
systemctl --user daemon-reload
rm -rf "$dest"
rmdir "$HOME/.local/share/magicpods-app" 2>/dev/null
echo "MagicPods menu removed."
