
import requests
from requests.exceptions import HTTPError
from typing import Dict
import json

# 应用的URL，确保与你的FastAPI应用运行地址匹配
PORT=8721
BASE_URL = "http://localhost"
LOGIN_PATH = "/macs/v1/account/login"
HISTORY_RETRIEVE_PATH = "/macs/v1/history/findDataBySection" 
from datetime import datetime

def login_api(userinfo:Dict) -> str:

    # 发送POST请求
    try:
        response = requests.post(f"{BASE_URL}:{PORT}{LOGIN_PATH}", json=userinfo)
        
        # 确保请求成功
        response.raise_for_status()
        
        # 打印响应内容
        return response.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
        

def history_data_retrieve_api(headers:Dict, data:Dict) -> str:
    """
    {
        "endTime": "2021-11-10 21:47:36",
        "includeBounds": True,
        "interval": 20000,
        "startTime": "2021-11-10 20:41:36",
        "tags": ["AI_TAG0.AV", "AI_TAG1.AV"]
    }"""

    response = requests.post(f"{BASE_URL}:{PORT}{HISTORY_RETRIEVE_PATH}", headers=headers, json=data)

    if response.status_code == 200:
        return response
    else:
        print(f"Request failed with status {response.status_code}: {response.text}")
        
        
