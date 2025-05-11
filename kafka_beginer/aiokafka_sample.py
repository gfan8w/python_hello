import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from typing_extensions import deprecated

import uvicorn
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer, TopicPartition
from fastapi import FastAPI
from pydantic import BaseModel


def print_red(text):
    # ANSI escape code for red color
    print("\033[31m" + text + "\033[0m")


class AIOProducerConsumer:

    def __init__(self):
        self.topic = 'aio-topic'
        self.server = 'localhost:9092'
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.server,  # 注意这里
            value_serializer=lambda v: v.encode('utf-8'),
            acks="all",  # 可选值：0（无ACK）, 1（Leader确认）, "all"（ISR全部确认）
            key_serializer=lambda v: v.encode('utf-8') if v else None
        )

        self.consumer_config = {
                "bootstrap_servers": self.server,
                "group_id": "aio-consume-group",
                "session_timeout_ms": 60000,  # 会话超时时间
                "heartbeat_interval_ms": 60000,  # 心跳间隔
                "max_poll_interval_ms": 300000,  # 最大处理间隔
                "enable_auto_commit": False,  # 是否自动提交偏移量, 默认是True
                # key_deserializer = lambda v: v.decode('utf-8'),
                # value_deserializer= lambda v: v.decode('utf-8')
        }

        self.consumer = AIOKafkaConsumer(self.topic, **self.consumer_config)
        self.consumer_task = None
        self.push_task = None
        self.monitor_task = None

        self.push_queue: asyncio.Queue[
            tuple[asyncio.Event, tuple[str, str, str]]
        ] = asyncio.Queue(1000)

    async def start(self):
        await self.producer.start()
        if self.consumer_task is None or self.consumer_task.done():
            self.consumer_task = asyncio.create_task(self.robust_consumer())
        if self.push_task is None or self.push_task.done():
            self.push_task = asyncio.create_task(self._real_push())
        self.monitor_task = asyncio.create_task(self.monitor_lag())

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

    async def get_topic_offsets(self):

        # 获取Topic所有分区
        partitions = self.consumer.partitions_for_topic(self.topic)
        tps = [TopicPartition(self.topic, p) for p in partitions]

        # 获取最早Offset（beginning）
        beginning_offsets = await self.consumer.beginning_offsets(tps)
        print("Earliest offsets:", beginning_offsets)

        # 获取最新Offset（end）
        end_offsets = await self.consumer.end_offsets(tps)
        print("Latest offsets:", end_offsets)

        # await consumer.stop()
        return {"beginning_offsets": beginning_offsets, "end_offsets": end_offsets}

    async def get_lag_sync(self):

        # 获取消费者分配的分区
        partitions = self.consumer.assignment()

        # 获取分区的最新Offset
        end_offsets = await self.consumer.end_offsets(partitions)

        # 获取已提交Offset
        committed_offsets = {}
        for tp in partitions:
            committed = await self.consumer.committed(tp)
            committed_offsets[tp] = committed or 0

        # 计算Lag
        for tp in partitions:
            lag = end_offsets[tp] - committed_offsets[tp]
            print(f"分区 {tp.partition} 的Lag: {lag}")

    async def monitor_lag(self, interval=10):
        consumer = AIOKafkaConsumer(self.topic, **self.consumer_config)
        await consumer.start()  #开启相同的group_id的消费者，但topic只有1个partition会有问题？TODO：？？

        while True:
            partitions = consumer.assignment()
            end_offsets = await consumer.end_offsets(partitions)

            for tp in partitions:
                committed = await consumer.committed(tp)
                lag = end_offsets[tp] - (committed or 0)
                print(f"警告！分区 {tp.partition} 的Lag过高: {lag}")
                if lag > 5:  # 设置报警阈值
                    print_red(f"警告！分区 {tp.partition} 的Lag过高: {lag}")

            await asyncio.sleep(interval)  # 每10秒检查一次


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
                metadata = await self.producer.send_and_wait(topic=topic, value=value, key=key)
                print(f"""发送成功！- 主题: {metadata.topic}  - 分区: {metadata.partition} - 偏移量: {metadata.offset} - 时间戳: {datetime.fromtimestamp(metadata.timestamp/1000)}""")
            except Exception as e:
                print(f"Failed to push message to Kafka: {e}")
            finally:
                event.set()

    async def robust_consumer(self):
        consumer = self.consumer
        print(" robust_consumer is running")
        try:
            await asyncio.sleep(60)
            await consumer.start()

            while True:
                try:
                    async for msg in consumer:
                        print("Consumed event from topic {topic}(ts={ts}): key = {key:12} value = {value:12}".format(
                            topic=msg.topic, ts = datetime.fromtimestamp(msg.timestamp/1000), key=msg.key.decode('utf-8') if msg.key else None, value=msg.value.decode('utf-8')))

                        # 模拟业务处理
                        await asyncio.sleep(0.1)

                        # 手动提交（确保至少处理一次语义）
                        tp = TopicPartition(msg.topic, msg.partition)
                        committed = await consumer.commit({tp: msg.offset + 1})
                        print(f"""- 当前消息Offset: {msg.offset}, - 已提交Offset: {committed}, - 剩余未消费: {msg.offset - committed if committed else 'N/A'}""")

                        await self.get_lag_sync()

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
        "kafka_consumer": "running" if aio_producer.consumer_task and not aio_producer.consumer_task.done() else "stopped",
        "kafka_offset": await aio_producer.get_topic_offsets(),
    }

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)