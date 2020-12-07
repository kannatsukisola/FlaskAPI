#coding:utf8
"""
测试 Flask API
"""
import pytest
import requests

import sys
sys.path.append("..")



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



class TestAPI:
    def test_settingparser(self):
        """测试配置解析
        """
        from source.utils import SETTINGS
        from source.settings import HOST, PORT

        assert SETTINGS["HOST"] == HOST, "解析方法不正确"
        assert SETTINGS["PORT"] == PORT, "解析方法不正确"