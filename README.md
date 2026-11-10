# MagicPods for Steam Frame

This is a fork of [MagicPods for Linux](https://github.com/steam3d/MagicPodsLinux) by
[Aleksandr Maslov](https://github.com/steam3d) and
[Andrey Litvintsev](https://github.com/andreylitvintsev), adapted for the **Steam Frame**. It brings the
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

On the Steam Frame:

1. Pair your headphones in the Frame's Bluetooth settings.
2. Switch to **Desktop Mode**, open this page in the headset's browser and press the
   button to download the installer:

   <a href="https://github.com/jimas21/MagicPodsCore/releases/latest/download/Install-MagicPods.desktop"><img src="docs/images/install-button.svg" alt="Install MagicPods" width="240" /></a>

3. Open `Install-MagicPods.desktop` from your Downloads folder and confirm when Desktop
   Mode asks whether to trust it. A terminal window opens, downloads the latest
   MagicPodsCore and MagicPods menu releases, checks their signatures and installs both.
4. Restart the headset once. The earbuds battery then shows in the top bar.

**Update:** run the installer again; your settings are kept. **Remove:** open
[`Uninstall-MagicPods.desktop`](https://github.com/jimas21/MagicPodsCore/releases/latest/download/Uninstall-MagicPods.desktop)
the same way.

Everything runs as your normal user; nothing needs root. Every download is checked before
it is installed.

## How it works

The installer adds the MagicPods menu to Steam's own screens on the headset, which is
why the headset needs one restart after the first install. A small helper keeps the menu
in place and shows the low-battery notifications. Everything stays on the headset;
nothing is sent anywhere.

If a Steam update changes Steam's menus, the battery icon or the
MagicPods tab may disappear until this project is updated. Your earbuds keep working,
including ear detection and switching to the speakers.

Technical details: [frame/README.md](frame/README.md).

## For developers

- `frame/`: the Steam Frame menu (released as `magicpods-frame-menu.tar.gz`, signed).
- `src/`: the original MagicPods desktop app (Qt), with small changes so it can work with
  a separately running MagicPodsCore. The Frame does not use it.
- The original project's README: [docs/UPSTREAM-README.md](docs/UPSTREAM-README.md).
- The changes are on the `frame-arm64` branch.

## Credits and licence

- [MagicPods for Linux](https://github.com/steam3d/MagicPodsLinux),
  [MagicPods for Decky](https://github.com/steam3d/MagicPodsDecky) and
  [MagicPodsCore](https://github.com/steam3d/MagicPodsCore) by
  [Aleksandr Maslov](https://github.com/steam3d) (<https://magicpods.app>) and
  [Andrey Litvintsev](https://github.com/andreylitvintsev). The menu's noise-mode icons and its
  behaviour follow MagicPods for Decky.
- This fork and its changes: GPL-3.0, like the original (see [LICENSE](LICENSE)).
- If MagicPods is useful to you, consider
  [supporting the original project](https://magicpods.app/donate/).
- AirPods is a trademark of Apple Inc.; Beats, Galaxy Buds, Pixel Buds and Steam Frame
  belong to their owners. They are named only to say what this works with.
