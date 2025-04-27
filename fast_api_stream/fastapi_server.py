#!/usr/bin/env python
# *-* coding: utf-8 *-*
import asyncio
import random
import uuid
from typing import Dict

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time
import uvicorn
from starlette.responses import HTMLResponse

app = FastAPI()

# 存储会话状态
sessions: Dict[str, dict] = {}


CONTENT = """《易经》被誉为诸经之首，大道之源，是中华优秀传统文化的总纲领，是中华民族五千年智慧的结晶。他含盖万有、纲纪群伦，是中华文化的杰出代表；他博大精微、包罗万象，亦是中华文明的源头。其内容涉及哲学、生命、自然、科学、政治、天文、地理、文学、艺术等诸多领域，是各家共同的经典。
《易经》包括《连山》《归藏》《周易》三部易书，现存于世的只有《周易》。《周易》相传是周文王被囚羑里时，研究《易经》所作的结论。"""


class BlockIterator:
    def __init__(self, text, block):
        self.index=0
        self.text= text
        self.block_size = block

    def    __iter__(self):
        return self

    def __next__(self):
        if self.index >=len(self.text):
            raise StopIteration

        block = self.text[self.index: self.index + self.block_size]
        self.index += self.block_size
        return block



async def generate_data(session_id: str, last_id: int = 0):
    session = sessions[session_id]
    message_id = last_id
    for i in BlockIterator(CONTENT, block=2):
        if not session["paused"]:

            await asyncio.sleep(0.5)  # 模拟每秒生成一个块的耗时操作
            random_number = random.randint(1, 5)
            # yield f"FASTAPI Chunk {i}\n"
            print(f"sending data: {i}")
            if random_number <3:  #模拟恶劣网络情况下的数据任意分块
                yield f"{i}\n\n"
            else:
                yield f"{i}"
        else:
            # 如果暂停，等待一小段时间再检查
            yield f"paused\n\n"
            start_time = time.time()
            while(True):
                if time.time() - start_time > 50 :
                    print(f"session: {session_id} pause timeout")
                    yield f"pause timeout\n\n"
                    return
                if not session["paused"]:
                    break
                else:
                    print("paused session %s %s sec"% (session_id, (time.time() - start_time)))
                    await asyncio.sleep(1)



@app.get("/")
async def read_root():
     with open("client.html", "r") as file:
        html = file.read()
        html = html.replace('$FASTAPI$', 'http://127.0.0.1:8001')
        return HTMLResponse(html)

@app.get("/stream")
async def stream_data(session_id: str, last_id: int = 0):
    if not session_id:
        session_id = str(uuid.uuid4())

        # 初始化或获取会话
    if session_id not in sessions:
        sessions[session_id] = {
            "paused": False,
            "last_id": last_id,
            "terminated": False
        }
    return StreamingResponse(generate_data(session_id, last_id), media_type="text/event-stream")


@app.post("/pause")
async def pause_stream(session_id: str):
    """暂停流"""
    if session_id in sessions:
        sessions[session_id]["paused"] = True
        return {"status": "paused"}
    return {"status": "session not found"}

@app.post("/continue")
async def continue_stream(session_id: str):
    """继续流"""
    if session_id in sessions:
        sessions[session_id]["paused"] = False
        return {"status": "resumed"}
    return {"status": "session not found"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)