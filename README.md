# Debian & Red Hat Packages for ITSM-NG

## Debian

ITSM-NG is stored in */var/www/html/itsm-ng*, you can update *itsm-ng* folder. 
If you do so update the version in the *control* file in *DEBIAN* folder.
Also, update the changelog file to keep track of the changes.

Then, you just need to recomplie it using this command:
```
dpkg-deb --build itsm-ng
dpkg-name itsm-ng.deb
```
OR
```
dpkg-deb --build itsm-ng itsm-ng_[version]_[arch].deb
```

## RPM

Store ITSM-NG as.tgz format in */SOURCES*.
To compile your own source update *itsm-ng.tgz*. 
If you also want to update the version, edit the *itsm-ng.spec* file in *SPECS* folder.

To compile the rpm you need to follow these instructions :
- *TODO*