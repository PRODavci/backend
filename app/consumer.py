import asyncio
import json

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from core.config import config

RABBIT_HOST = config.RABBITMQ_HOST
RABBIT_PORT = config.RABBITMQ_PORT
RABBITMQ_USER = config.RABBITMQ_USER
RABBITMQ_PASSWORD = config.RABBITMQ_PASSWORD


async def process_alive_hosts(data: dict):
    print(data)


async def process_hosts_services(data: dict):
    print(data)


async def receive_message():
    print(RABBIT_HOST, RABBIT_PORT)
    print(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = await aio_pika.connect_robust(
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('backend-api')

        async def on_message(message: AbstractIncomingMessage) -> None:
            data = message.body.decode()
            data = json.loads(data)
            print(" [x] Received dictionary :", data)

            if data['type'] == 'alive_hosts':
                await process_alive_hosts(data)

            elif data['type'] == 'host_service':
                await process_hosts_services(data)

            await message.ack()

        await queue.consume(on_message)
        await asyncio.Future()


def start_consumer():
    print(" [x] Start receiving")
    asyncio.run(receive_message())
