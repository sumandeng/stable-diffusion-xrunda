
# -*- coding: utf-8 -*
#!/user/bin/python3

import threading
import sys, time
from numpy import *
import requests, json
from PIL import Image
import re
from io import BytesIO
import base64


if len(sys.argv) > 1 :
    counter = int(sys.argv[1])
else:
    counter = 5

def base64_to_image(base64_str, image_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    if image_path:
        img.save(image_path)
    return img

def text2image():
    url = "http://127.0.0.1:8502/sdapi/v1/txt2img"
    data = {
        "prompt": "altese puppy",
        "steps": 20
    }
    headers = {"Content-Type": "application/json"}
    ret = requests.post(url=url, headers=headers, json=data)
    result = json.loads(ret.text)
    img_key = 'images'
    if img_key in result:
        # images = result.get(img_key)
        # for image in images:
        #     time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        #     filename = f"{time_str}-{images.index(image)}.jpg"
        #     base64_to_image(image, filename)
        return True
    else:
        return False



timing = []

class TestThread(threading.Thread):
    def __init__(self, threadId, name):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name


    def run(self):
        print("开始线程: " + self.name)
        start_time = time.time()
        if text2image():
            end_time = time.time()
            duration = end_time - start_time
            timing.append(duration)
            print("[v]线程结束: " + self.name + ", 耗时: %.3f秒"%duration)
        else:
            print(f"[x]线程异常: {self.name}")

print(">>>>>>>>>>>>>开始测试>>>>>>>>>>>>")
workerThreads = []
for i in range(counter):
    thread = TestThread(i, f"Thread-{i}")
    workerThreads.append(thread)

for thread in workerThreads:
    thread.start()

for thread in workerThreads:
    thread.join()

print("<<<<<<<<<<<<测试结束<<<<<<<<<<<<")
print("*********测试结果**********")
print("线程数: %d"%len(workerThreads))
print("成功返回: %d"%len(timing))
print("最长耗时: %.3f秒"%max(timing))
print("最短耗时: %.3f秒"%min(timing))
print("平均耗时: %.3f秒"%mean(timing))
print("中位数: %.3f秒"%median(timing))

