Hyperspace Pod Cluster



Turn multiple laptops into a single distributed compute cluster using Ray.

















Overview



Hyperspace Pod Cluster allows multiple laptops to work together as a distributed computing cluster.



One laptop acts as the Master / Head Node, while additional laptops join as Worker Nodes. Ray manages task distribution across the connected machines.



&#x20;                ┌─────────────────────────────┐

&#x20;                │       Laptop 1               │

&#x20;                │     MASTER / HEAD NODE      │

&#x20;                │     Ray Dashboard :8265     │

&#x20;                └──────────────┬──────────────┘

&#x20;                               │

&#x20;                   Wi-Fi / Ethernet / VPN

&#x20;                               │

&#x20;             ┌─────────────────┼─────────────────┐

&#x20;             │                 │                 │

&#x20;      ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐

&#x20;      │  Laptop 2   │   │  Laptop 3   │   │  Laptop N   │

&#x20;      │   WORKER    │   │   WORKER    │   │   WORKER    │

&#x20;      │ CPU / RAM   │   │ CPU / RAM   │   │ CPU / RAM   │

&#x20;      └─────────────┘   └─────────────┘   └─────────────┘

Features

Distributed CPU computing

Multiple worker laptops

Ray-based cluster management

Ray dashboard

Cluster information monitoring

Distributed task testing

Performance benchmarking

Windows installation scripts

Linux/macOS installation scripts

Wi-Fi and Ethernet networking

Tailscale support for remote networking

Requirements

Python 3.10 or higher

Ray

psutil

Windows 10/11, Linux, or macOS

Network connectivity between cluster machines

Project Structure

hyperspace-pod-cluster/

│

├── setup/

│   ├── install.bat

│   ├── install.sh

│   └── firewall\_setup.bat

│

├── cluster/

│   ├── start\_master.bat

│   ├── start\_master.sh

│   ├── join\_pod.bat

│   ├── join\_pod.sh

│   └── stop\_cluster.bat

│

├── scripts/

│   ├── test\_cluster.py

│   ├── cluster\_info.py

│   └── benchmark.py

│

├── docs/

│   ├── SETUP\_GUIDE.md

│   ├── NETWORKING.md

│   └── TROUBLESHOOTING.md

│

├── requirements.txt

├── .gitignore

└── README.md

Quick Start

1\. Install on All Laptops

Windows



Run on every laptop:



setup\\install.bat

Linux/macOS



Run:



bash setup/install.sh

2\. Find the Master Laptop IP



On Laptop 1, run:



ipconfig



Find the IPv4 address.



Example:



192.168.1.50

3\. Start the Master Node



On Laptop 1 only, run:



cluster\\start\_master.bat



The master starts the Ray head node.



Dashboard:



http://localhost:8265

4\. Connect Worker Laptops



On each worker laptop, open:



cluster\\join\_pod.bat



Edit:



set MASTER\_IP=192.168.1.50



Replace 192.168.1.50 with the actual IP address of Laptop 1.



Then run:



cluster\\join\_pod.bat



Repeat this on Laptop 2, Laptop 3, Laptop 4, and additional worker machines.



Ray Dashboard



On the master laptop:



http://localhost:8265



From another laptop:



http://MASTER\_IP:8265



Example:



http://192.168.1.50:8265



The dashboard can be used to monitor the Ray cluster.



Test the Cluster



Run:



python scripts/test\_cluster.py



The test dispatches multiple tasks through Ray and reports the machines that execute them.



Example:



HYPERSPACE POD - CLUSTER STATUS





Connected Machines : 3

Total CPU Cores    : 24

Total RAM          : 48.0 GB





Dispatching 12 parallel tasks across all laptops...





Task #00 completed on \[Laptop-1]

Task #01 completed on \[Laptop-2]

Task #02 completed on \[Laptop-3]

Cluster Information



To display information about the connected machines:



python scripts/cluster\_info.py



The script reports:



Number of nodes

Total CPU resources

Total RAM

Total GPU resources

Individual node status

CPU resources per node

RAM per node

Benchmark



Run:



python scripts/benchmark.py



The benchmark executes distributed compute tasks and reports:



Execution time

Number of machines used

Throughput



Example:



Running benchmark: 20 tasks x 500K operations...





Completed in    : XX.XX seconds

Machines used   : X

Throughput      : X.X tasks/second

Networking

Wi-Fi



For a local cluster, connect all laptops to the same Wi-Fi network.



A 5 GHz Wi-Fi connection is recommended for better throughput.



Ethernet



Gigabit Ethernet can provide lower latency and more consistent performance than Wi-Fi.



Recommended for heavy distributed workloads.



Tailscale



Tailscale can be used when machines are not on the same local network.



General setup:



Install Tailscale on all laptops.

Sign in to the same Tailscale network.

Find the master's Tailscale IP address.

Set that address as MASTER\_IP.

Start the worker node.

Firewall Configuration



On Windows, run:



setup\\firewall\_setup.bat



The script configures the required firewall rules for the cluster.



Administrator privileges may be required.



Power Settings



For long-running worker nodes:



Disable automatic sleep while plugged in.

Prevent the laptop from sleeping when the lid is closed if required.

Keep worker laptops connected to power during long workloads.

Use a stable network connection.

Stopping the Cluster



To stop Ray on a machine:



cluster\\stop\_cluster.bat



Alternatively:



ray stop

Scaling



The cluster can contain multiple worker machines.



Example:



Laptops	Configuration

2	1 Master + 1 Worker

3	1 Master + 2 Workers

5	1 Master + 4 Workers

8	1 Master + 7 Workers

10+	Larger distributed cluster



Actual performance depends on the CPU, RAM, GPU, network bandwidth, latency, and workload of each machine.



Example Use Cases



Hyperspace Pod Cluster can be used for:



Distributed Python workloads

Parallel computation

Machine-learning experiments

Data processing

Computer-vision workloads

Batch processing

Distributed benchmarking

Multi-machine development and testing

Troubleshooting

Worker Cannot Connect



Check the following:



MASTER\_IP



Make sure it points to the master laptop's reachable IP address.



Also verify:



Both machines are connected to the network.

The master is running.

Firewall rules are configured.

Port 6379 is reachable.

Dashboard Does Not Load



On the master:



http://localhost:8265



From another laptop:



http://MASTER\_IP:8265

ray Command Not Found



Run the installation script again:



setup\\install.bat



Or install Ray manually:



pip install -U "ray\[default]"

Worker Disconnects



Check:



Network stability

Master IP address

Firewall configuration

Laptop sleep settings

Power connection

Slow Wi-Fi



Try:



5 GHz Wi-Fi

Ethernet

A better Wi-Fi access point

Reducing network traffic

Using wired networking for heavy workloads

Documentation



Detailed documentation is available in:



docs/

├── SETUP\_GUIDE.md

├── NETWORKING.md

└── TROUBLESHOOTING.md

Technology Stack

Technology	Purpose

Python	Application and cluster scripts

Ray	Distributed computing framework

psutil	System resource information

Windows Batch	Windows automation

Bash	Linux/macOS automation

Wi-Fi/Ethernet	Local networking

Tailscale	Remote networking

License



This project is licensed under the MIT License.

