#coding:utf8
"""
Purpose: 解析配置信息
"""
import configparser
import importlib
from os import path

_parser = configparser.ConfigParser()
_config_file = path.join(path.dirname(__file__), "../../flask.cfg")

assert path.exists(_config_file), f"全局配置文件 'flask.cfg' 缺失"


class Configuration:
    """全局配置解析器
    """
    default_settings = {}
    def __init__(self, extract_settings=True):
        """Initialization

        初始化对象需要生成一个配置 parser 解析器，以及需要根据是否需要提取设置的选项初始化配置

        Args:
        --------
        extract_settings: boolean, 确认是否需要初始化设置

        Properties:
        --------
        parser: 解析配置文件的解析器，是 configparser 的 ConfigParser 对象
        """
        self.parser = _parser
        self.parser.read(_config_file)

        if extract_settings:
            self.parse_all()
    

    def parse_all(self):
        """解析所有配置信息
        """
        settings_file = self.parser.get("settings", "default")
        # import setting mudole
        settings = importlib.import_module(settings_file)

        for key in dir(settings):
            if not key.startswith("__"):
                self.default_settings[key] = getattr(settings, key)


SETTINGS = Configuration().default_settings

del Configuration