import math
import threading
import typing

import uvicorn
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sse_starlette.sse import EventSourceResponse
from fastapi import FastAPI, Request
from json import JSONDecoder

from fastapi import FastAPI
from kafka import KafkaProducer
from kafka import KafkaConsumer
import asyncio
from datetime import datetime
from uuid import uuid4
import json

from sse.messenger import MessengerReq

SSE_STREAM_DELAY = 1  # second
SSE_RETRY_TIMEOUT = 15000  # milisecond

producer = KafkaProducer(bootstrap_servers='localhost:9092')
consumer = KafkaConsumer("newstopic")

router = APIRouter()

from datetime import date


def json_date_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Data %s not serializable" % type(obj))


def date_hook_deserializer(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.strptime(value, "%Y-%m-%d").date()
        except:
            pass
    return json_dict


def find_primes(n: int) -> typing.List[int]:
    """
    计算从 2 到 n 的所有质数（非常耗 CPU）
    """
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes



@router.post("/messenger/kafka/send")
async def send_messnger_details(req:MessengerReq):
    """
    {
        "id": 1,
        "firstname": "Joke",
        "lastname": "good",
        "salary": 123.44,
        "date_employed": "2025-09-12",
        "status": 1,
        "vendor_id": 4
    }
    """
    messenger_dict = req.model_dump(exclude_unset=True)
    producer.send("newstopic", bytes(str(json.dumps(messenger_dict, default=json_date_serializer)), 'utf-8'))
    return {"content": "messenger details sent"}


@router.get('/messenger/sse/add')
async def send_message_stream(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    task = asyncio.current_task()
    thread_id = threading.get_ident()
    thread = threading.current_thread()
    print(
        f"New SSE client connected | IP: {client_ip} Port: {request.client.port} | Thread id: {thread_id}(name: {thread.name, thread.ident}) | Coroutine task: {task.get_name()} ID: {id(task)}")

    async def event_provider():
        while True:
            if await request.is_disconnected():
                break

            message = consumer.poll()
            if not len(message.items()) == 0:
                for tp, records in message.items():
                    for rec in records:
                        task1 = asyncio.current_task()
                        thread_id1 = threading.get_ident()
                        thread1 = threading.current_thread()
                        print(
                            f"SSE pushed to client | IP: {client_ip} Port: {request.client.port} | Thread id: {thread_id1}(name: {thread1.name, thread1.ident}) | Coroutine task: {task1.get_name()} ID: {id(task1)}")

                        messenger_dict = json.loads(rec.value.decode('utf-8'), object_hook=date_hook_deserializer)

                        # repo = MessengerRepository()
                        # result = await repo.insert_messenger(messenger_dict)

                        # 测试：计算 1,000,000 以内的质数（将占用大量 CPU）
                        primes = find_primes(1_000_000_000)
                        print(f"Found {len(primes)} primes up to 1,000,000")

                        id1 = uuid4()
                        yield {
                            "event": "kafka messenger processor: {} Received: {}".format(
                                asyncio.current_task().get_name(),
                                datetime.utcfromtimestamp(rec.timestamp // 1000).strftime("%B %d, %Y [%I:%M:%S %p]")),
                            "id": str(id1),
                            "retry": SSE_RETRY_TIMEOUT,
                            "data": rec.value.decode('utf-8')
                        }

            await asyncio.sleep(SSE_STREAM_DELAY)
            client_ip = request.client.host if request.client else "unknown"
            task = asyncio.current_task()
            thread_id = threading.get_ident()
            thread = threading.current_thread()
            print(
                f"SSE client keeplive | IP: {client_ip} Port: {request.client.port} | Thread id: {thread_id}(name: {thread.name, thread.ident}) | Coroutine task: {task.get_name()} ID: {id(task)}")

    return EventSourceResponse(event_provider())


app = FastAPI()
app.include_router(router, prefix='/sse')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)