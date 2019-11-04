import signal
import sys
import threading
import lorun
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


def run(command):
    def exec_cmd(cmd):
        r = os.popen(cmd)
        text = r.read()
        r.close()
        return text
    error = exec_cmd(command + ' 2> /home/isc-/Desktop/CS309_OOAD_online_judge/judger/userCodes/runtime_result.log')


def main(argv):
    # Runner path, exec file path, < , input test data, > , output path
    print(argv)


if __name__ == '__main__':
    main(sys.argv)
