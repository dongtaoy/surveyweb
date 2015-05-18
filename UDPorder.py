__author__ = 'zhangjingyuan'

UDP:
    timestamp:int
    dstPort:int
    srcPort:int

    data:Data

Receiver:
    current_udp_time:MIN_TIME
    if received_udp.timestamp>MIN_TIME:
        accept()
    else wait


Sender:
    current_stamp:MIN_TIME
    send()
    current_stamp++