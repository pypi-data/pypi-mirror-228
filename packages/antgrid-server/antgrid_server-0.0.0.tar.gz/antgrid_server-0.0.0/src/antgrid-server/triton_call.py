import websocket
import json
from typing import Dict

from request_collections import *
from blockutils import *

def call_chatglm(wsapp: websocket.WebSocketApp, payload: Dict, tid: int, stream=True):
    model = ChatGLMCall
    model.add_iter(payload=payload, tid=tid)
    if stream:
        for model_response, history in model.infer_iter(tid=tid):
            payload = {
                "response": model_response,
                "history": history
            }
            response = {
                "type": PackageType.Response,
                "tid" : tid,
                "payload": payload
            } # this
        wsapp.send(json.dumps(response))
    else:
        raise NotImplementedError