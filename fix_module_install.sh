#!/bin/bash
TARGET_DIR="/usr/share/zabbix/ui/modules/zabbix_ai_agent"
SOURCE_DIR="/home/ubuntu/zabbix_agent/zabbix_module/zabbix_ai_agent"

echo "Fixing module installation..."

# Remove the symlink if it exists
if [ -L "$TARGET_DIR" ]; then
    echo "removing existing symlink..."
    sudo rm "$TARGET_DIR"
fi

if [ -d "$TARGET_DIR" ]; then
    echo "removing existing directory..."
    sudo rm -rf "$TARGET_DIR"
fi

# Copy files instead
echo "Copying files to $TARGET_DIR..."
sudo cp -r "$SOURCE_DIR" "$TARGET_DIR"

# Fix permissions
echo "Setting permissions..."
sudo chown -R www-data:www-data "$TARGET_DIR"
sudo chmod -R 755 "$TARGET_DIR"

echo "Done. Please rescan modules in Zabbix."
