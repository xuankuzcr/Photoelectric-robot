#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 15:37:10 2019

@author: Whisdangist
"""

import cv2
import sys
import time
import serial
import numpy as np
import os, sys
import multiprocessing as mp

def mkdir(path):
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录

        os.makedirs(path) 
 
        #print path+' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        #print path+' 目录已存在'
        return False



def color_detect(q_command, q_result):
    is_show = 0
    DETECT_TIMES = 30

    FRAME_WIDTH = 352
    FRAME_HEIGHT = 288

    detect_cnt = 0
    
    red_lower_1 = np.array([0, 43, 46])
    red_upper_1 = np.array([10, 255, 255])
    red_lower_2 = np.array([156, 43, 46])
    red_upper_2 = np.array([180, 255, 255])
    green_lower = np.array([35, 43, 46])
    green_upper = np.array([87, 255, 255])
    blue_lower = np.array([100, 100, 100])
    blue_upper = np.array([124, 255, 255])
    white_lower = np.array([0, 0, 160])
    white_upper = np.array([180, 30, 255])
    black_lower = np.array([0, 30, 0])
    black_upper = np.array([180, 255, 110])

    cap_grab = cv2.VideoCapture(0)
    cap_grab.set(3, FRAME_WIDTH)  # cv2.CAP_PROP_FRAME_WIDTH
    cap_grab.set(4, FRAME_HEIGHT)  # cv2.CAP_PROP_FRAME_HEIGHT
    cap_grab.set(5, 30)  # cv2.CAP_PROP_FPS


    detect_times = -1
    color = ""
    color_score = {
        "b": 0,
        "g": 0,
        "r": 0,
        "w": 0,
        "k": 0
    }

    # start_time = time.time()

    while cap_grab.isOpened():
        # if int(time.time() - start_time) % 10 == 0:
        #     command = ord('s')
        if not q_command.empty():
            command = q_command.get_nowait()
            if command == 1:  # start
                #q_result.put_nowait(chr(0xAA))
                detect_cnt = detect_cnt + 1
                detect_times = DETECT_TIMES
            elif command == 2:
                detect_times = -1

        if detect_times == 0:  # end
            #q_result.put_nowait(chr(0x63))
            if color_score["g"] > color_score["b"]:
                color = "g"
            else:
                color = "b"
            if color_score["r"] > color_score[color]:
                color = "r"
            if color_score["w"] > color_score[color]:
                color = "w"
            if color_score["k"] > color_score[color]:
                color = "k"
            q_result.put_nowait(color)

            #print color

            detect_times = -1
            color_score["b"] = 0
            color_score["g"] = 0
            color_score["r"] = 0
            color_score["w"] = 0
            color_score["k"] = 0

        if detect_times > 0:
            detect_times = detect_times - 1
            ret_grab, frame_grab = cap_grab.read()
            hsv_grab = cv2.cvtColor(frame_grab, cv2.COLOR_BGR2HSV)
            mkpath="/home/pi/Desktop/detect/Ori_%d" % detect_cnt
            #mkdir(mkpath)
            #cv2.imwrite("/home/pi/Desktop/detect/Ori_%d/photo_%d.jpeg"%(detect_cnt,detect_times),frame_grab,[int(cv2.IMWRITE_JPEG_QUALITY),95])

            #mkpath_diff="/home/pi/Desktop/detect/Ori_%d" % (detect_cnt)

            # 黑色
            
            #mkdir(mkpath_diff+"/black")
            mask_bg_n_black = cv2.inRange(hsv_grab, black_lower, black_upper)
            
            #cv2.imwrite("/home/pi/Desktop/detect/Ori_%d/balck/photo_%d.jpeg"%(detect_cnt,detect_times),mask_bg_n_black,[int(cv2.IMWRITE_JPEG_QUALITY),95])
            
            # 白色
           
            #mkdir(mkpath_diff+"/white")
            mask_bg_n_white = cv2.inRange(hsv_grab, white_lower, white_upper)
            
            #cv2.imwrite("/home/pi/Desktop/detect/Ori_%d/white/photo_%d.jpeg"%(detect_cnt,detect_times),mask_bg_n_white,[int(cv2.IMWRITE_JPEG_QUALITY),95])
            # 蓝色
           
            #mkdir(mkpath_diff+"/blue")
            mask_bg_n_blue = cv2.inRange(hsv_grab, blue_lower, blue_upper)

            #cv2.imwrite("/home/pi/Desktop/detect/Ori_%d/blue/photo_%d.jpeg"%(detect_cnt,detect_times),mask_bg_n_blue,[int(cv2.IMWRITE_JPEG_QUALITY),95])
            
            # 绿色
            #mkdir(mkpath_diff+"/green")
            mask_bg_n_green = cv2.inRange(hsv_grab, green_lower, green_upper)
            
            #cv2.imwrite("/home/pi/Desktop/detect/Ori_%d/bgreen/photo_%d.jpeg"%(detect_cnt,detect_times),mask_bg_n_green,[int(cv2.IMWRITE_JPEG_QUALITY),95])
            
            # 红色
            #mkdir(mkpath_diff+"/green")
            mask_bg_n_red_1 = cv2.inRange(hsv_grab, red_lower_1, red_upper_1)
            mask_bg_n_red_2 = cv2.inRange(hsv_grab, red_lower_2, red_upper_2)
            mask_bg_n_red = cv2.bitwise_or(mask_bg_n_red_1, mask_bg_n_red_2)
            
            #cv2.imwrite("/home/pi/Desktop/detect/Ori_%d/bgreen/photo_%d.jpeg"%(detect_cnt,detect_times),mask_bg_n_red,[int(cv2.IMWRITE_JPEG_QUALITY),95])
            
            color_score["k"] += mask_bg_n_black.sum() / 255
            color_score["w"] += mask_bg_n_white.sum() / 255
            color_score["b"] += mask_bg_n_blue.sum() / 255
            color_score["g"] += mask_bg_n_green.sum() / 255
            color_score["r"] += mask_bg_n_red.sum() / 255
            # cv2.waitKey(500)

            if is_show == 1:
                
                print "black: %d, white: %d, blue: %d, green: %d, red: %d" % (mask_bg_n_black.sum() / 255, mask_bg_n_white.sum() / 255, mask_bg_n_blue.sum() / 255, mask_bg_n_green.sum() / 255, mask_bg_n_red.sum() / 255)
            
                cv2.namedWindow('Frame_Org', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('Frame_Org', frame_grab)
               
                # 黑色
                cv2.namedWindow('Frame_BG_Black', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('Frame_BG_Black', mask_bg_n_black)
                
                # 白色
                frame_bg_white = cv2.bitwise_and(frame_grab, frame_grab, mask=mask_bg_n_white)
                cv2.namedWindow('Frame_BG_White', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('Frame_BG_White', frame_bg_white)

                # 蓝色
                frame_bg_blue = cv2.bitwise_and(frame_grab, frame_grab, mask=mask_bg_n_blue)
                cv2.namedWindow('Frame_BG_Blue', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('Frame_BG_Blue', frame_bg_blue)

                # 绿色
                frame_bg_green = cv2.bitwise_and(frame_grab, frame_grab, mask=mask_bg_n_green)
                cv2.namedWindow('Frame_BG_Green', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('Frame_BG_Green', frame_bg_green)

                # 红色
                frame_bg_red = cv2.bitwise_and(frame_grab, frame_grab, mask=mask_bg_n_red)
                cv2.namedWindow('Frame_BG_Red', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('Frame_BG_Red', frame_bg_red)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    break


def circle_detect(q_command, q_result):
    FRAME_WIDTH = 352
    FRAME_HEIGHT = 288

    cap_grab = cv2.VideoCapture(2)
    cap_grab.set(3, FRAME_WIDTH)  # cv2.CAP_PROP_FRAME_WIDTH
    cap_grab.set(4, FRAME_HEIGHT)  # cv2.CAP_PROP_FRAME_HEIGHT
    cap_grab.set(5, 30)  # cv2.CAP_PROP_FPS

    phase = 0
    current_pos = 0
    current_color = ''
    black_pos = 0

    # from std_pos_from_pic import std_pos, std_pos_put
    from std_pos_from_array import std_pos, std_pos_put

    black_times = 0
    while cap_grab.isOpened():
        command = 0
        save_photo = False
        send_offset = False
        key = ""
        x_origin = y_origin = r = 0
        if not q_command.empty():
            command = q_command.get_nowait()
            command_type = command >> 4
            command_content = command & 0x0F
            if command_type == 0:  # from uart
                if command_content == 0:
                    phase = 0
                    current_pos = 0
                    current_color = ''
                if command_content == 1:
                    save_photo = True
                if command_content == 2:
                    send_offset = True
                    save_photo = True
                    current_pos += 1
                    if current_pos == 5:
                        current_pos = black_pos
                        current_color = "black"
                    key = str(current_pos)
                    try:
                        [x_origin, y_origin] = std_pos[key]
                    except Exception as e:
                        print e
                    print "current std_pos[" + key + "] x_origin=%d y_origin=%d" % (x_origin, y_origin)
                if command_content == 3:
                    send_offset = True
                    save_photo = True
                    key = current_color + str(phase)
                    try:
                        [x_origin, y_origin] = std_pos_put[key]
                    except Exception as e:
                        print e
                    print "current std_pos_put[" + key + "] x_origin=%d y_origin=%d" % (x_origin, y_origin)
                if command_content == 4:
                    phase = 1
            if command_type == 1:  # from color_detect process
                if command_content == 1:  # red
                    current_color = "red"
                    black_times = 0
                if command_content == 2:  # green
                    current_color = "green"
                    black_times = 0
                if command_content == 3:  # blue
                    current_color = "blue"
                    black_times = 0
                if command_content == 4:  # white
                    current_color = "white"
                    black_times = 0
                if command_content == 5:  # black
                    current_color = "black"
                    black_times += 1
                    if phase == 0 and black_times == 4:
                        black_pos = current_pos
                        print "black_pos: %d" % current_pos


        ret_grab, frame_grab = cap_grab.read()
        gray_grab = cv2.cvtColor(frame_grab, cv2.COLOR_RGB2GRAY)
        circles = cv2.HoughCircles(gray_grab, cv2.cv.CV_HOUGH_GRADIENT, 2, 100, maxRadius=100)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            x_grab, y_grab, r = circles[0]
            offset_x = x_grab - x_origin
            offset_y = y_grab - y_origin
        else:
            offset_x = offset_y = r = 0

        file_num = 0
        if save_photo:
            try:
                file_num = len(os.listdir("/home/pi/Desktop/images/origin")) +1
                cv2.imwrite("/home/pi/Desktop/images/origin/%.3d.jpg" % file_num, frame_grab)
                print "Saving image to /home/pi/Desktop/images/origin/%.3d.jpg" % file_num
                if r != 0:
                    cv2.circle(frame_grab, (x_grab, y_grab), r, (0, 255, 0), 4)
                    cv2.imwrite("/home/pi/Desktop/images/circled/%.3d.jpg" % file_num, frame_grab)
                    print "Saving image to /home/pi/Desktop/images/circled/%.3d.jpg" % file_num
                print "%d %d %d" % (offset_x, offset_y, r)
            except Exception as e:
                print e

        if send_offset:
            try:
                q_result.put_nowait("[data]%d %d %d" % (offset_x, offset_y, r))
                with open("/home/pi/Desktop/images/images_info.txt", "a") as fo:
                    fo.write("%.3d.jpg  offset_x: %d\toffset_y: %d\t [%s]\n" % (file_num, offset_x, offset_y, key))
            except Exception as e:
                print e

        time.sleep(0.01)


def uart_communication(q_color_detect_command, q_color_detect_result, q_circle_detect_command, q_circle_detect_result):
    ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=2)
    ser.flushInput()
    ser.flushOutput()
    ser.write(chr(0xFF))
    print "0xFF"
    time.sleep(1)


    while True:
        try:
            n = ser.inWaiting()
            if n > 0:
                uart_rx_data = ser.read(n)
                command = ord(uart_rx_data[0])
                command_type = command >> 4
                command_content = command & 0x0F
                if command_type == 1:
                    if command_content == 1:
                        ser.write(chr(0xFF))
                        q_circle_detect_command.put_nowait(0)
                        q_color_detect_command.put_nowait(0)
                        print "0xFF"
                    if command_content == 2:
                        os.system("sudo poweroff")
                        sys.exit()
                if command_type == 2:
                    q_color_detect_command.put_nowait(command_content)
                if command_type == 3:
                    q_circle_detect_command.put_nowait(command_content)

            if not q_color_detect_result.empty():
                res = q_color_detect_result.get_nowait()
                ser.write(res)

                command = 0x10
                if res == 'r':
                    command += 1
                if res == 'g':
                    command += 2
                if res == 'b':
                    command += 3
                if res == 'w':
                    command += 4
                if res == 'k':
                    command += 5
                q_circle_detect_command.put_nowait(command)
                
                print "[color]" + res

            if not q_circle_detect_result.empty():
                res = q_circle_detect_result.get_nowait()
                if res[:6] == "[data]":
                    [offset_x, offset_y, r] = [int(s) for s in res[6:].split()]
                    x = (int(offset_x*50/68) & 0x7F) + (0x80 if offset_x < 0 else 0)
                    y = (int(offset_y*50/68) & 0x7F) + (0x80 if offset_y < 0 else 0)
                    ser.write(chr(x))
                    ser.write(chr(y))
                    print "[circle][offset] x: %d y: %d" % (offset_x*50/68, offset_y*50/68)
                print "[circle]" + res
                
        except:
            continue


if __name__ == "__main__":

    q_color_detect_command = mp.Queue()
    q_color_detect_result = mp.Queue()
    q_circle_detect_command = mp.Queue()
    q_circle_detect_result = mp.Queue()

    p_uart_communication = mp.Process(target=uart_communication, args=(q_color_detect_command, q_color_detect_result, q_circle_detect_command, q_circle_detect_result))
    p_color_detect = mp.Process(target=color_detect, args=(q_color_detect_command, q_color_detect_result))
    p_circle_detect = mp.Process(target=circle_detect, args=(q_circle_detect_command, q_circle_detect_result))

    p_uart_communication.start()
    p_color_detect.start()
    p_circle_detect.start()
