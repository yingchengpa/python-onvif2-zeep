# -*- coding: utf-8 -*-
from onvif2 import ONVIFCamera

if __name__ == '__main__':
    mycam = ONVIFCamera('192.168.1.10', 8899, 'admin', 'admin') #, no_cache=True)
    events_service = mycam.create_events_service()
    print(events_service.GetEventProperties())

    pullpoint = mycam.create_pullpoint_service()
    
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
