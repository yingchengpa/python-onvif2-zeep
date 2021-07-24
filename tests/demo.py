# -*- coding: utf-8 -*-

import datetime

from onvif2 import ONVIFCamera
from zeep.transports import Transport
import json
import os
import sys


def getexepath():
    """
    返回可执行程序的当前路径。 sys.argv 中保存了可执行程序的全路径
    :return:
    """
    return os.path.split(os.path.realpath(sys.argv[0]))[0]


class COnvifClient:

    def __init__(self):
        self.mycam = None
        self.media_service = None
        self.media2_service = None
        self.events_service = None
        self.name = None
        self.pwd = None

    def __del__(self):
        pass

    def conn(self, ip, port, name, pwd) -> bool:
        """
        通过鉴权对设备进行连接.
        media\media2  默认加载，其他模块按需加载
        :param ip:
        :param port:
        :param name:
        :param pwd:
        :return:
        """
        try:
            # 设置操作时间
            transport = Transport(operation_timeout=10)

            # 设置wsdl 文件夹目录，需要把wsdl 复制到当前可执行文件目录
            self.mycam = ONVIFCamera(ip, port, name, pwd, wsdl_dir=getexepath() + '/wsdl',
                                     transport=transport)
        except Exception as e:
            print('error: {}'.format(e))
            return False
        finally:
            pass

        self.name = name
        self.pwd = pwd

        return self.getmedia()

    # ---------------------------------- media \ media2 -------------------------------------------
    def getmedia(self):
        """
        获取media： 分为media2、media，其中media2支持h265，media只支持h264
        :return:
        # 先使用media2，再使用media： media2支持h265
        # 比如海康、大华、宇视都支持media2， 淼盾只支持media
        """
        try:
            self.media2_service = self.mycam.create_media2_service()
        except Exception as e:
            print('error: {}'.format(e))
        finally:
            pass

        # media 获取h264
        if self.media2_service is None:
            try:
                self.media_service = self.mycam.create_media_service()
            except Exception as e:
                print('error: {}'.format(e))
                return False
            finally:
                pass

        return True

    def _getstreamuri_media(self) -> list:
        """
        通过media 获取rtsp地址
        :return:
        """
        profiles = self.media_service.GetProfiles()

        urilist = []
        for profile in profiles:
            o = self.media_service.create_type('GetStreamUri')
            o.ProfileToken = profile.token
            o.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
            r = self.media_service.GetStreamUri(o)

            # 携带鉴权信息
            if self.pwd != '':
                dic = {'token': profile.token,
                       'rtsp': "rtsp://{}:{}@{}".format(self.name, self.pwd, r['Uri'][7:])}
            else:
                dic = {'token': profile.token,
                       'rtsp': r['Uri']}
            urilist.append(dic)

        return urilist

    def _getvideo_media(self) -> list:
        """
        通过media获取视频参数
        :return:
        """
        configurations = self.media_service.GetVideoEncoderConfigurations()

        lns = []
        for configuration in configurations:
            if configuration['Encoding'].lower() == 'h264':
                width = configuration['Resolution']['Width']
                height = configuration['Resolution']['Height']
                dic = {'token': configuration['token'],
                       'encoding': configuration['Encoding'],
                       'ratio': "{}*{}".format(width, height),
                       'fps': configuration['RateControl']['FrameRateLimit'],
                       'bitrate': configuration['RateControl']['BitrateLimit'],
                       'gop': configuration['H264']['GovLength'],
                       'profile': configuration['H264']['H264Profile'],
                       'quality': configuration['Quality']}

            else:
                dic = {'token': configuration['Name'], 'encoding': configuration['Encoding']}

            lns.append(dic)

        return lns

    def _getstreamuri_media2(self) -> list:
        """通过media2.0 版本获取rtsp地址"""
        profiles = self.media2_service.GetProfiles()

        urilist = []
        for profile in profiles:
            o = self.media2_service.create_type('GetStreamUri')
            o.ProfileToken = profile.token
            o.Protocol = 'RTSP'
            uri = self.media2_service.GetStreamUri(o)

            # 携带鉴权信息
            if self.pwd != '':
                dic = {'token': profile.token,
                       'rtsp': "rtsp://{}:{}@{}".format(self.name, self.pwd, uri[7:])}
            else:
                dic = {'token': profile.token,
                       'rtsp': uri}

            urilist.append(dic)

        return urilist

    def _getvideo_media2(self) -> list:
        """通过media2获取编码配置，media2支持h265"""
        configurations = self.media2_service.GetVideoEncoderConfigurations()

        lns = []
        for configuration in configurations:
            if configuration['Encoding'].lower() == 'h264' or configuration['Encoding'].lower() == 'h265':
                width = configuration['Resolution']['Width']
                height = configuration['Resolution']['Height']
                dic = {'token': configuration['token'],
                       'encoding': configuration['Encoding'],
                       'ratio': "{}*{}".format(width, height),
                       'fps': configuration['RateControl']['FrameRateLimit'],
                       'bitrate': configuration['RateControl']['BitrateLimit'],
                       'gop': configuration['GovLength'],
                       'profile': configuration['Profile'],
                       'quality': configuration['Quality']}
            else:
                dic = {'token': configuration['Name'], 'encoding': configuration['Encoding']}

            lns.append(dic)

        return lns

    def getsteamuri(self) -> list:
        """
        获取流地址
        :return:
        """
        if self.media2_service is not None:
            urls = self._getstreamuri_media2()
        else:
            urls = self._getstreamuri_media()

        return urls

    def getvideo(self) -> list:
        """
        获取视频信息
        :return:
        """
        if self.media2_service is not None:
            vidoes = self._getvideo_media2()
        else:
            vidoes = self._getvideo_media()

        return vidoes

    # --------------------------------------------- device management ------------------------------------
    def getdeviceinfo(self) -> dict:
        """
        获取onvif设备基础信息
        "FirmwareVersion": "IPC_Q1207-B0006D1904",
        "HardwareId": "xdfd@SH-FA-VA",
        "Manufacturer": "bbb",
        "Model": "xdfd@SH-FA-VA",
        "SerialNumber": "210235C3EN3193000033"

        """

        resp = self.mycam.devicemgmt.GetDeviceInformation()
        dic = {'manufacturer': resp.Manufacturer,
               'model': resp.Model,
               'firmwareversion': resp.FirmwareVersion,
               'serialnumber': resp.SerialNumber,
               'hardwareid': resp.HardwareId}
        return dic

    # ---------------------------------------- event ------------------------------------------------

    def subEvent(self):
        """
        简单描述了核心逻辑，具体需求时需要再修改
        订阅事件通知，
        采用real-time pull-point Notification interface 模式。 需要启动线程
        资料介绍： http://www.doc88.com/p-381499525793.html
        该模式采用的方式：
        createPullPoint() ---- > ipc
        pullMessagees     ---- > ipc
        ------ http wait n seconds ------
        pullMessagesRespons <--  ipc
        pullMessagees     ---- > ipc
        ------ http wait n seconds ------
        pullMessagesRespons <--  ipc
              ............
        unsubscribe  ---- > ipc
        :return:
        """
        # event 订阅事件
        self.events_service = self.mycam.create_events_service()
        print(self.events_service.GetEventProperties())

        pullpoint = self.mycam.create_pullpoint_service()

        """模块启动时，自动启动一个线程执行清理"""
        # t1 = threading.Thread(target=_time_task, daemon=True)
        # t1.start()
        ######    _time_task  #######
        while True:
            try:
                pullmess = pullpoint.PullMessages({"Timeout": datetime.timedelta(seconds=5), "MessageLimit": 10})
                print(pullmess.CurrentTime)
                print(pullmess.TerminationTime)
                for msg in pullmess.NotificationMessage:
                    print(msg)
            except Exception as e:
                print(e)
            finally:
                pass


