#!/bin/sh
# XLPM Installer Script
curl -s -o /tmp/xlpm_binary -L https://github.com/VladosNX/xlpm/raw/refs/heads/main/xlpm
curl -s -o /tmp/xlpm_daemon_binary -L https://github.com/VladosNX/xlpm/raw/refs/heads/main/xlpm-daemon
curl -s -o /tmp/xlpm_daemon_ui_binary -L https://github.com/VladosNX/xlpm/raw/refs/heads/main/xlpm-daemon-ui
mv /tmp/xlpm_binary /usr/bin/xlpm
mv /tmp/xlpm_daemon_binary /usr/bin/xlpm_daemon
mv /tmp/xlpm_daemon_ui_binary /usr/bin/xlpm_daemon_ui
chmod ugo+x /usr/bin/xlpm
echo 'Installing complete'
