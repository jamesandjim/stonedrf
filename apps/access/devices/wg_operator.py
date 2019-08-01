from .wg_community import WGPaketShort


# 处理MAC 16进制字节，转为16进制的字符串
def formatMac(m):
    if '0x' in m:
        str = m.strip('0x')
        if len(m.strip()) == 3:
            str = '0'+str

        return str


# 搜索控制器
def search_dev():
    list_devs = []
    new_devs = []
    for i in range(60):
        dev = WGPaketShort('255.255.255.255', 0, 0x94)
        # onedev = Device()
        onedev = {}
        ret = dev.send_data()
        if ret is True:
            # 从返回值取得设备的SN,并以低位在前的方式，将字节码转为int
            dev_sn = dev.rec_data[4:8]
            rt_dev_sn = int.from_bytes(dev_sn, byteorder='little')
            # onedev.sn = rt_dev_sn
            onedev['sn'] = rt_dev_sn

            # 从返回的字节中分别取出IP的四个段并生成列表.进行组合，形成IP字符串
            tm_ip = dev.rec_data[8:12]
            list_ip = [str(tm_ip[i]) for i in range(4)]
            rt_dev_ip = '.'.join(list_ip)
            # onedev.ip = rt_dev_ip
            onedev['ip'] = rt_dev_ip

            # 从返回的字节中分别取出掩码的四个段并生成列表.进行组合，形成掩码字符串
            dev_netmask = dev.rec_data[12:16]
            list_netmask = [str(dev_netmask[i]) for i in range(4)]
            rt_dev_netmask = '.'.join(list_netmask)
            # onedev.netmask = rt_dev_netmask
            onedev['netmask'] = rt_dev_netmask

            # 从返回的字节中分别取出网关的四个段并生成列表.进行组合，形成网关字符串
            dev_netgate = dev.rec_data[16:20]
            list_netgate = [str(dev_netgate[i]) for i in range(4)]
            rt_dev_netgate = '.'.join(list_netgate)
            # onedev.netgate = rt_dev_netgate
            onedev['netgate'] = rt_dev_netgate

            # 从返回的字节中分别取出MAC的6个段并生成列表.进行组合，形成MAC字符串
            dev_mac = dev.rec_data[20:26]
            list_mac = [formatMac(str(hex(dev_mac[i]))) for i in range(6)]
            rt_dev_mac = '-'.join(list_mac)
            # onedev.mac = rt_dev_mac
            onedev['mac'] = rt_dev_mac

            dev_ver = dev.rec_data[26:28]
            list_ver = [str(dev_ver[i]) for i in range(2)]
            rt_dev_ver = '.'.join(list_ver)
            # onedev.ver = rt_dev_ver
            onedev['ver'] = rt_dev_ver

            # rt_dev_ver = dev_ver-(dev_ver/16)*6
            # 从返回的字节中分别取出时间的四个段并生成列表.进行组合，形成时间字符串
            dev_date = dev.rec_data[28:32]
            list_date = [str(dev_date[i]) for i in range(4)]
            rt_dev_date = '-'.join(list_date)
            #onedev.ver_date = rt_dev_date

            list_devs.append(onedev)

    for i in list_devs:
        if i not in new_devs:
            new_devs.append(i)

    return new_devs


# 设置设备IP地址
def set_ip(ip, sn, netmask, netgate):
    dev = WGPaketShort('255.255.255.255', sn, 0x96)

    list_ip = ip.split('.')
    bytelist_ip = [int(list_ip[i]) for i in range(4)]
    dev.udp_data[8:12] = bytelist_ip

    list_netmask = netmask.split('.')
    bytelist_netmask = [int(list_netmask[i]) for i in range(4)]
    dev.udp_data[12:16] = bytelist_netmask

    list_netgate = netgate.split('.')
    bytelist_netgate = [int(list_netgate[i]) for i in range(4)]
    dev.udp_data[16:20] = bytelist_netgate

    dev.udp_data[20] = 0x55
    dev.udp_data[21] = 0xAA
    dev.udp_data[22] = 0xAA
    dev.udp_data[23] = 0x55

    dev.send_data()

    return True


