import os

import numpy as np

from AutoWSGR.utils.api_image import crop_image
from AutoWSGR.utils.io import yaml_to_dict

POS = yaml_to_dict(os.path.join(os.path.dirname(__file__), "relative_location.yaml"))


def image_to_number(image: np.ndarray):
    """根据图片返回数字

    Args:
        image (np.ndarray): 图片

    Returns:
        int, None: 存在则返回数字,否则为 None
    """
    result = pytesseract.image_to_string(image).strip()
    if len(result) == 0:
        return None
    scale = 1

    if "K" in result:
        result = result[:-2]
        scale = 1000
    if "M" in result:
        result = result[:-2]
        scale = 10**6

    return scale * int(result)


def get_resources(timer):
    """根据 timer 所处界面获取对应资源数据
    部分 case 会没掉,请重写
    """
    goto_game_page(timer, "main_page")
    image = timer.screen

    ret = {}
    for key in POS["main_page"]["resources"]:
        image_crop = crop_image(image, *POS["main_page"]["resources"][key])
        raw_str = pytesseract.image_to_string(image_crop).strip()  # 原始字符串

        if raw_str[-1] == "K":
            num = raw_str[:-1]
            unit = 1000
        elif raw_str[-1] == "M":
            num = raw_str[:-1]
            unit = 1000000
        else:
            num = raw_str
            unit = 1

        # 容错处理，如果监测出来不是数字则出错了
        try:
            ret[key] = eval(num) * unit
        except NameError:
            print("读取资源失败！")
            quit()

    return ret


def get_loot_and_ship(timer):
    """获取掉落数据"""
    goto_game_page(timer, "map_page")
    timer.update_screen()
    image = timer.screen

    ret = {}
    for key in POS["map_page"]:
        image_crop = crop_image(image, *POS["map_page"][key])
        raw_str = pytesseract.image_to_string(image_crop).strip()  # 原始字符串
        try:
            ret[key] = eval(raw_str.split("/")[0])  # 当前值
            ret[key + "_max"] = eval(raw_str.split("/")[1])  # 最大值
        except:
            print("读今日战利品、捞船失败！")
            print(raw_str)
            quit()

    return ret
