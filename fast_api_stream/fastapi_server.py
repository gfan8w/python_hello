#!/usr/bin/env python
# *-* coding: utf-8 *-*
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time
import uvicorn
from starlette.responses import HTMLResponse

app = FastAPI()

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



async def generate_data():
    for i in BlockIterator(CONTENT, block=2):
        time.sleep(1)  # 模拟每秒生成一个块的耗时操作
        # yield f"FASTAPI Chunk {i}\n"
        yield i

@app.get("/")
async def read_root():
     with open("client.html", "r") as file:
        html = file.read()
        html = html.replace('$FASTAPI$', 'http://127.0.0.1:8001/stream/')
        return HTMLResponse(html)

@app.get("/stream")
async def stream_data():
    return StreamingResponse(generate_data(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)