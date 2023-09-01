#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/2 15:22
# @Author  : Adyan
# @File    : function.py


import json
import os
import re
import time
from datetime import datetime
from typing import Union
import fitz
import pytesseract
from PIL import Image

import pytz

cntz = pytz.timezone("Asia/Shanghai")
remap = {
    ord('\t'): '', ord('\f'): '',
    ord('\r'): '', ord('\n'): '',
}


class Fun:

    @classmethod
    def merge_dic(cls, dic: dict, lst: list):
        """
        合并多个dict
        :param dic: dict - 主dict
        :param lst: list - 多个字典列表方式传入
        :return:
        """
        for d in lst:
            for k, v in d.items():
                if v:
                    dic[k] = v
        return dic

    @classmethod
    def del_html(cls, html: str):
        for i in re.findall(r"<(.*?)>", html):
            html = html.replace(f'<{i}>', '')
        return html.translate({**remap, ord(' '): ''})

    @classmethod
    def re_dict(cls, re_pattern: dict and list, string_, ) -> dict:
        if isinstance(re_pattern, dict):
            fun = lambda x, y: y if ' ' in x else y.replace(' ', '')
            return {
                key: cls.compute_res(
                    re_pattern=re.compile(scale),
                    string_=fun(scale, string_.translate(remap))
                )
                for key, scale in re_pattern.items()
            }
        if isinstance(re_pattern, list):
            dic = {}
            for index in range(len(re_pattern)):
                string = string_
                if isinstance(string_, list):
                    string = string_[index]
                if isinstance(string, int):
                    string = string_[string]
                dict2 = cls.re_dict(re_pattern[index], string)
                for k, v in dict2.items():
                    if k in dic.keys():
                        values = dic.get(k)
                        if values and v:
                            dict2[k] = [values, v]
                        if values and v is None:
                            dict2[k] = values
                dic = {**dic, **dict2}
            return dic

    @classmethod
    def compute_res(cls, re_pattern: re.Pattern, string_=None):
        data = re_pattern.findall(string_)
        if data:
            try:
                return json.loads(data[0])
            except:
                return data[0]
        else:
            return None

    @classmethod
    def find(cls, target: str, dict_data: dict, index=None, ):
        result = []
        result_add = lambda x: [result.insert(0, d) for d in cls.find(target, x)]

        if isinstance(dict_data, dict):
            for key, value in dict_data.items():
                if key == target and value not in result:
                    result.insert(0, value)
                result_add(value)

        if isinstance(dict_data, (list, tuple)):
            for data in dict_data:
                result_add(data)

        if isinstance(index, int):
            try:
                return result[index]
            except:
                return None
        return result

    @classmethod
    def timeconvert(cls, times, timestamp=None, int_time=None) -> Union[int, str]:
        remap = {
            ord('年'): '-', ord('月'): '-',
            ord('日'): ' ', ord('/'): '-',
            ord('.'): '-',
        }
        if isinstance(times, str):
            times = times.translate(remap)
        if int_time:
            return int(time.mktime(time.strptime(times, int_time)))
        if isinstance(times, str):
            times = int(time.mktime(time.strptime(times, "%Y-%m-%d %H:%M:%S")))
        if timestamp:
            times = times + timestamp
        return str(datetime.fromtimestamp(times, tz=cntz))

    @classmethod
    def is_None(cls, dic: dict) -> dict:
        """
        :param dic: dict
        :return: 返回字典中值是None的键值对
        """
        return {
            k: v
            for k, v in dic.items()
            if not v
        }

    @classmethod
    def del_key(cls, dic, del_keys=None, is_None=None):
        if isinstance(dic, list):
            return [cls.del_key(item, del_keys, is_None) for item in dic]
        if isinstance(dic, dict):
            if is_None:
                del_keys = Fun.is_None(dic).keys()
            new_dict = {}
            for key in dic.keys():
                if key not in del_keys:
                    new_dict[key] = cls.del_key(dic[key], del_keys, is_None)
            return new_dict
        else:
            return dic

    def extract_text_from_image_and_pdf(cls, path, pdf_file):
        text = ""
        with fitz.open(f"{path}{pdf_file}") as pdf_document:
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                text += page.get_text()
                page = pdf_document[page_num]
                images = page.get_images(full=True)
                for img_index, img in enumerate(images):
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_data = base_image["image"]
                    image_filename = f"page_{page_num + 1}_image_{img_index + 1}.png"
                    image_path = os.path.join(path, image_filename)
                    text += cls.extract_text_from_image(image_path, image_data)
        return text

    def extract_text_from_image(cls, image_path, image_data):
        with open(image_path, "wb") as img_file:
            img_file.write(image_data)
        image = Image.open(image_path)
        return pytesseract.image_to_string(image, lang='chi_sim')
