#! -*- coding:utf-8 -*-
from plugin.tcp_check import tcpPortCheck
from plugin.table import createTableTitle
import configparser
import time
import multiprocessing
import argparse
import os 

parser = argparse.ArgumentParser()
parser.add_argument('-V', '--version', action='version', version='Version 1.0.0')
parser.add_argument("-c", "--config", help="(必要参数)配置文件位置,EP:'/etc/yqbnc.cfg'")
parser.add_argument("-r", "--refreshnum", help="滚屏每多少次出现标题")
parser.add_argument("-s", "--sourceip", help="本地服务器SourceIP")
parser.add_argument("-l", "--logdir", help="日志文件位置，默认为/tmp")
parser.add_argument("-i", "--interval", help="取值间隔时间,默认为1S")
parser.add_argument("-T", "--type", help="默认为tcp探测,其他类型探测等待后续版本")
args = parser.parse_args()

if not args.config:
    print "请在参数内输入配置文件位置"
    exit(0)
if not args.refreshnum:
    args.refreshnum = 50

if not args.sourceip:
    args.sourceip = '127.0.0.1'

if not args.logdir:
    args.logdir = "/tmp/"
else:
    if not os.path.exists(args.logdir):
        os.mkdir(args.logdir,0755)

if not args.interval:
    args.interval = 1


cf = configparser.ConfigParser()
cf.read(args.config)

iplist = cf.get("tcp", "iplist").split(",")
time_length,type_length,sip_length,dip_length,dport_length,dzone_length,result_length = createTableTitle()
sourceip = args.sourceip
screen_length = 1
logdir = args.logdir
while True:
    jobs = []
    for i in range(len(iplist)):
        dstip = iplist[i].split("_")[0]
        dstport = iplist[i].split("_")[1]
        dstenv = iplist[i].split("_")[2]
        p = multiprocessing.Process(target = tcpPortCheck, args = (time_length,type_length,sip_length,dip_length,dport_length,dzone_length,result_length,sourceip,dstip,dstport,dstenv,logdir))
        jobs.append(p)
        p.start()
    screen_length +=  len(jobs)
    if screen_length >= args.refreshnum:
        createTableTitle()
        screen_length = 1
    time.sleep(float(args.interval))
