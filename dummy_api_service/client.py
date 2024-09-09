import asyncio
import json
import websockets
from typing import Dict
async def receive_realtime_data(uri, body: Dict=None):
    async with websockets.connect(uri) as websocket:
        # 初始化发送cols信息给服务器
        # { "type":"point", "cols":[ "time_period", "coal_feed", "valve_opening" ] }

        await websocket.send(json.dumps(body))
        
        print(f"Connected to the server, waiting for real-time data on body: {body}")
        
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                print(f"Received Data: {data}")
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed by the server.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

if __name__ == "__main__":
    uri = "ws://localhost:8720/rtdata"
    body = { "type":"point", "cols":[ "time_period", "coal_feed", "valve_opening" ] }  # 更改为实际需要的列名
    
    asyncio.get_event_loop().run_until_complete(receive_realtime_data(uri, body))