#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ADB控制脚本 - 用于通过ADB命令控制Android设备

该脚本提供了一系列函数，用于执行常见的ADB操作，如滑动屏幕、点击屏幕等。
主要用于自动化测试或重复性操作。
"""

import subprocess
import time
import sys


def run_adb_command(command):
    """
    执行ADB命令并返回结果
    
    参数:
        command (str): 要执行的ADB命令（不包含'adb'前缀）
        
    返回:
        str: 命令执行的输出结果
        None: 如果命令执行失败
    """
    try:
        # 使用subprocess执行ADB命令，并捕获标准输出和错误输出
        result = subprocess.run(f"adb {command}", shell=True, check=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"执行ADB命令时出错: {e}")
        print(f"错误输出: {e.stderr}")
        return None


def swipe_screen(start_x, start_y, end_x, end_y, duration=300):
    """
    在屏幕上从起始坐标滑动到结束坐标
    
    参数:
        start_x (int): 起始点X坐标
        start_y (int): 起始点Y坐标
        end_x (int): 结束点X坐标
        end_y (int): 结束点Y坐标
        duration (int): 滑动持续时间(毫秒)，默认300ms
        
    返回:
        str: 命令执行的输出结果
        None: 如果命令执行失败
    """
    command = f"shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}"
    print(f"执行滑动操作: 从 ({start_x}, {start_y}) 到 ({end_x}, {end_y})")
    return run_adb_command(command)


def tap_screen(x, y):
    """
    点击屏幕上的指定坐标
    
    参数:
        x (int): 点击位置的X坐标
        y (int): 点击位置的Y坐标
        
    返回:
        str: 命令执行的输出结果
        None: 如果命令执行失败
    """
    command = f"shell input tap {x} {y}"
    print(f"执行点击操作: 坐标 ({x}, {y})")
    return run_adb_command(command)


def check_device_connected():
    """
    检查是否有设备连接到ADB
    
    返回:
        bool: 如果有设备连接则返回True，否则返回False
    """
    result = run_adb_command("devices")
    # 检查输出结果中是否包含设备信息（至少有两行，第一行是标题）
    if result and len(result.strip().split('\n')) > 1:
        # 提取设备列表（跳过第一行标题）
        devices = [line.split('\t')[0] for line in result.strip().split('\n')[1:] if line.strip()]
        print(f"检测到 {len(devices)} 个已连接设备: {', '.join(devices)}")
        return True
    else:
        print("没有检测到已连接的设备，请确保您的设备已连接并已启用USB调试模式")
        return False


def input_text(text):
    """
    在当前焦点位置输入文本
    
    参数:
        text (str): 要输入的文本
        
    返回:
        str: 命令执行的输出结果
        None: 如果命令执行失败
    """
    # 对特殊字符进行转义
    escaped_text = text.replace(" ", "%s").replace("'", "\'").replace("\"", "\\\"")
    command = f"shell input text '{escaped_text}'"
    print(f"执行文本输入: '{text}'")
    return run_adb_command(command)


def press_key(keycode):
    """
    模拟按键操作
    
    参数:
        keycode (int): 按键代码，例如4表示返回键，3表示HOME键
        
    返回:
        str: 命令执行的输出结果
        None: 如果命令执行失败
    """
    command = f"shell input keyevent {keycode}"
    print(f"执行按键操作: keycode {keycode}")
    return run_adb_command(command)


def main():
    """
    主函数 - 执行一系列ADB操作
    """
    # 检查设备连接
    if not check_device_connected():
        return
    
    try:
        # 等待设备准备就绪
        print("等待设备准备就绪...")
        time.sleep(2)
        
        # 执行滑动操作 (从屏幕右侧向左滑动)
        # 假设屏幕分辨率为1080x1920，可以根据实际设备调整
        print("\n执行滑动操作...")
        swipe_screen(1000, 1400, 540, 1400)
        
        # 等待动画完成
        time.sleep(1)
        
        # 执行点击操作
        print("\n执行点击操作...")
        tap_screen(1126, 1466)
        time.sleep(1)
        tap_screen(770, 2300)
        time.sleep(1)
        tap_screen(939, 2525)
        
        print("\n操作完成!")
        
    except KeyboardInterrupt:
        print("\n操作被用户中断!")
        sys.exit(0)
    except Exception as e:
        print(f"\n执行过程中出错: {e}")
        return


if __name__ == "__main__":
    # 设置循环次数，可以通过命令行参数修改
    repeat_count = 300
    if len(sys.argv) > 1:
        try:
            repeat_count = int(sys.argv[1])
        except ValueError:
            print(f"无效的循环次数参数: {sys.argv[1]}，使用默认值: {repeat_count}")
    
    print(f"将执行 {repeat_count} 次操作循环")
    
    try:
        for i in range(repeat_count):
            print(f"\n===== 执行第 {i+1}/{repeat_count} 次操作 =====")
            main()
            # 每次操作之间稍作暂停
            if i < repeat_count - 1:  # 最后一次循环后不需要等待
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n程序被用户中断!")
    
    print("程序执行完毕!")