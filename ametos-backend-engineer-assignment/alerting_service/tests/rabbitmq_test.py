import pika

# Connection parameters
rabbitmq_host = 'localhost'  # Use 'localhost' if RabbitMQ is on the same machine
queue_name = 'test_queue'    # Name of the test queue

# Establish connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Declare a queue (idempotent operation - ensures the queue exists)
channel.queue_declare(queue=queue_name)

# Publish a message
message = "Hello, RabbitMQ!"
channel.basic_publish(exchange='', routing_key=queue_name, body=message)
print(f"Sent: {message}")

# Callback function to handle messages
def callback(ch, method, properties, body):
    print(f"Received: {body.decode()}")

# Consume the message
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit, press CTRL+C')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Exiting...")
    channel.stop_consuming()
    connection.close()
