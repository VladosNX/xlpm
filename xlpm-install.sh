#!/bin/sh
# XLPM Installer Script
curl -s -o /tmp/xlpm_binary -L https://github.com/VladosNX/xlpm/raw/refs/heads/main/xlpm
mv /tmp/xlpm_binary /usr/bin/xlpm
chmod ugo+x /usr/bin/xlpm
echo 'Installing complete'
