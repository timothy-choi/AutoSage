from dask.distributed import Client, LocalCluster

def create_dask_client(n_workers=2, threads_per_worker=1, memory_limit='1GB'):
    cluster = LocalCluster(
        n_workers=n_workers,
        threads_per_worker=threads_per_worker,
        memory_limit=memory_limit
    )
    client = Client(cluster)
    return client, cluster

def run_dask_task(func, *args, n_workers=2, threads_per_worker=1, memory_limit='1GB', **kwargs):
    client, cluster = create_dask_client(n_workers, threads_per_worker, memory_limit)
    try:
        future = client.submit(func, *args, **kwargs)
        return future.result()
    except Exception as e:
        print(f"[DaskOrchestrator] Error running task: {e}")
        raise
    finally:
        client.shutdown()
        cluster.close()
