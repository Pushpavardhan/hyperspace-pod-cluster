$root = "$env:USERPROFILE\\OneDrive\\Documents\\hyperspace-pod-cluster"

New-Item -ItemType Directory -Force -Path "$root\\setup","$root\\cluster","$root\\scripts","$root\\docs" | Out-Null

\# README.md

$readme = @"

\# Hyperspace Pod Cluster

Turn multiple laptops into a single unified super-server.

!\[Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)

!\[Ray](https://img.shields.io/badge/Ray-Cluster-orange)

!\[License](https://img.shields.io/badge/License-MIT-green)

\## Architecture





&#x20;   Master (Laptop 1) → Dashboard: http://localhost:8265

&#x20;           |

&#x20;┌──────────┼──────────┐

Laptop 2 Laptop 3 Laptop N Worker Worker Unlimited







\## Scale Calculator

| Laptops | CPU Cores | RAM      | Capability              |

|---------|-----------|----------|-------------------------|

| 3       | \~24       | \~48 GB   | Vision, API server      |

| 5       | \~40       | \~80 GB   | LLM inference           |

| 8       | \~64       | \~128 GB  | Distributed analytics   |

| 10+     | \~80+      | \~160+ GB | Mini Supercomputer      |

\## Quick Start

1\. Run setup\\install.bat on ALL laptops

2\. Run cluster\\start\_master.bat on Laptop 1

3\. Edit MASTER\_IP in cluster\\join\_pod.bat, run on Laptop 2,3,4...

4\. Open http://localhost:8265 to see the dashboard

5\. Test with: python scripts\\test\_cluster.py

\## Range and Networking

| Method          | Range      | Latency  |

|-----------------|------------|----------|

| 5 GHz Wi-Fi     | \~15 m      | 2-5 ms   |

| 2.4 GHz Wi-Fi   | \~40 m      | 5-15 ms  |

| Ethernet Cable  | 100 m      | <1 ms    |

| Tailscale VPN   | Worldwide  | 20-80 ms |

\## License

MIT License

"@

Set-Content "$root\\README.md" $readme -Encoding UTF8

\# requirements.txt

Set-Content "$root\\requirements.txt" "ray\[default]>=2.10.0`npsutil>=5.9.0" -Encoding UTF8

\# .gitignore

Set-Content "$root\\.gitignore" "\_\_pycache\_\_/`n\*.pyc`n\*.log`n.env" -Encoding UTF8

\# setup/install.bat

$install\_bat = @"

@echo off

title Hyperspace Pod - Installation

echo ============================================

echo    Installing Hyperspace Pod Cluster...

echo ============================================

python --version >nul 2>\&1

if %errorlevel% neq 0 (

&#x20;   echo \[ERROR] Python not found! Download from https://python.org

&#x20;   pause \& exit /b

)

echo Installing Python packages...

pip install -U "ray\[default]" psutil

call "%\~dp0firewall\_setup.bat"

echo ============================================

echo    Installation Complete!

echo ============================================

pause

"@

Set-Content "$root\\setup\\install.bat" $install\_bat -Encoding UTF8

\# setup/install.sh

Set-Content "$root\\setup\\install.sh" "#!/bin/bash`necho Installing Hyperspace Pod...`npip3 install -U 'ray\[default]' psutil`necho Done!" -Encoding UTF8

\# setup/firewall\_setup.bat

$fw = @"

@echo off

echo Opening firewall ports for Hyperspace Pod...

netsh advfirewall firewall add rule name="HyperPod-Head" dir=in action=allow protocol=TCP localport=6379

netsh advfirewall firewall add rule name="HyperPod-Dashboard" dir=in action=allow protocol=TCP localport=8265

netsh advfirewall firewall add rule name="HyperPod-Worker" dir=in action=allow protocol=TCP localport=10001

echo Done. Ports 6379, 8265, 10001 are open.

"@

Set-Content "$root\\setup\\firewall\_setup.bat" $fw -Encoding UTF8

\# cluster/start\_master.bat

$master = @"

@echo off

title Hyperspace Pod - MASTER NODE (Laptop 1)

echo ============================================

echo    MASTER NODE Starting on Laptop 1

echo ============================================

echo Your IP address:

ipconfig | findstr /i "IPv4"

echo Dashboard: http://localhost:8265

ray stop >nul 2>\&1

ray start --head --port=6379 --dashboard-host=0.0.0.0 --dashboard-port=8265

echo ============================================

echo  MASTER RUNNING - Open http://localhost:8265

echo ============================================

pause

"@

Set-Content "$root\\cluster\\start\_master.bat" $master -Encoding UTF8

\# cluster/start\_master.sh

Set-Content "$root\\cluster\\start\_master.sh" "#!/bin/bash`nray stop 2>/dev/null`nray start --head --port=6379 --dashboard-host=0.0.0.0 --dashboard-port=8265`necho Dashboard: http://localhost:8265" -Encoding UTF8

\# cluster/join\_pod.bat

$join = @"

@echo off

title Hyperspace Pod - WORKER NODE

echo ============================================

echo    Joining Hyperspace Pod as WORKER

echo ============================================

:: EDIT THIS LINE with Laptop 1 IP address

set MASTER\_IP=192.168.1.50

echo Connecting to %MASTER\_IP%:6379 ...

ray stop >nul 2>\&1

ray start --address=%MASTER\_IP%:6379

echo ============================================

echo  SUCCESS! This laptop is now a Worker Node.

echo  Dashboard: http://%MASTER\_IP%:8265

echo ============================================

pause

"@

Set-Content "$root\\cluster\\join\_pod.bat" $join -Encoding UTF8

\# cluster/join\_pod.sh

Set-Content "$root\\cluster\\join\_pod.sh" "#!/bin/bash`nMASTER\_IP=`"192.168.1.50`"`nray stop 2>/dev/null`nray start --address=`"`$MASTER\_IP:6379`"`necho SUCCESS - Worker connected!" -Encoding UTF8

\# cluster/stop\_cluster.bat

Set-Content "$root\\cluster\\stop\_cluster.bat" "@echo off`necho Shutting down Hyperspace Pod...`nray stop`necho Done.`npause" -Encoding UTF8

\# scripts/test\_cluster.py

$test\_py = @"

import ray, socket, time

ray.init(address='auto')

nodes = ray.nodes()

total\_cpu = sum(n\['Resources'].get('CPU', 0) for n in nodes)

total\_ram = sum(n\['Resources'].get('memory', 0) for n in nodes) / (1024\*\*3)

print(f"\\n{'='\*55}")

print(f"  HYPERSPACE POD - CLUSTER STATUS")

print(f"{'='\*55}")

print(f"  Connected Machines : {len(nodes)}")

print(f"  Total CPU Cores    : {int(total\_cpu)}")

print(f"  Total RAM          : {total\_ram:.1f} GB")

print(f"{'='\*55}")

for i, n in enumerate(nodes, 1):

&#x20;   cpu = int(n\['Resources'].get('CPU', 0))

&#x20;   ram = n\['Resources'].get('memory', 0) / (1024\*\*3)

&#x20;   print(f"  Laptop {i}: {n\['NodeName']:<20} {cpu} cores | {ram:.1f} GB")

print(f"{'='\*55}\\n")

@ray.remote

def run\_task(task\_id):

&#x20;   hostname = socket.gethostname()

&#x20;   time.sleep(0.5)

&#x20;   return f"Task #{task\_id:02d} completed on \[{hostname}]"

print("Dispatching 12 parallel tasks across all laptops...")

results = ray.get(\[run\_task.remote(i) for i in range(12)])

for r in results:

&#x20;   print(f"  {r}")

print("\\nAll tasks completed successfully!")

ray.shutdown()

"@

Set-Content "$root\\scripts\\test\_cluster.py" $test\_py -Encoding UTF8

\# scripts/cluster\_info.py

$info\_py = @"

import ray

ray.init(address='auto')

nodes = ray.nodes()

total\_cpu = sum(n\['Resources'].get('CPU', 0) for n in nodes)

total\_ram = sum(n\['Resources'].get('memory', 0) for n in nodes) / (1024\*\*3)

total\_gpu = sum(n\['Resources'].get('GPU', 0) for n in nodes)

print(f"\\n{'='\*55}")

print(f"  HYPERSPACE POD - LIVE INFO")

print(f"{'='\*55}")

print(f"  Nodes : {len(nodes)}  |  CPUs : {int(total\_cpu)}  |  RAM : {total\_ram:.1f} GB  |  GPUs : {int(total\_gpu)}")

print(f"{'='\*55}")

for i, n in enumerate(nodes, 1):

&#x20;   cpu = int(n\['Resources'].get('CPU', 0))

&#x20;   ram = n\['Resources'].get('memory', 0) / (1024\*\*3)

&#x20;   status = "ALIVE" if n\['Alive'] else "DOWN"

&#x20;   print(f"  \[{status}] Laptop {i}: {n\['NodeName']:<20} {cpu} cores | {ram:.0f} GB")

print(f"{'='\*55}\\n")

ray.shutdown()

"@

Set-Content "$root\\scripts\\cluster\_info.py" $info\_py -Encoding UTF8

\# scripts/benchmark.py

$bench\_py = @"

import ray, time, socket

ray.init(address='auto')

@ray.remote

def heavy\_compute(n):

&#x20;   return socket.gethostname(), sum(i\*i for i in range(n))

print("Running benchmark: 20 tasks x 500K operations...")

start = time.time()

results = ray.get(\[heavy\_compute.remote(500\_000) for \_ in range(20)])

elapsed = time.time() - start

machines = set(r\[0] for r in results)

print(f"Completed in    : {elapsed:.2f} seconds")

print(f"Machines used   : {len(machines)} ({', '.join(machines)})")

print(f"Throughput      : {20/elapsed:.1f} tasks/second")

ray.shutdown()

"@

Set-Content "$root\\scripts\\benchmark.py" $bench\_py -Encoding UTF8

\# docs/SETUP\_GUIDE.md

$setup\_doc = @"

\# Full Setup Guide

\## Requirements

\- Python 3.10+ on every laptop

\- All laptops on the same Wi-Fi or Tailscale for remote

\## Steps

\### 1. Install on ALL laptops

Windows: setup\\install.bat

Linux/macOS: bash setup/install.sh

\### 2. Find Laptop 1 IP

PowerShell: ipconfig (look for IPv4 Address e.g. 192.168.1.50)

\### 3. Start Master (Laptop 1 ONLY)

Double-click: cluster\\start\_master.bat

\### 4. Join Workers (Laptop 2, 3, 4...)

Open cluster\\join\_pod.bat in Notepad.

Change MASTER\_IP=192.168.1.50 to Laptop 1 actual IP.

Save and double-click.

\### 5. Dashboard

http://LAPTOP\_1\_IP:8265

\### 6. Test

python scripts\\test\_cluster.py

"@

Set-Content "$root\\docs\\SETUP\_GUIDE.md" $setup\_doc -Encoding UTF8

\# docs/NETWORKING.md

$net\_doc = @"

\# Networking Guide

\## Local Wi-Fi

Range \~40m. Use 5 GHz band. All laptops on same router.

\## Wired Ethernet (Best)

Up to 100m per cable. Buy a Gigabit Ethernet Switch (\~$20).

\## Tailscale (No range limit - Worldwide)

1\. Install from https://tailscale.com on all laptops

2\. Sign in with the SAME account

3\. Each laptop gets a 100.x.y.z IP

4\. Use that IP in join\_pod.bat

5\. Works from anywhere on Earth!

\## Power Settings (Important!)

Prevent laptops from sleeping:

\- Settings > Power > Never sleep when plugged in

\- Control Panel > Power Options > Lid close > Do nothing

"@

Set-Content "$root\\docs\\NETWORKING.md" $net\_doc -Encoding UTF8

\# docs/TROUBLESHOOTING.md

$trouble\_doc = @"

\# Troubleshooting

\## Worker cannot connect

\- Check MASTER\_IP is correct (run ipconfig on Laptop 1)

\- Run setup\\firewall\_setup.bat as Administrator on Laptop 1

\- Both laptops must be on same Wi-Fi

\## Dashboard not loading

\- Laptop 1: http://localhost:8265

\- Other laptops: http://LAPTOP1\_IP:8265

\## ray command not found

\- Re-run install.bat

\- Reinstall Python with Add to PATH checked

\## Laptop drops from cluster

\- Disable sleep mode in Power Settings

\- Set lid close to Do Nothing in Power Options

\## Wi-Fi too slow

\- Switch to 5 GHz band

\- Use Ethernet Switch + LAN cables for best speed

"@

Set-Content "$root\\docs\\TROUBLESHOOTING.md" $trouble\_doc -Encoding UTF8

Write-Host ""

Write-Host "============================================" -ForegroundColor Green

Write-Host "  All files created! Pushing to GitHub..." -ForegroundColor Green

Write-Host "============================================" -ForegroundColor Green

Set-Location $root

git init

git add .

git commit -m "Initial commit: Hyperspace Pod Cluster - multi-laptop super server"

git branch -M main

git remote add origin https://github.com/Pushpavardhan/hyperspace-pod-cluster.git

git push -u origin main

Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan

Write-Host "  DONE! Repo is live at:" -ForegroundColor Cyan

Write-Host "  https://github.com/Pushpavardhan/hyperspace-pod-cluster" -ForegroundColor Cyan

Write-Host "============================================" -ForegroundColor Cyan

