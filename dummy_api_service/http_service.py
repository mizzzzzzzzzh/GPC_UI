from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import secrets
from datetime import datetime, timedelta
import json
import pandas as pd

df = pd.read_csv("data/data_20230225.csv")


app = FastAPI()

# 假设的用户数据库，实际应用中应替换为真实数据库操作
fake_users_db = {
    "ics_data": {
        "username": "ics_data",
        "password": "123456",  # 注意：实际应用中不应明文存储密码
    }
}

# 定义一个简单的Token模型，用于后续可能的扩展
class Token(BaseModel):
    access_token: str
    token_type: str

# 定义OAuth2方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/macs/v1/account/login")

def verify_password(username: str, password: str):
    """验证用户名和密码"""
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        return False
    return True

class LoginCredentials(BaseModel):
    username: str
    password: str
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb3VyY2UiOiJ0aGlyZCIsInR5cGUiOiJhcHAiLCJ0aWQiOiJiYmNlMDQ5NDlmZWM0OTZkYTc1M2RkMTM1NjBiOWRjNSIsImFjY291bnQiOiJLYWZrYSIsInNpZCI6ImJjMzY4MzU3YmViYzRlOWZhYTZmMzZiMzE3YmU4ZTE4In0.N0uTk7g-mxcI5ZbU-teugxCoGqva5oBQurEsRNhpK8o"

@app.post("/macs/v1/account/login") #查询指定时间范围内的历史数据接口-历史回放接口
async def login(credentials: LoginCredentials):
    """
    用户登录接口
    """
    if not verify_password(credentials.username, credentials.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # 生成JWT令牌，这里仅作为示例，实际应用中应使用更安全的方式生成和验证JWT
    token = {
        "data": {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb3VyY2UiOiJ0aGlyZCIsInR5cGUiOiJhcHAiLCJ0aWQiOiJiYmNlMDQ5NDlmZWM0OTZkYTc1M2RkMTM1NjBiOWRjNSIsImFjY291bnQiOiJLYWZrYSIsInNpZCI6ImJjMzY4MzU3YmViYzRlOWZhYTZmMzZiMzE3YmU4ZTE4In0.N0uTk7g-mxcI5ZbU-teugxCoGqva5oBQurEsRNhpK8o"
        },
        "status": 0,
        "timestamp": 1605778520744
    }
    
    
    return json.dumps(token, indent=4)

def datetime2ts(date_str):
    return int(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)


class QueryData(BaseModel):
    endTime: str
    includeBounds: bool
    interval: int
    namespace: str = None
    startTime: str
    tags: list[str]

@app.post("/macs/v1/history/findDataBySection")
async def find_data_by_section(query_data: QueryData, token: str = Header(None)):
    # 这里仅作为示例，实际应用中你需要根据endTime, startTime等参数查询数据库并返回数据
    print(token, query_data)
    print(token==TOKEN)
    if not token or token != TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    _d = df.query(f" '{query_data.startTime}' <=time_period <='{query_data.endTime}'")

    resp_dict = {
        "data": [
            {
                "namespace": query_data.namespace,
                "tag": tag,
                "total": _d.shape[0],
                "data": [
                    {
                        "time": datetime2ts(row.time_period),
                        "qos": 0,
                        "value": row[tag]
                    } for _, row in _d.iterrows()
                ]
            } for tag in query_data.tags
        ],
        "message": "操作成功!",
        "status": 0,
        "timestamp": int(datetime.now().timestamp()) * 1000
    }

    return resp_dict

@app.post("/macs/v1/realtime/read/findPoint")
async def find_data_by_section(query_data: QueryData, token: str = Header(None)):
    # 这里仅作为示例，实际应用中你需要根据endTime, startTime等参数查询数据库并返回数据
    print(token, query_data)
    print(token==TOKEN)
    if not token or token != TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    _d = df.query(f" '{query_data.startTime}' <=time_period <='{query_data.endTime}'")

    resp_dict = {
        "data": [
            {
                "namespace": query_data.namespace,
                "tag": tag,
                "total": _d.shape[0],
                "data": [
                    {
                        "time": datetime2ts(row.time_period),
                        "qos": 0,
                        "value": row[tag]
                    } for _, row in _d.iterrows()
                ]
            } for tag in query_data.tags
        ],
        "message": "操作成功!",
        "status": 0,
        "timestamp": int(datetime.now().timestamp()) * 1000
    }

    return resp_dict


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8721)