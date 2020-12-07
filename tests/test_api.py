#coding:utf8
"""
测试 Flask API
"""
import pytest
import requests


host="0.0.0.0"
port=5000
def test_connect():
    """测试flask 是否可以连接

    直接测试主页
    """
    url = f"http://{host}:{port}/"
    res = requests.get(url)
    
    assert res.status_code == 200, "连接不成功"
    assert res.json()["description"] == "连接 API 服务器成功"
