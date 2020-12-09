#coding:utf8
"""
Flask API 需要的所有配置信息
"""
# FLASK APP host and port
HOST = "0.0.0.0"
PORT = 5000

# Setup Flask APP DEBUG Status
APP_DEBUG = True

# Setup Flask APP Name
APP_NAME = "main"

# Log Config
LOG_ENABLED = True
LOG_PATH = "log"


# Status API-it's external API
STATUS_URL = 'http://192.168.170.41:8086/face/changeRobotsCheckPointFlag/1'