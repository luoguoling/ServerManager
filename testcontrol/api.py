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
def socket_send(ip,port,command):
    """
    发送命令到对应服务器
    """
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((ip,port))
    sock.send(command)
    result = sock.recv(2048)
    sock.close()
    return result
class ServerError(Exception):
    """
    self define exception
    自定义异常
    """
    pass
def parseConfig():
    """
    解析配置文件,获取信息
    """
def write_log(local_logs):
    if not os.path.exists("logs"):
        try:
            os.mkdir("logs")
        except:
            print 'can not mkdir'
    cur_time = time.strftime("%Y%m%d")
    logs = "["+time.strftime("%Y-%m-%d-%H-%M-%S")+"]: "+local_logs+"\n"
    file = open("logs/"+cur_time+".txt","a")
    file.write(logs)
    file.close()
