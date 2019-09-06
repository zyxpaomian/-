#! -*-coding:utf-8 -*-
from colorama import Fore, Back, Style
import datetime
import time


def createTableTitle():
    time_length = 21
    time_title = "Detecte Time".center(time_length, ' ')
    time_title_style = Fore.YELLOW + time_title + Style.RESET_ALL
    
    type_length = 14
    type_title = "Detecte Type".center(type_length, ' ')
    type_title_style = Fore.YELLOW + type_title + Style.RESET_ALL
    
    sip_length = 19
    sip_title = "Detecte SIP".center(sip_length, ' ')
    sip_title_style = Fore.MAGENTA + sip_title + Style.RESET_ALL
    
    dip_length = 19
    dip_title = "Detecte DIP".center(dip_length, ' ')
    dip_title_style = Fore.CYAN + dip_title + Style.RESET_ALL
    
    dport_length = 15
    dport_title = "Detecte DPort".center(dport_length, ' ')
    dport_title_style = Fore.CYAN + dport_title + Style.RESET_ALL
    
    dzone_length = 14
    dzone_title = "Detecte Zone".center(dzone_length, ' ')
    dzone_title_style = Fore.YELLOW + dzone_title + Style.RESET_ALL
    
    result_length = 16
    result_title = "Detecte Result".center(result_length, ' ')
    result_title_style = Fore.YELLOW + result_title + Style.RESET_ALL

    print("|{0}|{1}|{2}|{3}|{4}|{5}|{6}|").format(time_title_style,type_title_style,sip_title_style,dip_title_style,dport_title_style,dzone_title_style,result_title_style)
    return (time_length,type_length,sip_length,dip_length,dport_length,dzone_length,result_length)
