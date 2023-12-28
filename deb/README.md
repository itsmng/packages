## ITSM-NG Deb structure

### Before build .deb

Move itsm-ng app folder to `/usr/share`

Move the entire files from the itsm-ng app files folder into `/var/lib/itsm-ng`

In `/usr/share/itsm-ng/inc` folder, create the file `downstream.php` :

```bash    
$ vi downstream.php
```
```php
<?php
define('GLPI_CONFIG_DIR', '/etc/itsm-ng/');

if (file_exists(GLPI_CONFIG_DIR . '/local_define.php')) {
    require_once GLPI_CONFIG_DIR . '/local_define.php';
}
```