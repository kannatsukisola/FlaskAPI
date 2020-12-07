#coding:utf8
import flask
import logging
from flask import request, jsonify

app = flask.Flask(__name__)
logger = logging.getLogger(name="main")

#TODO:连接测试
@app.route("/", methods=["GET", "POST"])
def home():
    """测试服务器是否可以连接
    """
    result = jsonify({
        "description": "连接 API 服务器成功"
    })
    logger.debug("连接到测试服务器")
    return result


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")