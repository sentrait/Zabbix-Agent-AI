#!/bin/bash
TARGET_DIR="/usr/share/zabbix/ui/modules/zabbix_ai_agent"
SOURCE_DIR="/home/ubuntu/zabbix_agent/zabbix_module/zabbix_ai_agent"

if [ -d "$TARGET_DIR" ]; then
    echo "Module already linked or exists at $TARGET_DIR"
else
    echo "Linking module..."
    sudo ln -s "$SOURCE_DIR" "$TARGET_DIR"
    echo "Module linked. Go to Zabbix Administration > General > Modules to enable it."
fi
