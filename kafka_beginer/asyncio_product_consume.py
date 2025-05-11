#!/usr/bin/env python

# Companion code to the blog post "Integrating Kafka With Python
# Asyncio Web Applications"
# https://www.confluent.io/blog/kafka-python-asyncio-integration/
#
# Example Siege [https://github.com/JoeDog/siege] test:
# $ siege -c 400 -r 200 'http://localhost:8000/items1 POST {"name":"testuser"}'


import asyncio
import confluent_kafka
from confluent_kafka import KafkaException
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from time import time
from threading import Thread
import uvicorn


class AIOProducer:
    def __init__(self, configs, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._producer = confluent_kafka.Producer(configs)
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            print("AIOProducer polling")
            self._producer.poll(60)
            print("AIOProducer polling done")

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, topic, value):
        """
        An awaitable produce method.
        """
        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                self._loop.call_soon_threadsafe(result.set_exception, KafkaException(err))
            else:
                self._loop.call_soon_threadsafe(result.set_result, msg)
        self._producer.produce(topic, value, on_delivery=ack)
        return result

    def produce2(self, topic, value, on_delivery):
        """
        A produce method in which delivery notifications are made available
        via both the returned future and on_delivery callback (if specified).
        """
        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                self._loop.call_soon_threadsafe(
                    result.set_exception, KafkaException(err))
            else:
                self._loop.call_soon_threadsafe(
                    result.set_result, msg)
            if on_delivery:
                self._loop.call_soon_threadsafe(
                    on_delivery, err, msg)
        self._producer.produce(topic, value, on_delivery=ack)
        return result


class Producer:
    def __init__(self, configs):
        self._producer = confluent_kafka.Producer(configs)
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            print("Producer polling")
            self._producer.poll(1)
            print("Producer polling done")

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, topic, value, on_delivery=None):
        self._producer.produce(topic, value, on_delivery=on_delivery)


config = {"bootstrap.servers": "localhost:9092"}

app = FastAPI()


class Item(BaseModel):
    name: str


aio_producer: AIOProducer = None
producer: Producer = None


@app.on_event("startup")
async def startup_event():
    global producer, aio_producer
    aio_producer = AIOProducer(config)
    producer = Producer(config)


@app.on_event("shutdown")
def shutdown_event():
    aio_producer.close()
    producer.close()

cnt = 0


def ack(err, msg):
    global cnt
    cnt = cnt + 1
    print("cnt is ", cnt)




@app.post("/items1")
async def create_item1(item: Item):
    try:
        result = await aio_producer.produce("items", item.name)
        return {"timestamp": result.timestamp()}
    except KafkaException as ex:
        raise HTTPException(status_code=500, detail=ex.args[0].str())


@app.post("/items2")
async def create_item2(item: Item):
    try:
        result = await aio_producer.produce2("items", item.name, on_delivery=ack)
        print("result is ", result)
        return {"timestamp": time()}
    except KafkaException as ex:
        raise HTTPException(status_code=500, detail=ex.args[0].str())


@app.post("/items3")
async def create_item3(item: Item):
    try:
        producer.produce("items", item.name, on_delivery=ack)
        return {"timestamp": time()}
    except KafkaException as ex:
        raise HTTPException(status_code=500, detail=ex.args[0].str())


@app.post("/items4")
async def create_item4(item: Item):
    try:
        producer.produce("items", item.name)
        return {"timestamp": time()}
    except KafkaException as ex:
        raise HTTPException(status_code=500, detail=ex.args[0].str())


@app.post("/items6")
async def create_item5(item: Item):
    return {"timestamp": time()}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)