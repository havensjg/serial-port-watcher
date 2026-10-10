# Installs a shortcut in the user's applications folder that launches the program

# Variables
desktop_file=serial-port-watcher.desktop
opt_autostart=0
opt_help=0

# Parse options
for arg in "$@"; do
    # Help option
    if [ "$arg" = "--help" ]; then
        opt_help=1
    fi

    # Auto-start option
    if [ "$arg" = "--auto-start" ]; then
        opt_autostart=1
    fi

    # Everything else passed in is ignored
done

# If help was requested, just print the help and ignore all other options
if [ "$opt_help" -eq 1 ]; then
    echo "Serial Port Watcher - installer"
    echo "Installs the program and any requested optional features. Optional features can be enabled after installation"
    echo ""
    echo "Usage: $0 [options...]"
    echo ""
    echo "Options:"
    echo "  --help - Print this help message and perform no changes"
    echo "  --auto-start - Enable the script to install when the user logs in"
    exit 1
fi

# Create the .desktop file
cat << EOF > $desktop_file
[Desktop Entry]
Type=Application
Name=Serial Port Watcher
Comment=A tool for notifying the user when serial devices are added or removed
Path=$PWD
Exec=bash "$PWD/launch.sh"
Icon=$PWD/icon.png
Terminal=false
Categories=System;Monitor
EOF

# Auto-start option requires this
if [ "$opt_autostart" -eq 1 ]; then
    echo "X-GNOME-Autostart-enabled=true" >> $desktop_file
fi
echo "Generated .desktop file $desktop_file"

# Link it into the user's applications folder, if it doesn't already exist
apps_path="$HOME/.local/share/applications"
apps_link="$apps_path/$desktop_file" 
if [ ! -f "$apps_link" ]; then
    ln -s "$PWD/$desktop_file" "$apps_link"
    echo "Installed application link $apps_link"
fi

# Link the autostart script
if [ "$opt_autostart" -eq 1 ]; then
    autostart_path="$HOME/.config/autostart"
    autostart_file="$autostart_path/$desktop_file"
    if [ ! -f $autostart_file ]; then
        ln -s "$PWD/$desktop_file" "$autostart_file"
        echo "Enabled autostart"
    fi
fi