#coding:utf8
import flask
import logging
from flask import request, jsonify

import sys
sys.path.append("..")
from source.utils import SETTINGS
from source.utils import _check

app = flask.Flask(__name__)
app.config["DEBUG"] = SETTINGS.get("APP_DEBUG", False)
app.config["port"] = SETTINGS["PORT"]
app.config["host"] = SETTINGS["HOST"]

logger = logging.getLogger(name=SETTINGS.get("App_NAME", "main"))

#Done:连接测试
@app.route("/", methods=["GET", "POST"])
def home():
    """测试服务器是否可以连接
    """
    result = jsonify({
        "description": "连接 API 服务器成功"
    })
    logger.debug("连接到测试服务器")
    return result


# TODO: 带参数请求
@app.route("/args", methods=["GET", "POST"])
def extract():
    """测试带参数请求是否成功
    """
    _check.check_parameters("id")
    result = jsonify({
        "id": request.args["id"]
    })
    return result
    


if __name__ == "__main__":
    app.run(port=SETTINGS["PORT"], host=SETTINGS["HOST"])