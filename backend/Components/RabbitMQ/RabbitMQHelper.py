import pika
import json

def connect_to_rabbitmq(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    return connection, channel

def consume_message_from_rabbitmq(queue_name, process_func):
    def callback(ch, method, properties, body):
        process_message(ch, method, properties, process_func, body)

    connection, channel = connect_to_rabbitmq(queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
    channel.start_consuming()

def process_message(ch, method, properties, process_func, body):
    try:
        message = json.loads(body)
        process_func(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        raise e

def publish_message_to_rabbitmq(queue_name, message):
    connection, channel = connect_to_rabbitmq(queue_name)
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()