#coding:utf8
import flask
import logging
from flask import request, jsonify
import os
from os import path
import sqlite3
import requests
import json

import sys
sys.path.append("..")
from source.utils import SETTINGS
from source.utils import _check
from source.lib.locations import locations


# from source.utils.move_fun import send_mark, move_to_point


app = flask.Flask(__name__)
app.config["DEBUG"] = SETTINGS.get("APP_DEBUG", False)
app.config["port"] = SETTINGS["PORT"]
app.config["host"] = SETTINGS["HOST"]

logger = logging.getLogger(name=SETTINGS.get("App_NAME", "main"))

# 全局变量，记录当前点位
counter = 0
current_path = 0
retry_times = 0

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


# Done: 带参数请求
@app.route("/args", methods=["GET", "POST"])
def extract():
    """测试带参数请求是否成功
    """
    result = _check.check_parameters("id", "book")
    return jsonify(result)
    
# TODO: 平衡车移动 API 接口
@app.route("/move", methods=["GET", "POST"])
def move():
    """调用移动平衡车接口
    """
    # # 设置全局变量存储位置，用于检查阶段确认成功数量和位置所需步长值是否一直
    global current_path
    # import ipdb; ipdb.set_trace()
    location = _check.check_parameters("location")["location"]
    steps = locations[location]['point']
    # 连接任务列表写入任务数据
    connect = sqlite3.connect(path.join(path.dirname(__file__), "db/task.db"))
    try:
        cursor = connect.cursor()
        cursor.execute("INSERT INTO tlist (target, steps) VALUES (?, ?);", 
            (location, len(steps)))
        connect.commit()
        
        # 直接调用每步到点
        x,y, w = steps[0]
        move_to_point(x, y, w)
        current_path = location
        # for x, y in steps:
        #     logger.info("进入点{x}, {y}".format(x=x, y=y))
        #     os.system("python %s -x %s -y %s" % (
        #         path.join(path.dirname(__file__), "utils/move_fun.py")
        #         , x, y
        #     ))

        result = json.dumps({
            "code": 200,
            "msg": "Moving to location %s" % location
        })
    except:
        result = json.dumps({
            "code": 500,
            "msg": "Request Failure"
        })
        # raise Exception("没有到达目标点或者任务写入列表失败")
    finally:
        connect.close()
    return result

# 小车移动到某个点位
def move_to_point(pointx, pointy, forcew):
    os.system("python %s -x %s -y %s -r %s " % (
        path.join(path.dirname(__file__), "utils/move_fun.py")
        , pointx, pointy, forcew
    ))

# TODO: 检查任务状态
# 设置全局变量统计请求检查的次数


@app.route("/check", methods=["GET", "POST"])
def check():
    """检查任务状态

    检查任务步长值和最终数量值是否一直
    """
    # import ipdb; ipdb.set_trace()
    global counter, current_path, retry_times
    # 连接任务列表写入任务数据
    connect = sqlite3.connect(path.join(path.dirname(__file__), "db/task.db"))
    path_points = locations[current_path]['point']
    result_status = _check.check_parameters("result_status")["result_status"]
    try:
        cursor = connect.cursor()
        cursor.execute("SELECT steps FROM tlist LIMIT 1;")
        
        if result_status == "3":
            counter += 1
            retry_times = 0
        elif retry_times < 3:
            retry_times += 1
            x,y, w = path_points[counter]
            move_to_point(x, y, w)
            return json.dumps({
                "report": "retry to move current index {i} at {l} ({x}, {y})".format(i=counter, l=current_path, x=x, y=y)
            })
        elif retry_times >=3:
            requests.get(SETTINGS["FAIED_URL"]+'/'+current_path)
            cursor.execute("DELETE FROM tlist;")
            logger.debug("请求成功删除所有数据信息")
            connect.commit()
            return ""
        
        # 计数数量和请求数量一致时删除记录，发送成功信息同时将计数变量归零
        steps = cursor.fetchone()[0]
        if steps == counter:
            counter = 0
            requests.get(SETTINGS["STATUS_URL"]+'/'+current_path)
            cursor.execute("DELETE FROM tlist;")
            logger.debug("请求成功删除所有数据信息")
            connect.commit()
            result = {
                "message": "查询到数据，并清除数据"
            }
        else:
            x,y,w = path_points[counter]
            move_to_point(x, y,w)
            result = {
                "message": "查询到数据"
            }
    finally:
        connect.close()
    
    return json.dumps(result)






if __name__ == "__main__":
    # global goal_pub
    app.run(port=SETTINGS["PORT"], host=SETTINGS["HOST"])