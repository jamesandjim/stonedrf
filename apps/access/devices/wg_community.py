#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-05-28 15:11
# @Author  : James
# @Site    :
# @File    : mj_communication.py
# @Software: PyCharm

import socket


# 定义短报文包的类
class WGPaketShort:
    ''' 短报文类，实现发送短报文和收到返回短报文的功能 '''

    # 定义全局类变量
    Type = 0x17
    ControllerPort = 60000
    SpecialFlag = 0x55AAAA55
    WGPacketSize = 64

    def __init__(self, ip, dev_sn, func_id):

        self.udp_data = bytearray(WGPaketShort.WGPacketSize)
        self.udp_data[0] = WGPaketShort.Type
        self.udp_data[1] = func_id
        self.udp_data[4:8] = dev_sn.to_bytes(4, byteorder='little')
        if func_id == 0x94 or func_id == 0x96:
            self.ip = '255.255.255.255'
        else:
            self.ip = ip

        self.rec_data = None

    # 发送短报文功能
    def send_data(self):
        # 建立UDP连接
        udp_cli_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 定义UDP数据包

        ADDR = (self.ip, WGPaketShort.ControllerPort)
        # 设置UDP的选项：允许其发送广播包（地址255.255.255.255），第一个参数代表当前UDP，第二个是表示套接字广播选项，第三个表示为真
        udp_cli_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        try:
            udp_cli_socket.sendto(self.udp_data, ADDR)
            self.rec_data, ADDR = udp_cli_socket.recvfrom(WGPaketShort.WGPacketSize)

            b = self.rec_data[4:8]
            # 将字节转换为INT，格式为低位在前
            i = int.from_bytes(b, byteorder='little')

            if len(self.rec_data) == WGPaketShort.WGPacketSize:
                if self.rec_data[0] == self.udp_data[0] and self.rec_data[1] == self.udp_data[1]:
                    #x = self.rec_data
                    udp_cli_socket.close()
                    return True
                else:
                    udp_cli_socket.close()
                    return False
            else:
                udp_cli_socket.close()
                return False

        except OSError:
            print(OSError.errno)
            udp_cli_socket.close()














