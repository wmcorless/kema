
Debian
====================
This directory contains files used to package kemad/kema-qt
for Debian-based Linux systems. If you compile kemad/kema-qt yourself, there are some useful files here.

## kema: URI support ##


kema-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install kema-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your kemaqt binary to `/usr/bin`
and the `../../share/pixmaps/kema128.png` to `/usr/share/pixmaps`

kema-qt.protocol (KDE)

