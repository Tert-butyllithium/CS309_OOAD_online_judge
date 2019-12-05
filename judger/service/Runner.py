import sys
import os
import lorun
from config import LANGUAGE
from config import logger
from config import USER_CODES_FOLDER
from config import LIMIT

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
    # elif language == LANGUAGE.PY2.value:
        # args = ['python2', code_file]
    elif language == LANGUAGE.PY3.value:
        args = ['pypy3', code_file]
    elif language == LANGUAGE.KOTLIN.value:
        args = ['java', '-XX:-UseCompressedClassPointers', '-jar', f'{code_file}.jar']
    return args

# def compare(spj, ):
#     def compare_output_spj(self, output_folder, standard_output_folder):
#         logger.info(standard_output_folder)
#         spj_cpp = f'{standard_output_folder}/spj.cpp'
#         spj_exec = spj_cpp[0:len(spj_cpp) - 4]
#         if os.path.exists(spj_cpp):
#             compile_result = self.exec_cmd(f'g++ {spj_cpp} -o {spj_exec}')
#             if compile_result:
#                 raise Exception("Compile spj.cpp error")
#         else:
#             raise Exception(f'File spj.cpp not found in \'{spj_cpp}\'')
#         for TC_out in os.listdir(standard_output_folder):
#             if not TC_out.endswith('.out'):
#                 continue
#             TC_out = f'{standard_output_folder}/{TC_out}'
#             TC_in = TC_out[0:len(TC_out) - 4] + '.in'
#             if not os.path.exists(TC_in):
#                 raise Exception(TC_in + ' not found but ' + TC_out + ' found')
#             TC_id = TC_out[len(standard_output_folder): len(TC_out) - 4]
#             user_out = output_folder + TC_id + '.out'
#             if not os.path.exists(user_out):
#                 return False
#             result = os.system(f'{spj_exec} {TC_in} {TC_out} {user_out}')
#             if result != 0:
#                 return False
#         return True

#     def compare_output(self, output, standard):
#         success_count = 0
#         fail_count = 0
#         file_count = 0
#         user_output_list = os.listdir(output_folder)
#         for out_file in user_output_list:
#             if not out_file.endswith('.out'):
#                 continue
#             file_count += 1
#             out_file_path = f'{output_folder}/{out_file}'
#             stan_file_path = f'{standard_output_folder}/{out_file}'
#             outfile = open(out_file_path)
#             stan_file = open(stan_file_path)
#             # while outfile.newlines() :
#             while outfile.readable() or stan_file.readable():
#                 out = outfile.readline()
#                 stan = stan_file.readline()
#                 if not out and not stan:
#                     success_count += 1
#                     break
#                 if bool(out) != bool(stan):
#                     fail_count += 1
#                     break
#                 if not stan and out == '\n':
#                     success_count += 1
#                     break
#                 if out.strip() != stan.strip():
#                     fail_count += 1
#                     break
#             outfile.close()
#             stan_file.close()
#         if success_count == file_count:
#             return True
#         else:
#             return False
#     if spj == 1:
#         return compare_output_spj()
#     else:
#         return compare_output()

def compare_output(stan_file, user_file):
    out_data = open(user_file)
    stan_data = open(stan_file)
    while out_data.readable() or stan_data.readable():
        out = out_data.readline()
        stan = stan_data.readline()
        # logger.debug(f'out: {out}')
        # logger.debug(f'stan: {stan}')
        if not out and not stan:
            return True
        if bool(out) != bool(stan):
            return False
        if not stan and out == '\n':
            return True
        if out.strip() != stan.strip():
            return False
    return True 


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
        'result': 4,
        'timeused': -1,
        'memoryused': -1,
        'error': ''
    }
    mle_error = 'failed; error=\'Not enough space\''
    
    # r = open('/home/lumia/CS309_OOAD_online_judge/judger/tmp.file', 'w+')
    test_cases = os.listdir(input_folder)
    test_cases.sort()
    for testcase in test_cases:
        if not testcase.endswith('.in'):
            continue
        logger.debug(f'test:{testcase}')
        base_name = os.path.splitext(testcase)[0]
        error_file = os.path.join(output_folder, f'{base_name}.err')
        out_file = os.path.join(output_folder, f'{base_name}.out')
        stan_file = os.path.join(input_folder, f'{base_name}.out') 
        args = run_args(code_path, language, output_folder)
        logger.debug(args)
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
        fin.close()
        fout.close()
        ferr.close()
        # r.write(testcase)
        # r.write(str(rst))
        logger.debug(f'runner: {rst}')
        if rst['result'] == 5 :
            if rst['re_signum'] == 11:
                res['result'] = OJ_ML
                res['timeused'] = rst['timeused']
                res['memoryused'] = rst['memoryused']
                break


        if res['result'] > 8:
            res['result'] = 0
        else:
            res['result'] = mapping[rst['result']]

        if rst['timeused'] > time_limit * 1000:
            res['result'] = OJ_TL
        elif rst['memoryused'] > memory_limit * 1024 and language != LANGUAGE.JAVA.value:
            res['result'] = OJ_ML
        elif rst['memoryused'] > (memory_limit - LIMIT.JAVA_SPACE_BONUS.value) * 1024 and language == LANGUAGE.JAVA.value:
            res['result'] = OJ_ML
        # res['timeused'] = rst['timeused']
        # res['memoryused'] = rst['memoryused']
        error = open(error_file, 'r')
        res['error'] = error.read()
        error.close()
        # logger.debug('#######################')
        # logger.debug(res['timeused'])
        # logger.debug(int(rst['timeused']))
        # logger.debug('#######################')
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
        if not compare_output(stan_file, out_file):
            logger.debug("helloworld")
            res['result'] = OJ_WA
            break

    os.system(f'rm -rf {output_folder}/*')
    result = open(docker_result_log, 'w+')
    # r.close()
    result.write(str(res))
    result.close()

if __name__ == '__main__':
    main(sys.argv)

