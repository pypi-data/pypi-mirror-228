"""api工具箱"""

import importlib
from pathlib import Path
from typing import Union, Dict
from collections.abc import Mapping


def import_tools(mod_path: Union[str, Path], params: Dict = None):
    """导入工具"""

    if params is None:
        params = {}

    cls_or_obj = mod_path
    if isinstance(mod_path, str):
        if mod_path.find(".") > -1:
            class_name = mod_path.split(".")[-1]
            mod_name = ".".join(mod_path.split(".")[:-1])
            mod = importlib.import_module(mod_name)
            cls_or_obj = getattr(mod, class_name)
        else:
            cls_or_obj = importlib.import_module(mod_path)

    return cls_or_obj(**params) if isinstance(cls_or_obj, type) else cls_or_obj


def import_by_config(config: Dict):
    """根据配置文件初始化对象

    配置文件格式:
    config = {
        'class': 'vxsched.vxEvent',
        'params': {
            "type": "helloworld",
            "data": {
                'class': 'vxutils.vxtime',
            },
            "trigger": {
                "class": "vxsched.triggers.vxIntervalTrigger",
                "params":{
                    "interval": 10
                }
            }
        }
    }

    """
    if not isinstance(config, Mapping) or "class" not in config:
        return config

    mod_path = config["class"]
    params = {
        k: import_by_config(v) if isinstance(v, Mapping) and "class" in v else v
        for k, v in config.get("params", {}).items()
    }

    if isinstance(mod_path, str):
        if mod_path.find(".") < 0:
            cls_or_obj = importlib.import_module(mod_path)
        else:
            class_name = mod_path.split(".")[-1]
            mod_name = ".".join(mod_path.split(".")[:-1])
            mod = importlib.import_module(mod_name)
            cls_or_obj = getattr(mod, class_name)

    return cls_or_obj(**params) if isinstance(cls_or_obj, type) else cls_or_obj
