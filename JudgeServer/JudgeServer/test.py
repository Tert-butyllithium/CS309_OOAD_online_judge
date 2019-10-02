from multiprocessing import Process
import os
import psutil


def test():
    s = 'qwefsfsdfsdf/'
    str = s + 'nqisjdnjsdnasd.cpp'
    print(str[len(s): len(str) - 4])

test()