# 查询控制器状态
def show_dev_info(ip, sn):
    dev = WGPaketShort(ip, int(sn), 0x20)
    ret = dev.send_data()

    if ret is True and dev.udp_data[4:8] == dev.rec_data[4:8]:
        rt_data = dev.rec_data

        cn_data = byteinfotostr(rt_data)

        return cn_data


# 远程开门
def open_door(ip, sn, doorno):
    dev = WGPaketShort(ip, sn, 0x40)
    dev.udp_data[8] = int(doorno)
    ret = dev.send_data()

    print(dev.rec_data[1])

    if ret is True and dev.udp_data[4:9] == dev.rec_data[4:9]:
        cn_opendoor_ok = '开门成功'

        return {'cn_opendoor_ok':cn_opendoor_ok}

# 读取控制器时间
def get_device_time(ip, sn):
    pass


# 设置控制器时间
def set_device_time(ip, sn):
    pass


# 获取指定索引号的记录[功能号: 0xB0]
def get_record(ip, sn, recordno):
    pass


# 设置已读取过的记录索引号[功能号: 0xB2]
def set_no_readed(ip, sn, recordno):
    pass


# 获取已读取过的记录索引号[功能号: 0xB4]
def get_no_readed(ip, sn):
    pass


# 权限添加或修改[功能号: 0x50]
def add_auth(ip, sn):
    pass


# 权限删除(单个删除)[功能号: 0x52]
def del_auth(ip, sn):
    pass


# 权限清空(全部清掉)[功能号: 0x54]
def del_all_auth(ip, sn):
    pass


# 权限总数读取[功能号: 0x58]
def get_total_auth(ip, sn):
    pass


# 权限查询[功能号: 0x5A]
def get_auth(ip, sn):
    pass


# 获取指定索引号的权限[功能号: 0x5C]
def get_auth_no(ip, sn):
    pass


# 设置门控制参数(在线/延时) [功能号: 0x80]
def set_door_option(ip, sn):
    pass


# 读取门控制参数(在线/延时) [功能号: 0x82]
def get_door_option(ip, sn):
    pass


# 设置接收服务器的IP和端口 [功能号: 0x90]
def set_server_option(ip, sn):
    pass


# 读取接收服务器的IP和端口 [功能号: 0x92]
def get_server_option(ip, sn):
    pass


# 权限按从小到大顺序添加[功能号: 0x56] 适用于权限数过1000
def add_all_auth(ip, sn):
    pass


