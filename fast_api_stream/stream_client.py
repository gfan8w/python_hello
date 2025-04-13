
# !/usr/bin/env python
# coding=utf-8
#
# stream_client.py


import requests

url = "http://127.0.0.1:8001/stream/"  # 替换为你的实际接口地址


def test1():
    try:
        response = requests.get(url, stream=True) # stream参数为True

        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=7):  # 这行很重要哦
                if chunk:
                    print(chunk.decode("utf-8"), end="")
    except requests.RequestException as e:
        print(f"Request failed: {e}")


def test2():
    try:
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            for line in response.iter_lines(decode_unicode=True, chunk_size=8):
                if line:
                    print("Received SSE event:", line)
    except requests.RequestException as e:
        print(f"Request failed: {e}")


# test1()
test2()








