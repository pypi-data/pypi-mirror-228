import base64
import io
import numpy as np
from PIL import Image  # pytype: disable=import-error

from pytriton.client import ModelClient
import json

def infer(payload):
    prompt = payload["prompt"]
    img_size = int(payload["height"])
    inference_steps = int(payload["inference_steps"])
    img_size = np.array([[img_size]])
    inference_steps = np.array([[inference_steps]])
    with ModelClient("grpc://localhost:8001", "StableDiffusion_1_5", init_timeout_s=1200.0) as client:
        prompt = np.array([[prompt]])
        prompt = np.char.encode(prompt, "utf-8")
        #result_dict = client.infer_batch(prompt=prompt, img_size=img_size)
        result_dict = client.infer_batch(prompt=prompt, img_size=img_size, inference_steps=inference_steps)
        return result_dict["image"][0]

class ChatGLMCall:


    @staticmethod
    def infer(payload):
        input = payload["input"]
        history = payload["history"]
        max_length = payload["max_length"]
        top_p = payload["top_p"]
        temperature = payload["temperature"]

        input = np.char.encode(np.array([[input]]), "utf-8")
        history = np.char.encode(np.array([[json.dumps(history)]]), "utf-8")
        max_length = np.array([[max_length]], dtype=np.int64)
        top_p = np.array([[top_p]], dtype=np.float32)
        temperature = np.array([[temperature]], dtype=np.float32)

        with ModelClient("grpc://localhost:8001", "ChatGLM_6B", init_timeout_s=1200.0) as client:
            result_dict = client.infer_batch(input=input, history=history, max_length=max_length, top_p=top_p, temperature=temperature)
            return result_dict["response"], result_dict["history"]
    
    @staticmethod
    def infer_iter(tid):
        tid = np.array([[tid]], dtype=np.int64)
        history = []
        response = None
        while True:
            with ModelClient("grpc://localhost:8001", "ChatGLM_6B_fn_iter", init_timeout_s=1200.0) as client:
                result_dict = client.infer_batch(tid=tid)
                response = result_dict["response"][0][0].decode()
                history_tmp = json.loads(result_dict["history"][0][0])
                # print(response)
                
                if response == "[STOP]":
                    break
                else:
                    history = history_tmp
                    yield response, history
        # 最后一返回：stop，以及记录的所有历史。
        yield response, history
    
    @staticmethod
    def add_iter(payload, tid):
        input = payload["input"]
        history = payload["history"]
        max_length = payload["max_length"]
        top_p = payload["top_p"]
        temperature = payload["temperature"]

        input = np.char.encode(np.array([[input]]), "utf-8")
        history = np.char.encode(np.array([[json.dumps(history)]]), "utf-8")
        max_length = np.array([[max_length]], dtype=np.int64)
        top_p = np.array([[top_p]], dtype=np.float32)
        temperature = np.array([[temperature]], dtype=np.float32)

        tid = np.array([[tid]], dtype=np.int64)

        with ModelClient("grpc://localhost:8001", "ChatGLM_6B_additer", init_timeout_s=1200.0) as client:
            result_dict = client.infer_batch(input=input, history=history, max_length=max_length, top_p=top_p, temperature=temperature, tid=tid)
            return result_dict["response"], result_dict["history"]


__all__ = ["ChatGLMCall", "infer"]

if __name__ == '__main__':
    payload = {'prompt': 'a cute cat', 'height': 768, 'width': 768, 'inference_steps': 30}
    print(infer(payload))