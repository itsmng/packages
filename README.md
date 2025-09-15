# Debian & Red Hat Packages for ITSM-NG

## Debian

ITSM-NG is stored in ***/usr/share/itsm-ng*** and ***/itsm-ng/var/lib/itsm-ng***, you can update *itsm-ng* folder. 

To install the dpkg developper package execute this command:
```
apt install dpkg-dev debhelper wget
```

Then, set the version in the *rules* file in *debian* folder.
Also, update the changelog file to keep track of the changes.


Then, you just need to compile it using this command:
```
dpkg-buildpackage -us -uc -b
```

Now your debian package is in the *../* folder.

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
