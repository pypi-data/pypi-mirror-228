import pandas as pd


def format_db_table(dbs):
    dbs = pd.DataFrame(dbs)
    client = pd.json_normalize(dbs['client'])
    prefix = "client_"
    client.columns = [prefix + col for col in client.columns]
    dbs.drop(columns='client', inplace=True)
    dbs = pd.concat([dbs, client], axis=1)
    dbs.rename(columns={
        "id": "database_id",
        "name": "database_name"
    }, inplace=True)
    return dbs


def format_process_table(processes):
    processes = pd.DataFrame(processes)
    processes.rename(columns={
        "tenant_id": "process_id",
        "tenant_name": "process_name",
        "tenant_created_at": "process_created_at",
        "tenant_updated_at": "process_updated_at",
    }, inplace=True)
    return processes


def format_tasks_table(tasks):
    tasks = pd.DataFrame(tasks)
    tasks.rename(columns={
        "id": "task_id",
        "user_id": "task_name",
        "tenant_id": "process_id",
        "created_at": "task_created_at",
        "updated_at": "task_updated_at"
    }, inplace=True)
    return tasks


def format_queues_table(queues):
    queues = pd.DataFrame(queues)
    process = pd.json_normalize(queues['tenant'])
    prefix = "process_"
    process.columns = [prefix + col for col in process.columns]
    queues.drop(columns='tenant', inplace=True)
    queues = pd.concat([queues, process], axis=1)
    return queues


def format_tasks_executions_table(executions):
    executions = pd.DataFrame(executions)
    task = pd.json_normalize(executions['process'])
    prefix = "task_"
    task.columns = [prefix + col for col in task.columns]
    executions.drop(columns='process', inplace=True)
    executions = pd.concat([executions, task], axis=1)
    executions.rename(columns={
        "id": "execution_id",
        "status": "execution_processing_status_id",
        "created_at": "execution_created_at",
        "updated_at": "execution_updated_at"
    }, inplace=True)
    return executions


def format_queue_items(queue_items):
    queue_items = pd.DataFrame(queue_items)
    queue = pd.json_normalize(queue_items['queue'])
    task = pd.json_normalize(queue_items['process'])
    queue.columns = ["queue_" + col for col in queue.columns]
    task.rename(columns={
        "provider.id": "task_provider_id",
        "provider.name": "task_provider_name",
        "consumer.id": "task_consumer_id",
        "consumer.name": "task_consumer_name"
    }, inplace=True)
    queue_items.drop(columns=['process', 'queue'], inplace=True)
    queue_items = pd.concat([queue_items, queue, task], axis=1)
    queue_items.rename(columns={
        "id": "queue_item_id",
        "status": "queue_item_processing_status_id",
        "created_at": "queue_item_created_at",
        "started_at": "queue_item_started_at",
        "finished_at": "queue_item_finished_at",
    }, inplace=True)
    return queue_items
