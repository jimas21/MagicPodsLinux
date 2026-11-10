# MagicPods menu for Steam's VR UI

For ARM64 SteamOS headsets (Steam Frame). Adds, inside Steam's own VR interface:

- an earbuds battery indicator in the top bar, next to the headset battery;
- a **MagicPods** tab in the quick-access popup (the one the headset battery opens),
  with the same menus as the MagicPods Decky plugin: battery, noise control, ear
  detection, all headphone options, paired devices and Bluetooth, and settings;
- an earbuds row under **Battery Info**.

Clicking the top-bar indicator or the Battery Info row opens the MagicPods tab.

It needs:

- MagicPodsCore running as the same user (`magicpodscore.service`, see the
  MagicPodsCore `docs/FRAME.md`). The menu talks to it directly on
  `ws://127.0.0.1:2020`; no other program or window is involved.
- Steam's local DevTools endpoint (127.0.0.1:8080). Steam opens it when Steam developer
  mode is on, or when the file `~/.steam/steam/.cef-enable-remote-debugging` exists (the
  same switch Decky Loader uses). `install.sh` creates that file, so developer mode can be
  turned off after the next Steam restart. Without the endpoint the menu does not appear;
  MagicPodsCore keeps working. No Steam restart is needed to install, update or remove the
  menu itself.
- `python3` (part of SteamOS).

## Install, update, remove

    ./install.sh            # from the unpacked release (or ./frame/install.sh in the repo)
                            # copies to ~/.local/share/magicpods-app/frame and enables
                            # the user service magicpods-steamui.service
    ~/.local/share/magicpods-app/frame/uninstall.sh

To update, run the new release's `install.sh`. The service restarts and replaces the menu
in Steam's pages within a few seconds. `uninstall.sh` removes the menu from Steam's pages
and deletes the files; MagicPodsCore and its settings are not touched.

## How it works, and its limits

`magicpods-steamui.py` checks every few seconds that Steam's VR bar and quick-access
pages run the current `magicpods-menu.js`, using Steam's local DevTools endpoint
(127.0.0.1:8080, available because Steam runs with `-cef-enable-debugging`). This is the
mechanism Decky Loader uses. It only ever sends that one fixed script, and stopping the
service removes everything it added.

This is unofficial. A Steam update can change these pages; the menu then does not
appear until the script is updated, and nothing else is affected. Menu preferences
(displayed noise modes, low-battery level) are kept in Steam's browser storage.

Steam's DevTools endpoint is unauthenticated. With SteamOS developer mode on, the headset
also forwards it to the network on port 8081; with developer mode off it stays on the
headset only. Low-battery alerts are SteamVR notifications (via SteamVR's `vrcmd`).
"Disable headphone standby mode" streams digital silence to the headphones with `pw-cat`,
pinned to their output, while it is on.
