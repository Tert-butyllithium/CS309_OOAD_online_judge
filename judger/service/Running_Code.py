import sys
import threading
import time
import os
import psutil
from multiprocessing import Process

result = {
    'error': '',
    'TLE': False,
    'time': 0,
    'MLE': False,
    'memory': 0
}
taskThread_end = False
source_listener_end = False

lock = threading.Lock()


class SourceListener(threading.Thread):
    def __init__(self, time_limit, memory_limit, process, initial_memory):
        super().__init__()
        self.time_limit = float(time_limit)
        self.initial_memory = initial_memory
        self.process = process
        self.memory_limit = memory_limit

    def run(self):
        global result
        global taskThread_end
        global source_listener_end
        max_memory = -1
        startTime = time.time()
        while time.time() - startTime <= self.time_limit and not taskThread_end:
            if not taskThread_end:
                memory = self.process.memory_full_info().rss / 100
                max_memory = max(max_memory, memory)
                if memory - self.initial_memory >= int(self.memory_limit):
                    lock.acquire()
                    result['MLE'] = True
                    result['memory'] = memory - self.initial_memory
                    taskThread_end = True
                    lock.release()
        lock.acquire()
        if taskThread_end:
            result['time'] = time.time() - startTime
        else:
            result['TLE'] = True
            result['time'] = self.time_limit + 0.1
            taskThread_end = True
        result['memory'] = max_memory - self.initial_memory
        source_listener_end = True
        lock.release()


class TaskThread(threading.Thread):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        # startTime = time.time()
        global result
        global taskThread_end
        error = exec_cmd(self.command)
        # endTime = time.time()
        lock.acquire()
        taskThread_end = True
        result['error'] = error
        lock.release()
        # self.result['time'] = endTime - startTime


def run(command):
    # startTime = time.time()
    global result
    global taskThread_end
    error = exec_cmd(command)
    # endTime = time.time()
    lock.acquire()
    taskThread_end = True
    result['error'] = error
    lock.release()
    # self.result['time'] = endTime - startTime


def exec_cmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text


def main(argv):
    # /home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/Main < /home/isc-/Desktop/CS309_OOAD_online_judge/data/1001/2.in > /home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/2.out
    command = argv[1]
    time_limit = argv[2]
    memory_limit = argv[3] * 1024
    userCodes_folder = argv[4]

    p = Process(target=run, args=(command,))
    # print(psutil.pids())
    # pp = psutil.Process(p.pid)

    output_file = userCodes_folder + '/docker_result.log'
    runtime_result = userCodes_folder + '/runtime_result.log'
    # taskThread = TaskThread(command)
    p.start()
    process = psutil.Process(p.pid)
    print(psutil.pids())
    print(process.pid)
    source_listener = SourceListener(time_limit, memory_limit, process, process.memory_full_info().rss / 100)
    source_listener.start()
    # taskThread.start()
    while not os.path.exists(runtime_result) or not taskThread_end or not source_listener_end:
        # print((taskThread_end, timeoutThread_end, memoryThread_end))
        pass
    time.sleep(0.1)
    # print(taskThread.result)
    lock.acquire()
    lock.release()
    with open(runtime_result, 'r') as file:
        result['error'] = file.read()
        file.close()
    with open(output_file, 'w+') as file:
        saved_stdout = sys.stdout
        sys.stdout = file
        lock.acquire()
        print(result)
        lock.release()
        sys.stdout = saved_stdout
        file.close()


#
class DockerThread(threading.Thread):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        # docker run -u 1000:1000 --name 7615717558658269113 -v /home/isc-/Desktop/CS309_OOAD_online_judge/JudgeServer/JudgeServer/Running_Code.py:/home/isc-/Desktop/CS309_OOAD_online_judge/JudgeServer/JudgeServer/Running_Code.py -v /home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/:/home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/ -v /home/isc-/Desktop/CS309_OOAD_online_judge/data/1001/1.in:/home/isc-/Desktop/CS309_OOAD_online_judge/data/1001/1.in judge:v2 python3 /home/isc-/Desktop/CS309_OOAD_online_judge/JudgeServer/JudgeServer/Running_Code.py '/home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/Main < /home/isc-/Desktop/CS309_OOAD_online_judge/data/1001/1.in > /home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/1.out' 1.0 134217728 '/home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/' 2> /home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/runtime_result.log
        os.system(self.command)


if __name__ == '__main__':
    main(sys.argv)
