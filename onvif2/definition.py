SERVICES = {
        # Name                              namespace                           wsdl file                      binding name
        'devicemgmt': {'ns': 'http://www.onvif.org/ver10/device/wsdl',    'wsdl': './ver10/device/wsdl/devicemgmt.wsdl', 'binding' : 'DeviceBinding'},
        'media'     : {'ns': 'http://www.onvif.org/ver10/media/wsdl',     'wsdl': './ver10/media/wsdl/media.wsdl',      'binding' : 'MediaBinding'},
        'media2'    : {'ns': 'http://www.onvif.org/ver20/media/wsdl',     'wsdl': './ver20/media/wsdl/media.wsdl',      'binding' : 'Media2Binding'},
        'ptz'       : {'ns': 'http://www.onvif.org/ver20/ptz/wsdl',       'wsdl': './ver20/ptz/wsdl/ptz.wsdl',        'binding' : 'PTZBinding'},
        'imaging'   : {'ns': 'http://www.onvif.org/ver20/imaging/wsdl',   'wsdl': './ver20/imaging/wsdl/imaging.wsdl',    'binding' : 'ImagingBinding'},
        'deviceio'  : {'ns': 'http://www.onvif.org/ver10/deviceIO/wsdl',  'wsdl': './ver10/deviceio.wsdl',   'binding' : 'DeviceIOBinding'},
        'events'    : {'ns': 'http://www.onvif.org/ver10/events/wsdl',    'wsdl': './ver10/events/wsdl/event.wsdl',     'binding' : 'EventBinding'},
        'pullpoint' : {'ns': 'http://www.onvif.org/ver10/events/wsdl',    'wsdl': './ver10/events/wsdl/event.wsdl',     'binding' : 'PullPointSubscriptionBinding'},
        'analytics' : {'ns': 'http://www.onvif.org/ver20/analytics/wsdl', 'wsdl': './ver20/analytics/wsdl/analytics.wsdl',  'binding' : 'AnalyticsEngineBinding'},
        'recording' : {'ns': 'http://www.onvif.org/ver10/recording/wsdl', 'wsdl': './ver10/recording.wsdl',  'binding' : 'RecordingBinding'},
        'search'    : {'ns': 'http://www.onvif.org/ver10/search/wsdl',    'wsdl': './ver10/search.wsdl',     'binding' : 'SearchBinding'},
        'replay'    : {'ns': 'http://www.onvif.org/ver10/replay/wsdl',    'wsdl': './ver10/replay.wsdl',     'binding' : 'ReplayBinding'},
        'receiver'  : {'ns': 'http://www.onvif.org/ver10/receiver/wsdl',  'wsdl': './ver10/receiver.wsdl',   'binding' : 'ReceiverBinding'},
        }

#
#NSMAP = { }
#for name, item in SERVICES.items():
#    NSMAP[item['ns']] = name
