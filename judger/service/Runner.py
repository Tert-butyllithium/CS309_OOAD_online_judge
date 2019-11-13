import sys
import lorun
result = {
    'error': '',
    'TLE': False,
    'time': 0,
    'MLE': False,
    'memory': 0
}
taskThread_end = False
source_listener_end = False


def main(argv):
    OJ_PE = 5
    OJ_WA = 6
    OJ_TL = 7
    OJ_ML = 8
    OJ_OL = 9
    OJ_RE = 10
    OJ_CE = 11

    mapping = {
        1: OJ_PE,
        2: OJ_TL,
        3: OJ_ML,
        4: OJ_WA,
        5: OJ_RE,
        6: OJ_OL,
        7: OJ_CE,
        8: -1
    }
    # Runner path, exec file path, < , input test data, > , output path
    # print(argv)
    # run_code_command = argv[1].split('<')[0].lstrip().rstrip().split(' ')
    # test_file = argv[1].split('<')[1].split('>')[0].lstrip().rstrip()
    # out_file = argv[1].split('<')[1].split('>')[1].lstrip().rstrip()
    # time_limit = argv[2].lstrip().rstrip()
    # memory_limit = argv[3].lstrip().rstrip()
    # os.system(argv[1])
    # print(argv[1])
    # run_code_command = argv[1].split(' ')
    # print(run_code_command)
    run_code_command = argv[1].split('<')[0].lstrip().rstrip().split(' ')
    # run_code_command.append('-XX:MaxMetaspaceSize=128m')
    # print(run_code_command)
    # test_file = '/home/isc-/Desktop/CS309_OOAD_online_judge/judger/data/1000/2.in'
    test_file = argv[1].split('<')[1].split('>')[0].lstrip().rstrip()
    # out_file = '/home/isc-/Desktop/CS309_OOAD_online_judge/judger/userCodes/2.out'
    out_file = argv[1].split('<')[1].split('>')[1].lstrip().rstrip()
    time_limit = int(argv[2].lstrip().rstrip())
    memory_limit = int(argv[3].lstrip().rstrip())
    docker_result_log = argv[4].lstrip().rstrip()
    # print(docker_result_log)

    fin = open(test_file)
    fout = open(out_file, 'w')
    runcfg = {
        'args': run_code_command,
        #'args': ['java', '-XX:-UseCompressedClassPointers'],
        'fd_in': fin.fileno(),
        'fd_out': fout.fileno(),
        'timelimit': time_limit * 1000,  # in MS
        'memorylimit': memory_limit * 1024,  # in KB
    }
    print('runcfg', runcfg)
    rst = lorun.run(runcfg)
    print('rst', rst)
    if rst['result'] != 0:
        rst['result'] = mapping[rst['result']]
    if rst['result'] == OJ_RE:
        error_file = open(out_file, 'r')

        rst['error'] = error_file.read()
        error_file.close()
    else:
        rst['error'] = ''
    fin.close()
    fout.close()
    result = open(docker_result_log, 'w')
    result.write(str(rst))
    result.close()


if __name__ == '__main__':
    main(sys.argv)
