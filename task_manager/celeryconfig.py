imports = (
    "app.service.storage_service",
    "app.cache.cache",
    "app.storage.mongo_client",
    "app.service.get_data.process_data",
    "app.service.get_data.collect",
)

broker_url = "amqp://guest:guest@rabbitmq:5672"
result_backend = "rpc://guest:guest@rabbitmq:5672"
result_persistent = False
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
