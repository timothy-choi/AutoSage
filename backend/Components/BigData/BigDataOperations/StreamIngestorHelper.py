from typing import Callable, Optional
from kafka import KafkaConsumer
import threading
import json

_consumers = {}
_threads = {}
_running_flags = {}

def start_stream_ingestor(
    name: str,
    topic: str,
    callback: Callable[[dict], None],
    bootstrap_servers: str = "localhost:9092",
    group_id: str = "stream-ingestor",
    auto_offset_reset: str = "latest",
    deserializer: Optional[Callable[[bytes], dict]] = None
) -> bool:
    if name in _running_flags and _running_flags[name]:
        return False

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset=auto_offset_reset,
        value_deserializer=deserializer or (lambda m: json.loads(m.decode("utf-8")))
    )
    _consumers[name] = consumer
    _running_flags[name] = True

    def run():
        for message in consumer:
            if not _running_flags.get(name):
                break
            callback(message.value)

    thread = threading.Thread(target=run)
    _threads[name] = thread
    thread.start()
    return True

def stop_stream_ingestor(name: str) -> bool:
    if _running_flags.get(name):
        _running_flags[name] = False
        if name in _consumers:
            _consumers[name].close()
        if name in _threads:
            _threads[name].join()
        return True
    return False