def byteinfotostr(rec_data):
    '''
    解析0x20查询设备状态返回的字节流，得到设备状态 参数为完整的64字节字节流
    '''

    cn_rec_data = {}
    # 最后一条记录的索引号
    cn_last_no = int.from_bytes(rec_data[8:12], byteorder='little')
    cn_rec_data['cn_last_no'] = cn_last_no

    # 记录类型
    no_type = rec_data[12]
    if no_type == 0:
        cn_no_type = '无记录'
    elif no_type == 1:
        cn_no_type = '刷卡记录'
    elif no_type == 2:
        cn_no_type = '门磁,按钮,设备启动,远程开门记录'
    elif no_type == 3:
        cn_no_type = '报警记录'
    else:
        cn_no_type = '未知记录'

    cn_rec_data['cn_no_type'] = cn_no_type

    # 开门有效性
    yn = rec_data[13]
    if yn == 1:
        cn_yn = '正常通过'
    else:
        cn_yn = '未通过'

    cn_rec_data['cn_yn'] = cn_yn

    # 门号
    door_no = rec_data[14]
    if door_no == 1:
        cn_door_no = '一号门'
    elif door_no == 2:
        cn_door_no = '二号门'
    elif door_no == 3:
        cn_door_no = '三号门'
    elif door_no == 4:
        cn_door_no = '四号门'

    cn_rec_data['cn_door_no'] = cn_door_no

    # 进门还是出门
    in_out = rec_data[15]
    if in_out == 1:
        cn_in_out = '进门'
    else:
        cn_in_out = '出门'

    cn_rec_data['cn_in_out'] = cn_in_out

    # 卡号或编号
    cn_card_no = int.from_bytes(rec_data[16:20], byteorder='little')

    cn_rec_data['cn_card_no'] = cn_card_no

    # 刷卡时间
    temp1_card_time = []
    temp_card_time = [hex(i) for i in rec_data[20:27]]
    for x in temp_card_time:
        if len(x) == 4:
            temp1_card_time.append(x.replace('0x', ''))
        else:
            temp1_card_time.append(x.replace('0x', '0'))

    cn_card_time = ''.join(temp1_card_time)

    cn_rec_data['cn_card_time'] = cn_card_time

    # 刷卡记录说明
    temp_card_desc = rec_data[27]
    if temp_card_desc == 1:
        cn_card_desc = '刷卡开门'
    elif temp_card_desc == 5:
        cn_card_desc = '刷卡禁止通过: 电脑控制'
    elif temp_card_desc == 6:
        cn_card_desc = '刷卡禁止通过: 没有权限'
    elif temp_card_desc == 7:
        cn_card_desc = '刷卡禁止通过: 密码不对'
    elif temp_card_desc == 8:
        cn_card_desc = '刷卡禁止通过: 反潜回'
    elif temp_card_desc == 9:
        cn_card_desc = '刷卡禁止通过: 多卡'
    elif temp_card_desc == 10:
        cn_card_desc = '刷卡禁止通过: 首卡'
    elif temp_card_desc == 11:
        cn_card_desc = '刷卡禁止通过: 门为常闭'
    elif temp_card_desc == 12:
        cn_card_desc = '刷卡禁止通过: 互锁'
    elif temp_card_desc == 13:
        cn_card_desc = '刷卡禁止通过: 受刷卡次数限制'
    elif temp_card_desc == 15:
        cn_card_desc = '刷卡禁止通过: 卡过期或不在有效时段'
    elif temp_card_desc == 18:
        cn_card_desc = '刷卡禁止通过: 原因不明'
    elif temp_card_desc == 20:
        cn_card_desc = '按钮开门'
    elif temp_card_desc == 23:
        cn_card_desc = '门打开[门磁信号]'
    elif temp_card_desc == 24:
        cn_card_desc = '门关闭[门磁信号]'
    elif temp_card_desc == 25:
        cn_card_desc = '超级密码开门'
    elif temp_card_desc == 28:
        cn_card_desc = '控制器上电'
    elif temp_card_desc == 29:
        cn_card_desc = '控制器复位'
    elif temp_card_desc == 31:
        cn_card_desc = '按钮不开门: 强制关门'
    elif temp_card_desc == 32:
        cn_card_desc = '按钮不开门: 门不在线'
    elif temp_card_desc == 33:
        cn_card_desc = '按钮不开门: 互锁'
    elif temp_card_desc == 34:
        cn_card_desc = '胁迫报警'
    elif temp_card_desc == 37:
        cn_card_desc = '门长时间未关报警[合法开门后]'
    elif temp_card_desc == 38:
        cn_card_desc = '强行闯入报警'
    elif temp_card_desc == 39:
        cn_card_desc = '火警'
    elif temp_card_desc == 40:
        cn_card_desc = '强制关门'
    elif temp_card_desc == 41:
        cn_card_desc = '防盗报警'
    elif temp_card_desc == 42:
        cn_card_desc = '烟雾煤气温度报警'
    elif temp_card_desc == 43:
        cn_card_desc = '紧急呼救报警'
    elif temp_card_desc == 44:
        cn_card_desc = '操作员远程开门'
    elif temp_card_desc == 45:
        cn_card_desc = '发卡器确定发出的远程开门'
    else:
        cn_card_desc = '未知'

    cn_rec_data['cn_card_desc'] = cn_card_desc

    # 门状态
    dev_sn = str(int.from_bytes(rec_data[4:8], byteorder='little'))

    cn_doorstatus1 = ''
    cn_doorstatus2 = ''
    cn_doorstatus3 = ''
    cn_doorstatus4 = ''

    if dev_sn[0] == '1':
        temp_doorstatus1 = rec_data[28]
        if temp_doorstatus1 == 1:
            cn_doorstatus1 = '一号门已打开'
        else:
            cn_doorstatus1 = '一号门已关闭'

    elif dev_sn[1] == '2':
        temp_doorstatus1 = rec_data[28]
        temp_doorstatus2 = rec_data[29]
        if temp_doorstatus1 == 1:
            cn_doorstatus1 = '一号门已打开'
        else:
            cn_doorstatus1 = '一号门已关闭'

        if temp_doorstatus2 == 1:
            cn_doorstatus2 = '二号门已打开'
        else:
            cn_doorstatus2 = '二号门已关闭'

    elif dev_sn[4] == '4':
        temp_doorstatus1 = rec_data[28]
        temp_doorstatus2 = rec_data[29]
        temp_doorstatus3 = rec_data[30]
        temp_doorstatus4 = rec_data[31]
        if temp_doorstatus1 == 1:
            cn_doorstatus1 = '一号门已打开'
        else:
            cn_doorstatus1 = '一号门已关闭'

        if temp_doorstatus2 == 1:
            cn_doorstatus2 = '二号门已打开'
        else:
            cn_doorstatus2 = '二号门已关闭'

        if temp_doorstatus3 == 1:
            cn_doorstatus3 = '一号门已打开'
        else:
            cn_doorstatus3 = '一号门已关闭'

        if temp_doorstatus4 == 1:
            cn_doorstatus4 = '二号门已打开'
        else:
            cn_doorstatus4 = '二号门已关闭'

    cn_rec_data['cn_doorstatus1'] = cn_doorstatus1
    cn_rec_data['cn_doorstatus2'] = cn_doorstatus2
    cn_rec_data['cn_doorstatus3'] = cn_doorstatus3
    cn_rec_data['cn_doorstatus4'] = cn_doorstatus4

    # 按钮状态
    cn_button_status1 = ''
    cn_button_status2 = ''
    cn_button_status3 = ''
    cn_button_status4 = ''

    temp_button_status = rec_data[32:36]
    list_button_status = [st for st in temp_button_status]
    if dev_sn[0] == '1':
        if list_button_status[0] == 1:
            cn_button_status1 = '按钮已按下'
        else:
            cn_button_status1 = '按钮已松开'

    elif dev_sn[0] == '2':
        if list_button_status[0] == 1:
            cn_button_status1 = '按钮已按下'
        else:
            cn_button_status1 = '按钮已松开'

        if list_button_status[1] == 1:
            cn_button_status2 = '按钮已按下'
        else:
            cn_button_status2 = '按钮已松开'

    elif dev_sn[0] == '4':
        if list_button_status[0] == 1:
            cn_button_status1 = '按钮已按下'
        else:
            cn_button_status1 = '按钮已松开'

        if list_button_status[1] == 1:
            cn_button_status2 = '按钮已按下'
        else:
            cn_button_status2 = '按钮已松开'

        if list_button_status[2] == 1:
            cn_button_status3 = '按钮已按下'
        else:
            cn_button_status3 = '按钮已松开'

        if list_button_status[3] == 1:
            cn_button_status4 = '按钮已按下'
        else:
            cn_button_status4 = '按钮已松开'

    cn_rec_data['cn_button_status1'] = cn_button_status1
    cn_rec_data['cn_button_status2'] = cn_button_status2
    cn_rec_data['cn_button_status3'] = cn_button_status3
    cn_rec_data['cn_button_status4'] = cn_button_status4

    return cn_rec_data