if __name__ == '__main__':
    obj = COnvifClient()
    if obj.conn('204.204.50.190', 80, 'admin', '*Ab123456') is True:
        """
        {
            "manufacturer": "HIKVISION",
            "model": "DS-IPC-B12HV2-IA",
            "firmwareversion": "V5.5.102 build 200928",
            "serialnumber": "DS-IPC-B12HV2-IA20201125AACHF11786005",
            "hardwareid": "88"
        }
        """
        print(json.dumps(obj.getdeviceinfo()))
        """
        [
        {"token": "Profile_1", "rtsp": "rtsp://admin:*Ab123456@204.204.50.190/Streaming/Channels/101?transportmode=unicast&profile=Profile_1"}, 
        {"token": "Profile_2", "rtsp": "rtsp://admin:*Ab123456@204.204.50.190/Streaming/Channels/102?transportmode=unicast&profile=Profile_2"}
        ]
        """
        print(json.dumps(obj.getsteamuri()))

        """
        [
        {"token": "VideoEncoderToken_1", "encoding": "H264", "ratio": "1920*1080", "fps": 25.0, "bitrate": 2614, "gop": 25, "profile": "Main", "quality": 3.0}, 
        {"token": "VideoEncoderToken_2", "encoding": "H265", "ratio": "640*480", "fps": 8.0, "bitrate": 192, "gop": 50, "profile": "Main", "quality": 3.0}]
        """
        print(json.dumps(obj.getvideo()))

        """
        2021-06-01 07:15:26+00:00
        2021-06-01 07:25:31+00:00
        {
                'SubscriptionReference': None,
                'Topic': {
                    '_value_1': 'tns1:Monitoring/ProcessorUsage',
                    'Dialect': 'http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet',
                    '_attr_1': {
                }
                },
                'ProducerReference': None,
                'Message': {
                    'Message': {
                        'Source': {
                            'SimpleItem': [
                                {
                                    'Name': 'Token',
                                    'Value': 'Processor_Usage'
                                }
                            ],
                            'ElementItem': [],
                            'Extension': None,
                            '_attr_1': None
                        },
                        'Key': None,
                        'Data': {
                            'SimpleItem': [
                                {
                                    'Name': 'Value',
                                    'Value': '37'
                                }
                            ],
                            'ElementItem': [],
                            'Extension': None,
                            '_attr_1': None
                        },
                        'Extension': None,
                        'UtcTime': datetime.datetime(2021, 6, 1, 7, 15, 30, tzinfo=<isodate.tzinfo.Utc object at 0x000001F821BD1F40>),
                        'PropertyOperation': 'Changed',
                        '_attr_1': {
                    }
                    }
                }
            }
        """
        print(obj.subEvent())
