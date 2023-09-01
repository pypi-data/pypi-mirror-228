#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/26 11:49
# @Author  : Adyan
# @File    : Forge.py


import hashlib
import logging
import queue
import random
import re
import threading
import urllib.parse
import cpca

from faker import Faker
from requests import sessions

fake = Faker()


def ranstr(num):
    # 猜猜变量名为啥叫 H
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(num):
        salt += random.choice(H)
    return salt


def hex_md5(cookie, ti, formdata):
    try:
        string = f'{re.findall("_m_h5_tk=(.*?)_", cookie)[0]}&{ti}&12574478&{formdata.get("data")}'
        m = hashlib.md5()
        m.update(string.encode('UTF-8'))
        return m.hexdigest()
    except:
        logging.warning(f'参数错误：{[cookie, formdata]}')


def url_code(string, code='utf-8'):
    if code == "utf-8" or code == "gbk":
        quma = str(string).encode(code)
        bianma = urllib.parse.quote(quma)
    if code == "ascii":
        bianma = string.encode('unicode_escape').decode(code)
    return bianma


def gen_headers(string):
    lsl = []
    headers = {}
    for l in string.split('\n')[1:-1]:
        l = l.split(': ')
        lsl.append(l)
    for x in lsl:
        headers[str(x[0]).strip('    ')] = x[1]

    return headers


def address(address: list):
    area_list = cpca.transform(address).values.tolist()[0]
    data = {"province": area_list[0], "city": area_list[1], "district": area_list[2]}
    while None in area_list:
        area_list.remove(None)
    data["address"] = "".join(area_list[:-1])
    return data


def arabic_to_chinese(number):
    chinese_numerals = {
        0: '零',
        1: '一',
        2: '二',
        3: '三',
        4: '四',
        5: '五',
        6: '六',
        7: '七',
        8: '八',
        9: '九'
    }

    units = ['', '十', '百', '千']
    large_units = ['', '万', '亿', '兆']

    # 将整数转换为字符串，以便于处理每个数字
    num_str = str(number)
    num_len = len(num_str)

    # 初始化结果字符串
    result = ''

    # 从最高位开始循环处理数字
    for i in range(num_len):
        digit = int(num_str[i])
        unit_index = num_len - i - 1

        # 处理零值
        if digit == 0:
            if unit_index % 4 == 0:
                # 如果是一个新的大单位（万、亿、兆等），需要添加大单位
                result += large_units[unit_index // 4]
            elif result[-1] != chinese_numerals[0]:
                # 避免在结果中连续添加多个零
                result += chinese_numerals[digit]
        else:
            result += chinese_numerals[digit] + units[unit_index % 4]

            if unit_index % 4 == 0:
                # 如果是一个新的大单位（万、亿、兆等），需要添加大单位
                result += large_units[unit_index // 4]

    return result


class Headers:

    @classmethod
    def user_agent(cls, mobile_headers):
        while True:
            user_agent = fake.chrome(
                version_from=63, version_to=80,
                build_from=999, build_to=3500
            )
            if "Android" in user_agent or "CriOS" in user_agent:
                if mobile_headers:
                    break
                continue
            else:
                break
        return user_agent

    @classmethod
    def header(
            cls, string=None,
            mobile_headers=None,
            headers={}
    ) -> dict:
        if string:
            headers = gen_headers(string)
            if "\n" not in string:
                headers['Referer'] = string
        headers['user-agent'] = cls.user_agent(mobile_headers)
        return headers


class Decode:
    def __init__(self, string):
        pass

    def discern(self):
        pass


def get(args):
    # time.sleep(random.randint(1,3))
    method = args.pop("method")
    url = args.pop("url")
    with sessions.Session() as session:
        return session.request(method=method, url=url, **args)


class ThreadManager(object):
    def __init__(self, work_num: list, func=None, **kwargs):
        self.work_queue = queue.Queue()  # 任务队列
        self.threads = []  # 线程池
        self.func = func
        self.__work_queue(work_num, kwargs)  # 初始化任务队列，添加任务
        self.__thread_pool(len(work_num))  # 初始化线程池，创建线程

    def __thread_pool(self, thread_num):
        """
        初始化线程池
        :param thread_num:
        :return:
        """
        for i in range(thread_num):
            # 创建工作线程(线程池中的对象)
            self.threads.append(Work(self.work_queue))

    def __work_queue(self, jobs_num, kwargs):
        """
        初始化工作队列
        :param jobs_num:
        :return:
        """
        for i in jobs_num:
            #  添加一项工作入队
            if self.func:
                self.work_queue.put((self.func, {'data': i, **kwargs}))
            else:
                self.work_queue.put((get, i))

    def wait_allcomplete(self):
        """
        等待所有线程运行完毕
        :return:
        """
        respone = []
        for item in self.threads:
            item.join()
            respone.append(item.get_result())
        return respone


class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.result = None
        self.work_queue = work_queue
        self.start()

    def run(self) -> None:
        # 死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                do, args = self.work_queue.get(block=False)  # 任务异步出队，Queue内部实现了同步机制
                self.result = do(args)
                # print(self.result.text)
                self.work_queue.task_done()  # 通知系统任务完成
            except:
                break

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
