import asyncio
import json
import websockets
from typing import Dict, Callable
from collections import deque, defaultdict
from functools import partial
import traceback

async def receive_realtime_data(uri:str, body: Dict, callback: Callable[[str], None] = None):
    async with websockets.connect(uri) as websocket:
        # 初始化发送cols信息给服务器
        # { "type":"point", "cols":[ "time_period", "coal_feed", "valve_opening" ] }

        await websocket.send(json.dumps(body))
        
        print(f"Connected to the server, waiting for real-time data on body: {body}")
        
        while True:
            try:
                message = await websocket.recv()
                callback(message)
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed by the server.")
                break
            except Exception as e:
                traceback.print_exc()
                print(f"An error occurred: {e}")
                break
            
            await asyncio.sleep(1)  # 每隔0.1秒发送一次心跳包

if __name__ == "__main__":
    from datetime import datetime
     # 更改为实际需要的列名
    window_size=60
    ls = defaultdict(partial(deque, [0]*window_size, maxlen=window_size))
    def callback(rtdata: str):
        data = json.loads(rtdata)
        for k, v in data.items():
            if k=='time_period':
                ls[k].append(datetime.strptime(v, '%Y-%m-%d %H:%M:%S'))
            else:
                ls[k].append(v)
        print(ls)
    uri = "ws://localhost:8720/rtdata"
    body = { "type":"point", "cols":[ "time_period", "coal_feed", "valve_opening" ] } 
    asyncio.get_event_loop().run_until_complete(receive_realtime_data(uri, body, callback))