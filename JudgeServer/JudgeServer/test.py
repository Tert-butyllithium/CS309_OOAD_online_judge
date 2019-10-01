from multiprocessing import Process
import os
import psutil


def test():
    # process = psutil.Process(os.getpid())
    # print(os.getpid())
    # print(psutil.pids())
    # print(process.memory_info().rss/1024/1024)
    # print(os.system('top -p ' + str(pid)))
    print("hello")

p = Process(target=test)
# print(p)
p.start()
print(p.pid)