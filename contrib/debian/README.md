
Debian
====================
This directory contains files used to package kemad/Kema-qt
for Debian-based Linux systems. If you compile kemad/Kema-qt yourself, there are some useful files here.

## Kema: URI support ##


Kema-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install Kema-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your Kemaqt binary to `/usr/bin`
and the `../../share/pixmaps/Kema128.png` to `/usr/share/pixmaps`

Kema-qt.protocol (KDE)

