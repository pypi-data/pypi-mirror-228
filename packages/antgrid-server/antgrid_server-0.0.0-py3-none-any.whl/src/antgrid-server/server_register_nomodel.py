import json
from blockutils import *
import logging
import websocket
import time
from typing import Dict
from multiprocessing import Process, Queue
import threading
from request_collections import *
import configparser
logging.basicConfig(level=logging.INFO)
config = configparser.ConfigParser()
def set_login_package(token: str, device: str, devicemem: str):
    return {
        "type": PackageType.Login,
        "authorization": token,
        "device": device,
        "deviceMem": devicemem
    }


device = "NVIDIA GTX 1080Ti"
device_mem = "11GB"


state_pack = {
    "type": PackageType.ServerState,
    "state": "Running",
    "model": "Stable Diffution v1.4",
}

# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NCwibmFtZSI6InRlc3QiLCJjdXIiOjE2OTI5NTU5NjguNzc5ODQyMX0.KBMtFoRQQBtezsSViGZfYv9YbkJ25YuIuXf-Wgmjph8"
token = None




def on_open(wsapp):
    logging.info("Connection Established.")
    info = {
        "type": PackageType.Login,
        "authorization": token,
        "device": device,
        "devicemem": device_mem
    }
    wsapp.send(json.dumps(info))

def _on_message(wsapp, message):
    message = json.loads(message)
    if message["type"] == PackageType.PulseCheck:
        logging.info("Pluse Check.")
        wsapp.send(json.dumps(state_pack))

    elif message["type"] == PackageType.Verification:
        if message["state"] == "failed":
            logging.warning("Auth Failed.")
            return
        print("receive model message as below:\n", message)
        models_to_run = message["model"]
        # here you got the model_to_run message, and decide on which model to run.
        logging.info(f"Prepare pytriton for models: {models_to_run}")
        # pytriton_file_name = prepare(message)
        # th = threading.Thread(target=run_pytriton, args=(pytriton_file_name,))
        # th.start()
        ##########################################################################
        time.sleep(1)
        # response = {
        #     "type": PackageType.ServerState,
        #     "state": "Running",
        #     "model": models_to_run
        # }
        # wsapp.send(json.dumps(response))
        # logging.info("Running {}".format(models_to_run))
        state_pack["model"] = models_to_run
        state_pack["state"] = "Ready"
        wsapp.send(json.dumps(state_pack))
        logging.info("Ready {}".format(models_to_run))

    elif message["type"] == PackageType.Request:
        #payload = json.loads(message["payload"])
        payload = message["payload"]
        print("receive payload:", payload)
        def call_chatglm(wsapp: websocket.WebSocketApp, payload: Dict, tid: int, stream=True):
            model = ChatGLMCall
            model.add_iter(payload=payload, tid=tid)
            if stream:
                for model_response, history in model.infer_iter(tid=tid):
                    payload = {
                        "response": model_response,
                        "history": history,
                        ## 确定server
                        "servername": message["servername"]
                    }
                    response = {
                        "type": PackageType.Response,
                        "tid" : tid,
                        "payload": payload
                    } # this
                    wsapp.send(json.dumps(response))
                    time.sleep(0.01)
            else:
                raise NotImplementedError
        
        call_chatglm(wsapp, payload, message["tid"])
    elif message["type"] == PackageType.Join:
        logging.info("Server join!")

        time.sleep(5)
        join_info ={
                "type": PackageType.Join,
                "state": "Running",
                "model": message["model"],
                "servername": message["servername"],
                "tid": message["tid"]
        }
        state_pack["state"] = "Running"
        logging.info(join_info)
        wsapp.send(json.dumps(join_info))

    elif message["type"] == PackageType.Leave:
        logging.info("Server leave!")
        ## 定义leave操作，此处为暂时关闭这个triton进程
        ## close_pytriton()
        time.sleep(2)
        logging.info("Pytriton closed.") 
        leave_info ={
                "type": PackageType.Leave,
                "state": "Leave",
                "model": message["model"],
                "servername": message["servername"],
                "tid": message["tid"]           
        }       
        state_pack["state"] = "Leave"
        ## state_pack["model"] = ""    
        wsapp.send(json.dumps(leave_info))

def on_message(wsapp, message):
    th = threading.Thread(target=_on_message, args=(wsapp, message))
    th.start()

def on_cont_message(wsapp, frame_data, frame_fin):
    logging.info("Receive continuous message.")
    print(type(frame_data), frame_fin,"----", sep="\n")

def on_data(wsapp, frame_data, frame_opcode, frame_fin):
    pass

def on_close(ws, close_status_code, close_msg):
    print(">>>>>>CLOSED")

def start(file: str):
    global token
    config.read(file)
    host = config.get('server','host')
    port = config.get('server','port')
    route = "ws"
    token = config.get('server','token')
    try:
        logging.info("ServerRuntime Start.")
        websocket.setdefaulttimeout(1000)
        url = 'ws://' + host + ':' + port + '/' + route
        # login_url = 'http://' + args.host + ':' + args.port + '/' + "login"
        # token = get_token(args.username, args.password, login_url)
        wsapp = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_cont_message=on_cont_message, on_data=on_data, on_close=on_close)
        wsapp.run_forever(ping_interval=2000, ping_timeout=1000)
    except KeyboardInterrupt:
        logging.info("ServerRuntime exited.")
        wsapp.close()