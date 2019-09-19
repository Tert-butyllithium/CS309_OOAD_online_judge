import threading
import time
import docker
import os


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
                # raise NameError('TLE')

                pass
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
            time.sleep(1)
            client = docker.from_env()
            # 新建一个container，参数是镜像，这里是随便的一个
            print(os.system(
                "docker run --mount type=bind,source=/home/data/Code/2019fall/OJ_template/Judger/demo/,target=/Judger/mount judge:v2 python3 Judger/mount/demo.py main"))
            self.timeout_thread.setCancel()
        except InterruptedError:
            print("interrupted")