#!/bin/sh
# Remove the MagicPods menu from Steam's VR UI. Stopping the service removes the
# menu from Steam's pages; MagicPodsCore and its settings are left alone.
set -u
units="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
systemctl --user disable --now magicpods-steamui.service 2>/dev/null
rm -f "$units/magicpods-steamui.service"
systemctl --user daemon-reload
rm -rf "$HOME/.local/share/magicpods-app/frame"
echo "MagicPods menu removed."
