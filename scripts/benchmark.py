import ray, time, socket
ray.init(address='auto')

@ray.remote
def heavy_compute(n):
    return socket.gethostname(), sum(i*i for i in range(n))

print('Running benchmark: 20 tasks x 500K operations...')
start = time.time()
results = ray.get([heavy_compute.remote(500_000) for _ in range(20)])
elapsed = time.time() - start
machines = set(r[0] for r in results)
print(f'Completed in  : {elapsed:.2f} seconds')
print(f'Machines used : {len(machines)} ({chr(44).join(machines)})')
print(f'Throughput    : {20/elapsed:.1f} tasks/second')
ray.shutdown()
