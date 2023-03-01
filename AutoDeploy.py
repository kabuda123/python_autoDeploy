import datetime
import os, sys, time, ctypes
import re
import shutil

import requests
import webbrowser


# 自动化部署类
class Auto:

    # 是否有管理员权限
    @staticmethod
    def is_admin():
        try:
            return ctypes.windll.shell32.isUserAdmin()
        except:
            return False

    # 获取端口号进程pid （端口）
    @staticmethod
    def get_pid(port):
        task_info = os.popen("netstat -tunlp |grep {}".format(port))
        line = task_info.readlines()
        task_info.close()
        if line == '':
            return ""
        filed_list = str(line).split()
        if len(filed_list) < 6:
            return ""
        pid = filed_list[6]
        pid = re.sub("\D", "", pid)
        return pid

        # i = 0
        # for filed in filed_list:
        #     print("====下标：" + str(i) + "=======数据：" + filed)
        #     i = i + 1

    # 停止指定端口进程 （端口）
    @staticmethod
    def kill_server(port):
        pid = Auto.get_pid(port)
        if pid == "" or pid == "0":
            print("端口号 {} 已停止或不存在".format(pid))
            return
        os.popen("kill -9 {}".format(pid))
        print("端口号{} 已经停止！".format(pid))
        return

    # 执行指定启动脚本 （启动脚本，端口）
    @staticmethod
    def start_popen(popen_str, port):
        if len(str(popen_str)) <= 0:
            print("命令异常！")
            return
        pid = Auto.get_pid(port)
        if pid == "" or pid == "0":
            os.popen(popen_str)
            print("启动成功！")
            return
        else:
            print("启动失败！")
            return

    @staticmethod
    def removeFile(fileUrl, fileName):
        if fileUrl == "" or fileName == "":
            print("文件地址或文件名不能为空！")
            return
        os.popen("rm -rf " + fileUrl + fileName)
        print("文件{}删除成功".format(fileName))
        return

    # '''复制文件'''
    @staticmethod
    def copy_file(src_file, dest_path):
        print(dest_path)
        print(src_file)
        if not os.path.isfile(src_file):
            print("文件 {} 不存在\n".format(src_file))
            return False
        else:
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            print(dest_path)
            print(src_file)
            shutil.copy(src_file, dest_path)
            return True

    # 备份文件
    @staticmethod
    def backup_resource(srcFle, targDir):

        if not os.path.isfile(srcFle):
            print("文件 {} 不存在\n".format(srcFle))
            return False
        srcList = str(srcFle).split("/")
        oldFileName = srcList[-1]

        # if fileName == "":
        dateStr = datetime.datetime.now().strftime('%Y-%m-%d')
        fileName = oldFileName + dateStr
        newtargDir = targDir + "/" + str(fileName)
        i = 1
        while True:
            if not os.path.isfile(newtargDir):
                break
            else:
                if i == 1:
                    newtargDir = newtargDir + "-" + str(i)
                else:
                    newtargDir = newtargDir[0:-1] + str(i)
                i += 1
        os.popen("mv " + str(srcFle) + " " + newtargDir)
        print("文件备份成功")
        return


# print(Auto.kill_server("8081"))
# Auto.copy_file("", "/mydata/tomcat/zjq_auto_deploy/bms_base")


def run():
    # war包名称
    warFileName = "bms-base.war"
    # 项目所在目录
    workDir = "/mydata/tomcat/tomcat_bms_base/webapps"
    binDir = "/mydata/tomcat/tomcat_bms_base/bin"
    srcDir = "/mydata/tomcat/zjq_auto_deploy/bms_base"
    srcFileDir = srcDir + "/" + warFileName
    catchFile = "bms-base"
    warFileDir = workDir + "/" + warFileName
    port = 8081
    startBot = binDir + "/./startup.sh"

    Auto.kill_server(8081)
    Auto.removeFile(workDir, catchFile)
    Auto.backup_resource(warFileDir, workDir)
    # 文件修改延迟
    time.sleep(2)
    Auto.copy_file(srcFileDir, workDir)
    Auto.start_popen(startBot, port)


if __name__ == "__main__":
    run()