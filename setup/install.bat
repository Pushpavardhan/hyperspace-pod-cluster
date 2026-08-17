@echo off
title Hyperspace Pod - Installation
echo Installing Hyperspace Pod Cluster...
pip install -U "ray[default]" psutil
echo Installation Complete!
pause
