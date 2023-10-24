# Debian & Red Hat Packages for ITSM-NG

## Debian

ITSM-NG is stored in */var/www/html/itsm-ng*, you can update *itsm-ng* folder. 
If you do so update the version in the *control* file in *DEBIAN* folder.
Also, update the changelog file to keep track of the changes.

Then, you just need to recomplie it using this command:
```
dpkg-deb -Zgzip --build itsm-ng
dpkg-name itsm-ng.deb
```
OR
```
dpkg-deb -Zgzip --build itsm-ng itsm-ng_[version]_[arch].deb
```

_Note : -Zgzip is only reveleant if you are compiling from ubuntu which use `zst` as default compression method (debian is not compatible with this compression method)_

## RPM

If you also want to update the version, edit the *itsm-ng.spec* file in *SPECS* folder.

To compile the rpm you need to follow these instructions :

```
dnf install -y rpmdevtools git
rpmdev-setuptree
git clone https://github.com/itsmng/packages
cp -r packages/rpm/itsm-ng/* ~/rpmbuild/
rpmbuild -bb ~/rpmbuild/SPECS/itsm-ng.spec
```