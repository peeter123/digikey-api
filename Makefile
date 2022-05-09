#!/usr/bin/make

deb:
	DEB_BUILD_OPTIONS=nocheck fakeroot dpkg-buildpackage -uc -b

deb_sig:
	DEB_BUILD_OPTIONS=nocheck fakeroot dpkg-buildpackage -b

deb_clean:
	fakeroot debian/rules clean


.PHONY: deb deb_clean
