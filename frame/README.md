# MagicPods menu for Steam's VR UI

For ARM64 SteamOS headsets (Steam Frame). Adds, inside Steam's own VR interface:

- an earbuds battery indicator in the top bar, next to the headset battery;
- a **MagicPods** tab in the quick-access popup (the one the headset battery opens),
  with the same menus as the MagicPods Decky plugin: battery, noise control, ear
  detection, all headphone options, paired devices and Bluetooth, and settings;
- an earbuds row under **Battery Info**.

Clicking the top-bar indicator or the Battery Info row opens the MagicPods tab.

It needs MagicPodsCore running as the same user (`magicpodscore.service`, see the
MagicPodsCore `docs/FRAME.md`). The menu talks to it directly on
`ws://127.0.0.1:2020`; no other program or window is involved.

## Install / remove

    ./frame/install.sh      # copies to ~/.local/share/magicpods-app/frame, enables magicpods-steamui.service
    ~/.local/share/magicpods-app/frame/uninstall.sh

## How it works, and its limits

`magicpods-steamui.py` checks every 3 seconds that Steam's VR bar and quick-access
pages run the current `magicpods-menu.js`, using Steam's local DevTools endpoint
(127.0.0.1:8080, available because Steam runs with `-cef-enable-debugging`). This is the
mechanism Decky Loader uses. It only ever sends that one fixed script, and stopping the
service removes everything it added.

This is unofficial. A Steam update can change these pages; the menu then does not
appear until the script is updated, and nothing else is affected. Menu preferences
(displayed noise modes, low-battery level) are kept in Steam's browser storage.

Steam's DevTools endpoint is unauthenticated and, in developer mode, is also forwarded
to the network on port 8081. That is Steam's setting, not this tool's; turn developer
mode off when you do not need it.
