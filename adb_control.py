#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import time

def run_adb_command(command):
    """
    执行ADB命令并返回结果
    """
    try:
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
        start_x, start_y: 起始点坐标
        end_x, end_y: 结束点坐标
        duration: 滑动持续时间(毫秒)
    """
    command = f"shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}"
    print(f"执行滑动操作: 从 ({start_x}, {start_y}) 到 ({end_x}, {end_y})")
    return run_adb_command(command)

def tap_screen(x, y):
    """
    点击屏幕上的指定坐标
    
    参数:
        x, y: 点击坐标
    """
    command = f"shell input tap {x} {y}"
    print(f"执行点击操作: 坐标 ({x}, {y})")
    return run_adb_command(command)

def check_device_connected():
    """
    检查是否有设备连接
    """
    result = run_adb_command("devices")
    if result and len(result.strip().split('\n')) > 1:
        return True
    else:
        print("没有检测到已连接的设备，请确保您的设备已连接并已启用USB调试模式")
        return False

def main():
    # 检查设备连接
    if not check_device_connected():
        return
    
    # 等待设备准备就绪
    print("等待设备准备就绪...")
    time.sleep(2)
    
    # 执行滑动操作 (从屏幕中间向上滑动)
    # 假设屏幕分辨率为1080x1920，可以根据实际设备调整
    print("\n执行滑动操作...")
    swipe_screen(1000, 1400, 540, 1400)
    
    # 等待一段时间
    time.sleep(1)
    
    # 执行点击操作 (点击屏幕中间位置)
    print("\n执行点击操作...")
    tap_screen(1126, 1466)
    time.sleep(1)
    tap_screen(770, 2300)
    time.sleep(1)
    tap_screen(939, 2525)
    print("\n操作完成!")

if __name__ == "__main__":
    for i in range(300):
        main()