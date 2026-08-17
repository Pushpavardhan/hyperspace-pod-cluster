import ray, socket, time
ray.init(address='auto')
nodes = ray.nodes()
total_cpu = sum(n['Resources'].get('CPU',0) for n in nodes)
total_ram = sum(n['Resources'].get('memory',0) for n in nodes)/(1024**3)
print('='*50)
print('  HYPERSPACE POD - CLUSTER STATUS')
print('='*50)
print(f'  Machines : {len(nodes)}')
print(f'  CPU Cores: {int(total_cpu)}')
print(f'  RAM      : {total_ram:.1f} GB')
print('='*50)

@ray.remote
def run_task(i):
    import socket, time
    time.sleep(0.5)
    return f'Task {i:02d} on [{socket.gethostname()}]'

print('Dispatching 12 tasks across all laptops...')
results = ray.get([run_task.remote(i) for i in range(12)])
for r in results:
    print(f'  {r}')
print('All tasks completed!')
ray.shutdown()
