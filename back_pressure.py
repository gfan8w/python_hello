import asyncio
from asyncio.queues import Queue
import os

main_queue = Queue(5)
counter = 0
# message = os.urandom(10).hex()  # random 1kb message


async def producer():
    i =0
    while loop.is_running():
        i=i+1
        await main_queue.put(i)
        print(f"put {i} into queue")
        await asyncio.sleep(5)  # 主动让出控制权， 模拟一种更公平的调度方式


async def consumer():
    global counter
    while loop.is_running():
        d =await main_queue.get()
        print(f"get {d} from queue")
        counter += 1
        await asyncio.sleep(0.1)


async def end():
    await asyncio.sleep(50)

    asyncio.get_event_loop().stop()
    print("in queue : {}".format(main_queue.qsize()))
    print("processed items : {}".format(counter))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(producer())
    asyncio.ensure_future(consumer())
    asyncio.ensure_future(end())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()