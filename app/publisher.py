import json

import aio_pika

from core.config import config

RABBIT_HOST = config.RABBITMQ_HOST
RABBIT_PORT = config.RABBITMQ_PORT
RABBITMQ_USER = config.RABBITMQ_USER
RABBITMQ_PASSWORD = config.RABBITMQ_PASSWORD


async def send_to_queue(queue_name, data):
    connection = await aio_pika.connect_robust(
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}/")

    try:
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(queue_name)

            data = json.dumps(data)
            await channel.default_exchange.publish(
                aio_pika.Message(body=data.encode()),
                routing_key=queue_name
            )

            print(" [x] Data published successfully!")

    except Exception as e:
        print(f" [x] Error publishing data: {e}")

    finally:
        await connection.close()
