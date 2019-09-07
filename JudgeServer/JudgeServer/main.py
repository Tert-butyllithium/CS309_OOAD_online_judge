import pymysql
import docker
import threading
import time


class TimeoutThread(threading.Thread):
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout
        self.isCancel = False

    def setCancel(self):
        self.isCancel = True

    def run(self):
        print("守护线程开始")
        try:
            time.sleep(self.timeout)
            if not self.isCancel:
                # 超时，需要杀死，这里代码还没有实现
                raise NameError('TLE')
            else:
                print(self.isCancel)
        except InterruptedError:
            print("interrupted")


class TaskThread(threading.Thread):
    def __init__(self, timeout_thread):
        super().__init__()
        self.timeout_thread = timeout_thread
        self.timeout_thread.start()

    def run(self):
        try:
            # 这里的2是假设我的代码会在两秒内完成，用来替代真实步骤
            time.sleep(2)
            client = docker.from_env()
            # 新建一个container，参数是镜像，这里是随便的一个
            client.containers.create("registry.cn-hangzhou.aliyuncs.com/onlinejudge/judge_server")
            self.timeout_thread.setCancel()
        except InterruptedError:
            print("interrupted")

def connect_DB():
    return True
    # 连接数据库
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='xxx',
        db='mysql'
    )


def main():
    if connect_DB():
        try:
            # 这里的3是limit，超过3s就失效
            tt = TimeoutThread(3)
            thread = TaskThread(tt)
            thread.start()
            thread.join()
        except:
            print("Error: The thread cannot be start")


if __name__ == '__main__':
    main()

# client = docker.from_env()
# client.containers.run('registry.cn-hangzhou.aliyuncs.com/onlinejudge/judge_server')
