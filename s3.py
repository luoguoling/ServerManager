#__author__ = 'Administrator'
#coding=UTF-8
# -*- coding: utf-8 -*-
from SocketServer import TCPServer,ThreadingMixIn,StreamRequestHandler
import time,os,commands
#HOST = '207.198.106.114'
HOST = '0.0.0.0'
PORT = 1003
def transfertime(ret):
    a = filter(str.isdigit,ret)
    a = list(a)
    c = ''
    for i in range(len(a)):
        c += a[i]
        if i in (3,5):
            c += '-'
        if i==7:
            c += ' '
        if i in (9,11):
            c += ':'
    a = time.mktime(time.strptime(c,'%Y-%m-%d %H:%M:%S'))
    return a
def stopjava():
#    os.popen("cd /program/game/ss_pub_english_ios_10001/ssserver/ && /bin/sh stop.sh >/dev/null 2>&1")
    os.popen("cd /data/game/ssstest1000pub_sss && /bin/sh stop.sh >/dev/null 2>&1")
    os.popen("cd /data/game/ssstest1000_sss_1_sss && /bin/sh stop.sh >/dev/null 2>&1") 
def startjava():
#    os.popen("cd /program/game/ss_pub_english_ios_10001/ssserver/ && /bin/sh start.sh >/dev/null 2>&1")
#    time.sleep(3)
#    os.popen("cd /home/bleach/game_cehua && /bin/sh start.sh >/dev/null 2>&1")
    os.popen("cd  /data/game/ssstest1000pub_sss  && /bin/sh start.sh >/dev/null 2>&1")
    os.popen("cd  /data/game/ssstest1000_sss_1_sss  && /bin/sh start.sh >/dev/null 2>&1")
#    os.popen("cd /data/game/huodong && /bin/sh start.sh >/dev/null 2>&1")


def updatejava():
    #os.popen('rsync -vzrtopg --progress --stats  /var/ftp/qmrserver/* /data/game/pubserver/qmrserver > /dev/null 2>&1')
    os.popen('cd /data/game/ssstest1000pub_sss/pubserver && svn update')
    os.popen('cd /data/game/ssstest1000_sss_1_sss/nodeserver && svn update') 
#def checkJavaStatus():
#    JavaStatus=commands.getoutput('netstat -tunlp|grep java|wc -l')
#    print JavaStatus
#    return JavaStatus
def reloadjava():
    os.popen('cd /data/game/ssstest1000pub_sss && sh reload.sh')
    os.popen('cd /data/game/ssstest1000_sss_1_sss && sh reload.sh')
def checkJavaStatus():
#    game_cehua_Status=commands.getoutput('cd /home/bleach/game_cehua/ && sh checkserver.sh -ct')
    game_new_Status=commands.getoutput('cd /data/game/ssstest1000_sss_1_sss && sh checkserver.sh -ct')
    game_new_Status_code = eval(game_new_Status)["code"]
    if game_new_Status_code == "1":
        result = commands.getoutput('cd /data/game/ssstest1000_sss_1_sss && tail -n 10 nohup.out')
        javaStatus = result
    else:
#    public_Status=commands.getoutput('cd /program/game/ss_pub_english_ios_10001/ssserver/ && sh checkserver.sh -ct')
        javaStatus=game_new_Status
    return javaStatus
logfile = open('name1.txt','a')
def log(msg):
    datenow = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    logstr = '%s : %s \n' %(datenow, msg)
    #print(logstr)
    logfile.write(logstr)

class Server(ThreadingMixIn,TCPServer):
    pass
class ThreadingServer(ThreadingMixIn,TCPServer):
    allow_reuse_address = True
class Handler(StreamRequestHandler):
    def handle(self):
        while True:
            try:
                ip = self.client_address[0]
                print ip
#                print ip
                ret = self.request.recv(2048).strip()
#		print ret
                #log('ret %s' % ret)
                if ip == '222.190.107.198' or ip == '127.0.0.1' or ip == '134.175.14.29':
                    if ret == 'reboot':
                        self.request.send('???????????????????????????.....')
                        stopjava()
                        time.sleep(4)
                        updatejava()
                        startjava()
                        time.sleep(10)
                        javaStatus = checkJavaStatus()
			self.request.send(javaStatus)
                        self.finish()
                    elif ret == 'banben':
                        self.request.send('?????????????????????????????????reload')
                        updatejava()
                        reloadjava()
                    elif ret == 'time':
                        shijian = os.popen('date +"%Y-%m-%d %H:%M:%S"').read()
                        self.request.send(shijian)
                    elif ret == 'shutdowngame':
                        stopjava()    
                        self.request.send("???????????????????????????")
                    elif ret == 'check':
#                        checkJavaStatus()
                        javaStatus = checkJavaStatus()
                        self.request.send(javaStatus)
                    elif not ret:
#                        print '????????????'
                        break
                    else:
                        self.request.send('???????????????????????????....')
                        try:
                            global time1
                            time1 = transfertime(ret)
                            timett = commands.getoutput('date "+%Y-%m-%d %H:%M:%S"')
                            time2 = transfertime(timett)
                        except Exception,e:
                            print e
                            #log('??????????????????')
                            self.request.send('??????????????????')
                        if int(time1) > int(time2):
			    print ret
                            os.popen('date -s "%s"' % ret).read()
                            self.request.send('??????????????????')
                        else:
			    print ret
                            self.request.send('?????????????????????????????????...')
                            stopjava()
                            time.sleep(8)
                            os.popen('date -s "%s"' % ret).read()
                            startjava()
                            time.sleep(8)
                else:
                    #log('the source is wrong')
                    pass
            except KeyboardInterrupt:
                log('????????????')
#server = Server((HOST,PORT),Handler)
def funzioneDemo():
    server = ThreadingServer((HOST,PORT),Handler)
    server.serve_forever()
def createDaemon():
    try:
        if os.fork() > 0:
            os._exit(0)
    except OSError,error:
        print "fork #1 failed: %d (%s)" % (error.errno, error.strerror)
        os._exit(1)
    os.chdir('/')
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            print 'Daemon PID %d' % pid
            os._exit(0)
    except OSError,error:
        print "fork #1 failed: %d (%s)" % (error.errno, error.strerror)
        os._exit(1)
    funzioneDemo()
if __name__ == "__main__":
    createDaemon()








