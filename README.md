# python-arcade-game
This repository contains all software for my highschool project of building an arcade machine that runs AI-generated games using a Raspberry Pi.

**This project is made to run on a _Raspberry Pi_ with _Raspberry Pi OS_ installed (preferably the _lite_ version).**



## These instructions will guide you through how to set up this project on a Raspberry Pi.


### First enter raspi-config:
```
sudo raspi-config
```
Navigate - System Options -> Boot / Auto Login and make sure that “Console Autologin” is selected.

Then navigate - System Options -> Wireless LAN and fill in the SSID and password of the WiFi you want.

Close raspi-config by selecting "Finish" in the start menu.


### Update the system and install Git:
```
sudo apt update
sudo apt install git
```
### Then clone this repository:
```
git clone https://github.com/LoveTheCoder/python-arcade-game.git
```
### Set the permissions of setup.py and then run it:
```
cd python-arcade-game
sudo chmod ugo+rwx setup.py
sudo python3 setup.py
```
### Lastly, reboot your Raspberry Pi:
```
sudo reboot
```
Now the startmenu should open at boot.
