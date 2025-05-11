import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from typing_extensions import deprecated

import uvicorn
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from fastapi import FastAPI
from pydantic import BaseModel



class AIOProducerConsumer:

    def __init__(self):
        self.topic = 'aio-topic'
        server = 'localhost:9092'
        self.producer = AIOKafkaProducer(
            bootstrap_servers=server,  # 注意这里
            value_serializer=lambda v: v.encode('utf-8'),
            key_serializer=lambda v: v.encode('utf-8') if v else None
        )
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=server,
            group_id="aio-consume-group",
            session_timeout_ms=60000,  # 会话超时时间
            heartbeat_interval_ms=60000,  # 心跳间隔
            max_poll_interval_ms=300000,  # 最大处理间隔
            # key_deserializer = lambda v: v.decode('utf-8'),
            # value_deserializer= lambda v: v.decode('utf-8')

        )
        self.consumer_task = None
        self.push_task = None

        self.push_queue: asyncio.Queue[
            tuple[asyncio.Event, tuple[str, str, str]]
        ] = asyncio.Queue(1000)

    async def start(self):
        await self.producer.start()
        if self.consumer_task is None or self.consumer_task.done():
            self.consumer_task = asyncio.create_task(self.robust_consumer())
        if self.push_task is None or self.push_task.done():
            self.push_task = asyncio.create_task(self._real_push())

    async def stop(self):
        await self.producer.stop()

        if self.push_task:
            self.push_task.cancel()
            try:
                await self.push_task
            except asyncio.CancelledError:
                print("Consumer task cancelled")

        if self.consumer_task:
            self.consumer_task.cancel()
            try:
                await self.consumer_task
            except asyncio.CancelledError:
                print("Consumer task cancelled")

        await self.consumer.stop()

    # don't use this push in web http thread
    # use push_message instead, see https://aber.sh/articles/asyncio-kafka/
    @deprecated("don't call directly from web http thread, it will cause CPU high")
    async def produce(self, value):
        try:
            await self.producer.send_and_wait(self.topic, value=value, key="item")
            print("Message sent:", value)
        except Exception as e:
            print(f"Error sending message: {e}")

    async def push_message(self, value: str, key: str) -> None:
        """
        Push a message to a Kafka topic.
        """
        topic = self.topic
        event = asyncio.Event()
        await self.push_queue.put((event, (topic, value, key)))
        # await event.wait()


    async def _real_push(self):
        print(" _real_push is running")
        while True:
            event, (topic, value, key) = await self.push_queue.get()
            try:
                await self.producer.send_and_wait(topic=topic, value=value, key=key)
            except Exception as e:
                print(f"Failed to push message to Kafka: {e}")
            finally:
                event.set()

    async def robust_consumer(self):
        consumer = self.consumer
        print(" robust_consumer is running")
        try:
            await consumer.start()

            while True:
                try:
                    async for msg in consumer:
                        print("Consumed event from topic {topic}(ts={ts}): key = {key:12} value = {value:12}".format(
                            topic=msg.topic, ts = datetime.fromtimestamp(msg.timestamp/1000), key=msg.key.decode('utf-8') if msg.key else None, value=msg.value.decode('utf-8')))

                        # 模拟业务处理
                        await asyncio.sleep(0.1)

                        # 手动提交（确保至少处理一次语义）
                        await consumer.commit()

                except asyncio.CancelledError:
                    print("Consumer task cancelled")
                    break
                except Exception as e:
                    print(f"Processing failed: {e}")
                    await asyncio.sleep(5)  # 错误后延迟重试
        except asyncio.CancelledError:
            print("Consumer task cancelled")
        except Exception as oe:
            print(f"Error starting consumer: {oe}")




config = {"bootstrap.servers": "localhost:9092"}




class Item(BaseModel):
    name: str


aio_producer: AIOProducerConsumer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    global aio_producer
    aio_producer = AIOProducerConsumer()
    await aio_producer.start()
    yield
    # Clean up and release the resources
    await aio_producer.stop()
    print("AIO producer stopped")

app = FastAPI(lifespan=lifespan)


cnt = 0


def ack(err, msg):
    global cnt
    cnt = cnt + 1
    print("cnt is ", cnt)




@app.post("/items1")
async def create_item1(item: Item):
    result = await aio_producer.push_message(item.name, "item")
    return {"timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "kafka_consumer": "running" if aio_producer.consumer_task and not aio_producer.consumer_task.done() else "stopped"
    }

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)