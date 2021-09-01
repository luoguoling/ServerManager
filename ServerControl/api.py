#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
import socket,time,sys,os,commands
import ConfigParser
def my_render(template, data, request):
    """
    重新定义视图返回函数,减少代码重复性
    """
    return render_to_response(template, data, context_instance=RequestContext(request))
def socket_send(ip,command):
    """
    发送命令到对应服务器
    """
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((ip,1003))
    sock.send(command)
    result = sock.recv(2048)
    sock.close()
    return result
def parseConfig():
    """
    解析配置文件,获取信息
    """

