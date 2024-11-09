#!/bin/sh
# XLPM Installer Script
curl -s https://github.com/VladosNX/xlpm/raw/refs/heads/main/xlpm -o /tmp/xlpm_binary
mv /tmp/xlpm_binary /usr/bin/xlpm
echo 'Installing complete'
