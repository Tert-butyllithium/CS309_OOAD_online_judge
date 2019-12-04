import sys
import os
import lorun
from config import LANGUAGE
result = {
    'error': '',
    'TLE': False,
    'time': 0,
    'MLE': False,
    'memory': 0
}
taskThread_end = False
source_listener_end = False


def run_args(code_file, language, output_folder):
    args = []
    if language == LANGUAGE.C.value or language == LANGUAGE.CPP.value:
        args = [code_file]
    elif language == LANGUAGE.JAVA.value:
        args = ['java', '-XX:-UseCompressedClassPointers', '-cp', f'{output_folder}/', 'Main']
    elif language == LANGUAGE.PY2.value:
        args = ['python2', code_file]
    elif language == LANGUAGE.PY3.value:
        args = ['python3', code_file]
    elif language == LANGUAGE.KOTLIN.value:
        args = ['java', '-XX:-UseCompressedClassPointers', '-jar', f'{code_file}.jar']
    return args


def main(argv):
    OJ_AC = 4
    OJ_PE = 5
    OJ_WA = 6
    OJ_TL = 7
    OJ_ML = 8
    OJ_OL = 9
    OJ_RE = 10
    OJ_CE = 11

    mapping = {
        0: OJ_AC,
        1: OJ_PE,
        2: OJ_TL,
        3: OJ_ML,
        4: OJ_WA,
        5: OJ_RE,
        6: OJ_OL,
        7: OJ_CE,
        8: -1
    }
    code_path = argv[1]
    input_folder = argv[2]
    output_folder = argv[3]
    language = int(argv[4])
    time_limit = int(argv[5])
    memory_limit = int(argv[6])
    docker_result_log = argv[7]

    res = {
        'result': -1,
        'timeused': -1,
        'memoryused': -1,
        'error': ''
    }
    mle_error = 'failed; error=\'Not enough space\''
    
    # r = open('/home/lumia/CS309_OOAD_online_judge/judger/tmp.file', 'w+')
    for testcase in os.listdir(input_folder):
        if not testcase.endswith('.in'):
            continue
        base_name = os.path.splitext(testcase)[0]
        error_file = os.path.join(output_folder, f'{base_name}.err')
        out_file = os.path.join(output_folder, f'{base_name}.out')
        args = run_args(code_path, language, output_folder)
        fin = open(os.path.join(input_folder, testcase))
        fout = open(out_file, 'w')
        ferr = open(error_file, 'w')
        runcfg = {
            'args': args,
            'fd_in': fin.fileno(),
            'fd_out': fout.fileno(),
            'fd_err': ferr.fileno(),
            'timelimit': time_limit * 1000 * 2,  # in MS
            'memorylimit': memory_limit * 1024,  # in KB
        }
        rst = lorun.run(runcfg)
        # r.write(testcase)
        # r.write(str(rst))
        res['result'] = mapping[rst['result']]
        if rst['timeused'] > time_limit * 1000 or rst['memoryused'] > memory_limit * 1024:
            if rst['timeused'] > time_limit * 1000:
                res['result'] = OJ_TL
            elif rst['memoryused'] > memory_limit * 1024:
                res['result'] = OJ_ML
            res['timeused'] = rst['timeused']
            res['memoryused'] = rst['memoryused']
            error = open(error_file, 'r')
            res['error'] = error.read()
            error.close()
            break
        res['timeused'] = max(res['timeused'], int(rst['timeused']))
        res['memoryused'] = max(res['memoryused'], int(rst['memoryused']))
        error = open(error_file, 'r')
        res['error'] = error.read()
        if mle_error in res['error']:
            res['result'] = OJ_ML
            break
        error.close()
        if res['error']:
            res['result'] = OJ_RE
            break
        fin.close()
        fout.close()
        ferr.close()

    result = open(docker_result_log, 'w+')
    # r.close()
    result.write(str(res))
    result.close()



#     error_file = argv[1].split('2>')[-1].lstrip().rstrip()
#     command_without_error_file = argv[1].split('2>')[0]
#     run_code_command = command_without_error_file.split(
#         '<')[0].lstrip().rstrip().split(' ')
#     # run_code_command.append('-XX:MaxMetaspaceSize=128m')
#     # print(run_code_command)
#     # test_file = '/home/isc-/Desktop/CS309_OOAD_online_judge/judger/data/1000/2.in'
#     test_file = command_without_error_file.split('<')[1].split('>')[
#         0].lstrip().rstrip()
#     # out_file = '/home/isc-/Desktop/CS309_OOAD_online_judge/judger/userCodes/2.out'
#     out_file = command_without_error_file.split(
#         '<')[1].split('>')[1].lstrip().rstrip()

# #    print(error_file)
# #    print(run_code_command)
# #    print(test_file)
# #    print(out_file)

#     time_limit = int(argv[2].lstrip().rstrip())
#     memory_limit = int(argv[3].lstrip().rstrip())
#     docker_result_log = argv[4].lstrip().rstrip()
#     # print(docker_result_log)

#     fin = open(test_file)
#     fout = open(out_file, 'w')
#     ferr = open(error_file, 'w')
#     runcfg = {
#         'args': run_code_command,
#         # 'args': ['java', '-XX:-UseCompressedClassPointers'],
#         'fd_in': fin.fileno(),
#         'fd_out': fout.fileno(),
#         'fd_err': ferr.fileno(),
#         'timelimit': time_limit * 1000 * 2,  # in MS
#         'memorylimit': memory_limit * 1024,  # in KB


#     }
#     # print('runcfg', runcfg)
#     rst = lorun.run(runcfg)
#     # print('rst', rst)
#     if rst['result'] != 0:
#         rst['result'] = mapping[rst['result']]
#     if rst['timeused'] > time_limit * 1000:
#         rst['result'] = OJ_TL
#     if rst['memoryused'] > memory_limit * 1024:
#         rst['result'] = OJ_ML
#     error = open(error_file, 'r')
#     rst['error'] = error.read()
#     if rst['error']:
#         rst['result'] = OJ_RE
#     error.close()

#     fin.close()
#     fout.close()
#     result = open(docker_result_log, 'w+')
#     result.write(str(rst))
#     result.close()


if __name__ == '__main__':
    main(sys.argv)
