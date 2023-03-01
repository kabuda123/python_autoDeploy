import os, sys, time, ctypes
import shutil
import requests
import webbrowser

'''自动化部署类'''


class AutoRelease():
    '''判断是否有管理员权限'''

    @staticmethod
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    '''根据端口号获取pid'''

    @staticmethod
    def get_pid(port):
        task_info = os.popen('netstat -ano | findstr {}'.format(port))
        line = task_info.readline()
        task_info.close()
        if line == "":
            return ""
        field_list = line.split()
        pid = field_list[4]
        return pid

    '''根据端口号停止进程'''

    @staticmethod
    def close_process(port):
        pid = AutoRelease.get_pid(port)
        if pid == "" or pid == "0":
            print("端口 %s 已停止或不存在" % port)
            return

        if AutoRelease.is_admin():
            os.popen('taskkill /pid %s /f' % pid)
        else:
            print("正在停止进程（端口） %s ..." % port)
            if sys.version_info[0] == 3:
                # 以管理员权限重新打开一个进程执行命令，最后一个参数表示是否显示cmd窗口，0 隐藏，1 显示
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)

    '''启动指定的服务'''

    @staticmethod
    def start_service(service_name):
        if AutoRelease.is_admin():
            os.popen('net start {}'.format(service_name))
        else:
            # print("正在启动服务 %s，请稍候..." % service_name)
            if sys.version_info[0] == 3:
                # 以管理员权限重新打开一个进程执行命令，最后一个参数表示是否显示cmd窗口，0 隐藏，1 显示
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)

    '''停止指定的服务'''

    @staticmethod
    def stop_service(service_name):
        if AutoRelease.is_admin():
            os.popen('net stop {}'.format(service_name))
        else:
            # print("正在停止服务 %s，请稍候..." % service_name)
            if sys.version_info[0] == 3:
                # 以管理员权限重新打开一个进程执行命令，最后一个参数表示是否显示cmd窗口，0 隐藏，1 显示
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)

    '''压缩目录'''

    @staticmethod
    def archive_file(out_zip, root_dir):
        try:
            shutil.make_archive(out_zip, 'zip', root_dir=root_dir)
        except Exception:
            return False
        else:
            return True

    '''复制文件'''

    @staticmethod
    def copy_file(src_file, dest_path):
        if not os.path.isfile(src_file):
            print("文件 %s 不存在\n" % src_file)
            return False
        else:
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            shutil.copy(src_file, dest_path)
            return True

    '''
    判断http资源是否可以访问
    @url http资源地址
    '''

    @staticmethod
    def get_http_status(url):
        try:
            request = requests.get(url)
        except Exception:
            return False
        else:
            httpStatusCode = request.status_code
            if httpStatusCode == 200:
                return True
            return False


def run():
    print("-" * 63)
    print("\n{0}{1}\n".format("自动化部署工具 V2.1", "\t" * 11))
    print("步骤1.备份原文件\n")
    print("步骤2.停止 Tomcat 服务\n")
    print("步骤3.部署新文件并同时删除原文件\n")
    print("步骤4.启动 Tomcat 服务\n")
    print("步骤5.检测应用是否可以正常访问\n")
    print("-" * 63)
    print("\n{0}{1}{0}\n".format("*" * 27, "部署开始"))

    # 应用端口号
    port = "8383"
    # 服务名称
    service_name = "Tomcat8"
    # war包名称
    war_file_name = "assist-mis.war"
    # 备份压缩包名称
    zip_file_name = "assist-mis.zip"
    # 项目所在目录
    work_dir = "D:/apache-tomcat-8.5.38/webapps"
    # 备份根目录
    backup_dir = "D:/系统更新备份/2022"
    # 缓存目录
    cache_dir = "D:/apache-tomcat-8.5.38/work/Catalina/localhost"
    # url
    url = "http://127.0.0.1:8383/assist-mis"

    try:
        start_time = int(time.time())
        if not os.path.exists(war_file_name):
            print("当前目录未找到文件 %s ，部署终止\n" % war_file_name)
            input("按下回车键退出当前窗口")
            sys.exit(0)

        print("【1/5】原文件正在备份，请稍候...\n")
        date_str = time.strftime('%Y%m%d', time.localtime(time.time()))
        project_dir = work_dir + "/" + war_file_name[:war_file_name.find(".")]
        out_zip_dir = "{}/{}".format(backup_dir, date_str)
        if not os.path.exists(out_zip_dir):
            os.makedirs(out_zip_dir)

        if AutoRelease.archive_file(out_zip_dir + "/" + zip_file_name, project_dir):
            print("备份完成，路径：" + out_zip_dir + "/" + zip_file_name + "\n")

        print("【2/5】正在停止服务 %s，请稍候..." % service_name + "\n")
        AutoRelease.stop_service(service_name)
        # AutoRelease.close_process(port)
        during_time_stop = 0;
        while True:
            pid = AutoRelease.get_pid(port)
            if pid == "" or pid == "0":
                print("服务 %s 已停止" % service_name + "\n")
                break
            time.sleep(1)
            during_time_stop += 1
            if during_time_stop == 60:
                print("服务 %s 停止超时，请手动停止" % service_name + "\n")

        print("【3/5】部署新文件，请稍候...\n")
        AutoRelease.copy_file(war_file_name, out_zip_dir)
        if os.path.isfile(work_dir + "/" + war_file_name):
            os.remove(work_dir + "/" + war_file_name)
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir, True)
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir, True)
        AutoRelease.copy_file(war_file_name, work_dir)
        print("新文件部署完成\n")

        print("【4/5】正在启动服务 %s，请稍候...\n" % service_name)
        AutoRelease.start_service(service_name)
        during_time_start = 0
        while True:
            if AutoRelease.get_pid(port) != "":
                print("服务 %s 已启动\n" % service_name)
                break
            time.sleep(1)
            during_time_start += 1
            if during_time_start == 60:
                print("服务 %s 启动超时，请手动启动\n" % service_name)

        print("【5/5】正在检测应用是否可以正常访问，请稍候...\n")
        during_time_access = 0
        while True:
            if AutoRelease.get_http_status(url):
                print("应用已可以正常访问\n")
                break
            time.sleep(5)
            during_time_access += 5
            if during_time_access == 60:
                print("应用访问超时\n")
    except Exception as e:
        print("部署异常：{}\n".format(str(e)))
    else:
        print("{0}{1}{0}\n".format("*" * 27, "部署完毕"))
        print("耗时 {} 秒\n".format(int(time.time()) - start_time))
        webbrowser.open(url)

    input("按下回车键退出当前窗口")
    # os.system("pause")


if __name__ == "__main__":
    run()
