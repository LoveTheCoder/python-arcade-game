import os
import subprocess

def create_systemd_service():
    service_content = """[Unit]
Description=Launch games on startup
After=multi-user.target
AllowIsolate=yes

[Service]
TTYPath=/dev/tty1
StandardOutput=tty
StandardInput=tty
StandardError=tty
TTYVHangup=yes
TTYReset=yes
Type=idle
User=ga5
Environment=Display=:0
Environment=XAUTHORITY=.Xauthority
Environment=XDG_RUNTIME_DIR=/run/user/1000
ExecStart=/home/ga5/launch.sh

[Install]
WantedBy=multi-user.target
"""
    service_path = "/lib/systemd/system/arcade.service"
    try:
        # Skapa och skriv till arcade.service
        with open(service_path, "w") as service_file:
            service_file.write(service_content)
        print(f"Systemd service-fil skapad: {service_path}")

        # Sätt rättigheter
        subprocess.run(["sudo", "chmod", "ugo+rwx", service_path], check=True)
        print("Behörigheter för arcade.service har satts.")

        # Aktivera servicen
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "arcade.service"], check=True)
        print("arcade.service har aktiverats.")
    except Exception as e:
        print(f"Ett fel uppstod vid skapandet av systemd-servicen: {e}")

def create_launch_script():
    script_content = """#!/bin/bash
exec </dev/tty1
old_stty=$(stty -g)

echo "To enter the terminal, press any key" > /dev/tty1

if read -t 1 -n 1 -r key; then
    stty "$old_stty" </dev/tty1
    echo -e "\\n$key was pressed. Process Terminated!" > /dev/tty1
    exit 0
else
    cd /home/ga5/python-arcade-game
    sudo python3 main.py
fi
"""
    script_path = "/home/ga5/launch.sh"
    try:
        # Skapa och skriv till launch.sh
        with open(script_path, "w") as script_file:
            script_file.write(script_content)
        print(f"Launch-script skapad: {script_path}")

        # Sätt rättigheter
        subprocess.run(["sudo", "chmod", "ugo+rwx", script_path], check=True)
        print("Behörigheter för launch.sh har satts.")
    except Exception as e:
        print(f"Ett fel uppstod vid skapandet av launch-scriptet: {e}")

if __name__ == "__main__":
    create_systemd_service()
    create_launch_script()