
Debian
====================
This directory contains files used to package ketand/ketan-qt
for Debian-based Linux systems. If you compile ketand/ketan-qt yourself, there are some useful files here.

## ketan: URI support ##


ketan-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install ketan-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your ketanqt binary to `/usr/bin`
and the `../../share/pixmaps/ketan128.png` to `/usr/share/pixmaps`

ketan-qt.protocol (KDE)

