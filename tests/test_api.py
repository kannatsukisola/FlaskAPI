#coding:utf8
"""
测试 Flask API
"""
from flask.globals import request
import pytest
import requests

import sys
sys.path.append("..")

from source.settings import HOST, PORT


def test_connect():
    """测试flask 是否可以连接

    直接测试主页
    """
    url = f"http://{HOST}:{PORT}/"
    res = requests.get(url)
    
    assert res.status_code == 200, "连接不成功"
    assert res.json()["description"] == "连接 API 服务器成功"



class TestAPI:
    def test_settingparser(self):
        """测试配置解析
        """
        from source.utils import SETTINGS

        assert SETTINGS["HOST"] == HOST, "解析方法不正确"
        assert SETTINGS["PORT"] == PORT, "解析方法不正确"


    def test_request_parameters(self):
        """测试带请求参数
        """
        id_ = 1234
        url = f"http://{HOST}:{PORT}/args?id={id_}"
        res = requests.get(url)
        assert res.json()["id"] == str(id_), "带参数 GET 请求不成功"

        res = requests.post(url)
        assert res.json()["id"] == str(id_), "带参数 POST 请求不成功"