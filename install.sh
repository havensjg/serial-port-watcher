# Installs a shortcut in the user's applications folder that launches the program

# Create the .desktop file
cat << EOF > serial-port-watcher.desktop
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

# Link it into the user's applications folder
ln -s $PWD/serial-port-watcher.desktop ~/.local/share/applications/serial-port-watcher.desktop