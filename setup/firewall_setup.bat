@echo off
echo Opening firewall ports...
netsh advfirewall firewall add rule name=HyperPod-Head dir=in action=allow protocol=TCP localport=6379
netsh advfirewall firewall add rule name=HyperPod-Dashboard dir=in action=allow protocol=TCP localport=8265
netsh advfirewall firewall add rule name=HyperPod-Worker dir=in action=allow protocol=TCP localport=10001
echo Done! Ports 6379, 8265, 10001 are open.
pause
