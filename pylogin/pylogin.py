#! /usr/bin/python
# -*- coding: utf-8 -*- 
#auther barney add by 20151110

import pexpect
import struct,fcntl,sys
import termios


input_ip=sys.argv[1]
length=len(input_ip.split('.'))

##shangha password
sh_passwd='shpasswd'
sh_root_pass='shpasswd'
sh_location='\033[5;32;40m######上海IDC...######\033[0m'
##tianjin password
tj_passwd='tjpasswd'
tj_root_pass='tjpasswd'
tj_location='\033[5;32;40m######天津IDC...######\033[0m'
##suzhou password
sz_passwd='sjpasswd'
sz_root_pass='sjpasswd'
sz_location='\033[5;32;40m######苏州IDC...######\033[0m'

def getwinsize(): #这个模块主要用于记录登录前的session的窗口大小，不然会发生登录后窗口大小变小的问题
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912L 
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]

def ipinfo():
         if  network in ('1','2','6','7','8'):
             return (ip,sh_passwd,sh_root_pass,sh_location)
         elif  network in ('30','31','32','33'):
             return (ip,tj_passwd,tj_root_pass,tj_location)
         elif  network in ('4','11','71','72'):
             return (ip,sz_passwd,sz_root_pass,sz_location)
         else:
             print '请输入正确的2位 IP'

def ssh_host(): #因为都是192.168 开头的私有地址，所以就输入后2位就行了
    try:
        print"%s"%location
        child=pexpect.spawn('ssh -p 56000 barney@%s'%ip)
        child.expect(['密码','(?i)password:'])
        child.sendline('%s'%passwd)
        child.sendline('su -')
        child.expect(['密码','(?i)password:'])
        child.sendline('%s'%root_pass)
        child.sendline('clear')
        winsize = getwinsize();
        child.setwinsize(winsize[0], winsize[1])
        child.interact()
        child.close()
    except OSError:
        print 'Login Ended'
        
if length == 2:
        ip='192.168.'+input_ip
        network=input_ip.split('.')[0]
        ip,passwd,root_pass,location=ipinfo()
        ssh_host()
else:
     print "IP地址错误"