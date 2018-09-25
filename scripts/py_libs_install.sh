#!/bin/sh
# run installs with sudo! 
echo ***Running update and upgrade***
sudo apt-get update  
sudo apt-get upgrade 
echo ***Installing python3 pip***
sudo apt-get install python3-pip
echo ***Installing pi3d***
sudo pip3 install pi3d   
echo ***Installing python3 PIL Required for pi3d***
sudo apt-get install python3-pil 
echo ***Installing python3 numpy Required for pi3d***
sudo apt-get install python3-numpy     
echo ***Installing feedparser***
sudo pip3 install feedparser
echo ***Installing WiringPi for gpio control, to dim backlight***
sudo sudo apt-get install wiringpi   
