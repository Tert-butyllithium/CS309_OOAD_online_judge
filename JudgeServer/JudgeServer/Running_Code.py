import sys
import threading
import time
import os


class TimeoutThread(threading.Thread):
    # 这里的timeout是假设我的代码会在两秒内完成，用来替代真实步骤
    def __init__(self, command, timeout):
        super().__init__()
        self.timeout = float(timeout)
        self.result = {
            'error': '',
            'TLE': False,
            'time': 0
        }
        self.end = False
        self.taskThread = TaskThread(command)

    def run(self):
        startTime = time.time()
        self.taskThread.start()
        while time.time() - startTime <= self.timeout:
            continue
        if not self.taskThread.end:
            self.result['TLE'] = True
            self.result['time'] = self.timeout + 0.1
        else:
            self.result['error'] = self.taskThread.result['error']
            self.result['time'] = self.taskThread.result['time']
        self.end = True
        return self.result


class TaskThread(threading.Thread):
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.end = False
        self.result = {
            'error': '',
            'time': 0
        }

    def run(self):
        startTime = time.time()
        result = exec_cmd(self.command)
        endTime = time.time()
        self.result['error'] = result
        self.result['time'] = endTime - startTime
        self.end = True


def exec_cmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text


def main(argv):
    command = argv[1]
    timeout = argv[2]
    userCodes_folder = argv[3]
    output_file = userCodes_folder + '/docker_result.log'
    runtime_result = userCodes_folder + '/runtime_result.log'
    timeoutThread = TimeoutThread(command, timeout)
    timeoutThread.start()
    while not timeoutThread.end:
        pass
    while not os.path.exists(runtime_result):
        pass
    time.sleep(0.1)
    with open(runtime_result, 'r') as file:
        timeoutThread.result['error'] = file.read()
        file.close()
    with open(output_file, 'w+') as file:
        saved_stdout = sys.stdout
        sys.stdout = file
        print(timeoutThread.result)
        sys.stdout = saved_stdout
        file.close()



class DockerThread(threading.Thread):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        os.system(self.command)


if __name__ == '__main__':
    main(sys.argv)
