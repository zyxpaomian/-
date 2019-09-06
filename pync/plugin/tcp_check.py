#! -*- coding:utf-8 -*-
import socket
from colorama import Fore, Back, Style
import time
import datetime
 
def tcpPortCheck(time_length,type_length,sip_length,dip_length,dport_length,dzone_length,result_length,scrip,dstip,dstport,dstenv,logdir):
    socket.setdefaulttimeout(1)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        server.connect((str(dstip),int(dstport)))

        time_data = nowtime.center(time_length, ' ')
        time_data_style = Fore.YELLOW + time_data + Style.RESET_ALL
        
        type_data = "TCP".center(type_length, ' ')
        type_data_style = Fore.YELLOW + type_data + Style.RESET_ALL
        
        sip_data = scrip.center(sip_length, ' ')
        sip_data_style = Fore.MAGENTA + sip_data + Style.RESET_ALL
        
        dip_data = dstip.center(dip_length, ' ')
        dip_data_style = Fore.CYAN + dip_data + Style.RESET_ALL
        
        dport_data = dstport.center(dport_length, ' ')
        dport_data_style = Fore.CYAN + dport_data + Style.RESET_ALL
        
        dzone_data = dstenv.center(dzone_length, ' ')
        dzone_data_style = Fore.YELLOW + dzone_data + Style.RESET_ALL
        
        result_data = "SUCCESS".center(result_length, ' ')
        result_data_style = Fore.GREEN + result_data + Style.RESET_ALL

        logname = logdir + "/" + datetime.datetime.now().strftime('%Y_%m_%d') + "_" + dstip + "_" + dstport + ".log" 

        with open(logname, 'a+') as f:
            f.write(nowtime+ ":" + "From IP: " + scrip + " to IP: " + dstip + ":" + dstport + " Result: Success" + "\n")
        f.close()

        print("|{0}|{1}|{2}|{3}|{4}|{5}|{6}|").format(time_data_style,type_data_style,sip_data_style,dip_data_style,dport_data_style,dzone_data_style,result_data_style)
    except Exception as err:
        time_data = nowtime.center(time_length, ' ')
        time_data_style = Fore.YELLOW + time_data + Style.RESET_ALL
    
        type_data = "TCP".center(type_length, ' ')
        type_data_style = Fore.YELLOW + type_data + Style.RESET_ALL
    
        sip_data = scrip.center(sip_length, ' ')
        sip_data_style = Fore.MAGENTA + sip_data + Style.RESET_ALL
    
        dip_data = dstip.center(dip_length, ' ')
        dip_data_style = Fore.CYAN + dip_data + Style.RESET_ALL
    
        dport_data = dstport.center(dport_length, ' ')
        dport_data_style = Fore.CYAN + dport_data + Style.RESET_ALL
    
        dzone_data = dstenv.center(dzone_length, ' ')
        dzone_data_style = Fore.YELLOW + dzone_data + Style.RESET_ALL
    
        result_data = "FAILED".center(result_length, ' ')
        result_data_style = Fore.RED + result_data + Style.RESET_ALL

        logname = logdir + "/" + datetime.datetime.now().strftime('%Y_%m_%d') + "_" + dstip + "_" + dstport + ".log"

        with open(logname, 'a+') as f:
            f.write(nowtime+ ":" + "From IP: " + scrip + " to IP: " + dstip + ":" + dstport + " Result: Failed" + "\n")
        f.close()

        print("|{0}|{1}|{2}|{3}|{4}|{5}|{6}|").format(time_data_style,type_data_style,sip_data_style,dip_data_style,dport_data_style,dzone_data_style,result_data_style)
    finally:
        server.close()
