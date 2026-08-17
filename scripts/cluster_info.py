import ray
ray.init(address='auto')
nodes = ray.nodes()
total_cpu = sum(n['Resources'].get('CPU',0) for n in nodes)
total_ram = sum(n['Resources'].get('memory',0) for n in nodes)/(1024**3)
total_gpu = sum(n['Resources'].get('GPU',0) for n in nodes)
print(f'Nodes:{len(nodes)}  CPUs:{int(total_cpu)}  RAM:{total_ram:.1f}GB  GPUs:{int(total_gpu)}')
for i,n in enumerate(nodes,1):
    cpu = int(n['Resources'].get('CPU',0))
    ram = n['Resources'].get('memory',0)/(1024**3)
    status = 'ALIVE' if n['Alive'] else 'DOWN'
    print(f'  [{status}] Laptop {i}: {cpu} cores | {ram:.0f} GB')
ray.shutdown()
