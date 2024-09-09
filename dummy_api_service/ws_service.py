from fastapi import FastAPI, WebSocket
import asyncio
from datetime import datetime
import pandas as pd
import json

app = FastAPI()

data_sample = pd.read_csv("data/data_20230225.csv")

async def send_realtime_data(websocket: WebSocket, cols: list = None):
    """每隔1秒向客户端推送当前时间戳，处理连接中断情况"""
    try:
        index = 0
        while True:
            row_data = data_sample[cols].iloc[index].to_dict()
            message = json.dumps(row_data)
            await websocket.send_text(message)
            index = (index + 1) % len(data_sample)
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("WebSocket connection closed by client.")
    except Exception as e:
        print(f"An error occurred while sending data: {e}")
    finally:
        print("Closing WebSocket task.")

@app.websocket("/rtdata")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        cols=None
        data = await websocket.receive_json()  # 接收初始化的JSON数据
        
        if "type" not in data or "cols" not in data:
            await websocket.send_text("Missing required parameters.")
            await websocket.close()
            return


        # 假设我们只处理第一个item作为示例
        cols = data["cols"] if data["cols"] else None
        if cols:
            print(f"WebSocket connection established for cols: {cols}")
        
        # 开始发送实时数据
        await send_realtime_data(websocket, cols)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print(f"WebSocket connection closed for cols: {cols}")
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8720)