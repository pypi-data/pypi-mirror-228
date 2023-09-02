#! /usr/bin/env python
"""
-*- coding: UTF-8 -*-
Project   : restore_dependencies
Author    : Captain
Email     : qing.ji@extremevision.com.cn
Date      : 2023/9/2 10:42
FileName  : src.py
Software  : PyCharm
Desc      : $END$
"""
# 导入必要的模块
import os
import subprocess
import shutil
import zipfile
from loguru import logger


# 定义一个函数，用ldd检查c++程序的依赖，并返回一个列表，包含not found的依赖名
def check_dependencies(program):
    # 执行ldd命令，并获取输出结果
    output = subprocess.check_output(["ldd", program])
    # 定义一个空列表，用于存储not found的依赖名
    not_found = []
    # 遍历输出结果的每一行
    for line in output.splitlines():
        # 如果行中包含"not found"，则提取依赖名，并添加到列表中
        if b"not found" in line:
            # 依赖名一般是第一个单词，以空格分隔
            dep_name = line.split()[0].decode()
            logger.info(f"找不到依赖：{dep_name}")
            not_found.append(dep_name)
    # 返回列表
    return not_found


# 定义一个函数，根据一个文件的内容，查找对应的依赖，并复制到指定的文件夹内，并记录依赖文件的路径，并将还原路径拼接为“cp ./lib/缺失的依赖文件 原依赖文件路径”后存储至cp_dep.txt中
def copy_dependencies(file, folder):
    # 打开文件，并读取所有行
    with open(file, "r") as f:
        lines = f.readlines()
    # 定义一个空列表，用于存储还原命令
    restore_commands = []
    # 遍历每一行，每一行应该是一个依赖名
    for line in lines:
        # 去掉换行符
        dep_name = line.strip()
        try:
            # 使用find命令，在系统中查找该依赖的路径，如果有多个结果，只取第一个
            output = subprocess.check_output(["find", "/", "-name", dep_name])
            logger.info(f"找到依赖：{dep_name}")
            dep_path = output.splitlines()[0].decode()
            # 复制该依赖到指定的文件夹内
            shutil.copy(dep_path, folder)
            logger.info(f"复制依赖：{dep_name}")
            # 拼接还原命令，格式为“cp ./lib/缺失的依赖文件 原依赖文件路径”
            restore_command = "cp ./lib/" + dep_name + " " + dep_path
            # 将还原命令添加到列表中
            restore_commands.append(restore_command)
            logger.info(f"还原命令：{restore_command}")
        except subprocess.CalledProcessError:
            logger.error(f"找不到依赖：{dep_name}")
    # 返回列表
    return restore_commands


# 定义一个函数，根据一个列表，将列表中的每一项写入一个文件中，每一项占一行
def write_list_to_file(lst, file):
    logger.info(f"写入文件：{file}")
    # 打开文件，并写入列表中的每一项
    with open(file, "w") as f:
        for item in lst:
            f.write(item + "\n")


# 定义一个函数，根据一个文件的内容，返回一个列表，包含文件中的每一行
def read_list_from_file(file):
    logger.info(f"读取文件：{file}")
    # 定义一个空列表，用于存储文件中的每一行
    lst = []
    # 打开文件，并读取所有行
    with open(file, "r") as f:
        lines = f.readlines()
    # 遍历每一行，去掉换行符，并添加到列表中
    for line in lines:
        item = line.strip()
        lst.append(item)
    # 返回列表
    return lst


# 定义一个函数，根据一个列表，执行列表中的每一项，每一项应该是一个还原命令
def execute_list(lst):
    logger.info(f"执行还原命令：{lst}")
    # 遍历列表中的每一项，每一项应该是一个还原命令
    for item in lst:
        # 执行该命令
        os.system(item)


# 定义一个函数，根据一个文件夹，将文件夹内的所有文件压缩为一个zip文件
def zip_folder(folder, zip_file):
    logger.info(f"压缩文件夹：{folder}")
    # 创建一个ZipFile对象，以写入模式打开
    with zipfile.ZipFile(zip_file, "w") as zip:
        # 遍历文件夹内的所有文件
        for file in os.listdir(folder):
            # 拼接文件夹和文件名，得到文件的完整路径
            file_path = os.path.join(folder, file)
            # 将文件写入到zip文件中，使用文件名作为压缩后的名称
            zip.write(file_path, file)


# 定义一个函数，根据一个zip文件，将zip文件内的所有文件解压到一个文件夹中
def unzip_file(zip_file, folder):
    logger.info(f"解压文件：{zip_file}")
    # 创建一个ZipFile对象，以读取模式打开
    with zipfile.ZipFile(zip_file, "r") as zip:
        # 将zip文件内的所有文件解压到指定的文件夹中
        zip.extractall(folder)
