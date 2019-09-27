import threading
import time
import os
from config import logger
from config import OJ_TL
from config import OJ_AC

class TimeoutThread(threading.Thread):
    # 这里的timeout是假设我的代码会在两秒内完成，用来替代真实步骤
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout
        self.isCancel = False
        self.result = {
            'time': 0,
            'result': 0,
            'running_success': True
        }

    def setCancel(self):
        self.isCancel = True

    def run(self):
        try:
            logger.debug(self.timeout)
            time.sleep(self.timeout)
            if not self.isCancel:
                if self.container_name:
                    self.result['result'] = OJ_TL
                    self.result['running_success'] = False
                    os.system('docker stop ' + str(self.container_name))
                else:
                    logger.error("Do not have a container_name in time out thread.")
        except InterruptedError:
            print("interrupted")

