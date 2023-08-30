#!/usr/bin/env python
# coding=utf-8
# @Time    : 2023/8/29 17:27
# @Author  : 江斌
# @Software: PyCharm

import argparse
import glob
import os.path
from pathlib import Path


# 使用argparse模块解析命令行参数


def ls():
    """ 列出文件。
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', help='通配符， 例如： ls *.png, ls C:\\*.mp4 ')
    parser.add_argument('-r', "--recursive", action="store_true", help='是否递归')
    args = parser.parse_args()
    p, f = os.path.split(args.pattern)
    p = p or "."
    count = 0
    if args.recursive:
        for each in Path(p).rglob(f):
            print(each)
            count += 1
    else:
        for each in glob.glob(args.pattern):
            print(each)
            count += 1
    if count == 0:
        print("没有找到匹配的文件。")


if __name__ == '__main__':
    ls()
