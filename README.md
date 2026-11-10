# MagicPods for Steam Frame

This is a fork of [MagicPods for Linux](https://github.com/steam3d/MagicPodsLinux) by
Aleksandr Maslov and Andrei Litvintsev, adapted for the **Steam Frame**. It brings the
menus of the [MagicPods Decky plugin](https://github.com/steam3d/MagicPodsDecky) into the
Frame's own VR interface. All credit for MagicPods goes to the original project; this
fork only adds what the Frame needs. Licence: GPL-3.0, the same as the original.

## What you get on the Frame

- **Battery in the top bar**, next to the headset battery: one blue bar per earbud and
  the percentage. Clicking it opens the MagicPods menu.
- **A MagicPods tab** in the quick menu (the one the headset battery opens), with the
  same menus as on the Steam Deck:
  - **Headphones:** battery for each earbud and the case, noise control, ear detection
    (pause when off-ear, switch to the speakers when both are out), conversation
    awareness, equalizer, press-and-hold controls and the other options your headphones
    support.
  - **Devices:** Bluetooth on/off and connecting or disconnecting paired headphones.
  - **Settings:** which noise modes to show, low-battery notifications, "Disable
    headphone standby mode" and more.
- **An earbuds row** under Battery Info.
- **Low-battery notifications** that name the part, for example "MagicPods: Left earbud
  18% remaining. Charge your headphones."

Works with AirPods, Beats, Galaxy Buds and Pixel Buds
([list](docs/UPSTREAM-README.md#-supported-headphones)). It needs
[MagicPodsCore for Steam Frame](https://github.com/jimas21/MagicPodsCore), the background
service that talks to the headphones.

## Install

### With frameplex

In frameplex, open **Settings › Earbuds** and choose **Install earbud support**. It
installs MagicPodsCore and this menu and keeps them up to date. (Coming in the next
frameplex beta.)

### Manually

1. Pair your headphones in the Frame's Bluetooth settings.
2. Install MagicPodsCore: see its
   [instructions](https://github.com/jimas21/MagicPodsCore#install).
3. In a terminal on the Frame (Konsole, in Desktop Mode), download
   `magicpods-frame-menu.tar.gz` from the
   [latest release](https://github.com/jimas21/MagicPodsLinux/releases/latest), then:

   ```sh
   tar -xzf magicpods-frame-menu.tar.gz
   ./magicpods-frame-menu/install.sh
   ```

4. Restart the headset once.

To update, repeat step 3 with the new release. To remove:
`~/.local/share/magicpods-app/frame/uninstall.sh` (MagicPodsCore and your headphone
settings stay).

Everything runs as your normal user; nothing needs root.

## How it works

The menu is a script that runs inside Steam's own VR interface, the same way Decky
Loader adds its menus on the Steam Deck; the installer turns on the local connection
Steam provides for that. A small background service keeps the script in place, shows the
low-battery notifications through SteamVR and runs the standby fix. Everything talks to
MagicPodsCore on the headset itself; nothing is sent anywhere else.

It is unofficial: a Steam update can change Steam's menus. If that happens, the battery
indicator or the tab may disappear until this project is updated; Steam itself and the
headphone features (ear detection, speaker switching) keep working.

Details: [frame/README.md](frame/README.md).

## About this repository

- `frame/`: the Steam Frame menu (released as `magicpods-frame-menu.tar.gz`, signed).
- `src/`: the original MagicPods desktop app (Qt), with small changes so it can work with
  a separately running MagicPodsCore. The Frame does not use it.
- The original project's README: [docs/UPSTREAM-README.md](docs/UPSTREAM-README.md).
- The changes are on the `frame-arm64` branch.

## Credits and licence

- [MagicPods for Linux](https://github.com/steam3d/MagicPodsLinux),
  [MagicPods for Decky](https://github.com/steam3d/MagicPodsDecky) and
  [MagicPodsCore](https://github.com/steam3d/MagicPodsCore) by Aleksandr Maslov
  (<https://magicpods.app>) and Andrei Litvintsev. The menu's noise-mode icons and its
  behaviour follow MagicPods for Decky.
- This fork and its changes: GPL-3.0, like the original.
