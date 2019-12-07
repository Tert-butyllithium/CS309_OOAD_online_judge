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
        args = ['java', '-XX:-UseCompressedClassPointers', '-jar', f'{code_file}']
    return args

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
    solution_id = os.path.split(output_folder)[1]

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
        logger.info(f'#{solution_id}# test:{testcase}')
        base_name = os.path.splitext(testcase)[0]
        error_file = os.path.join(output_folder, f'{base_name}.err')
        out_file = os.path.join(output_folder, f'{base_name}.out')
        stan_file = os.path.join(input_folder, f'{base_name}.out') 
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
        fin.close()
        fout.close()
        ferr.close()
        # r.write(testcase)
        # r.write(str(rst))
        # logger.debug(f'runner: {rst}')
        if rst['result'] == 5 :
            if rst['re_signum'] == 11:
                res['result'] = OJ_RE
                # res['error'] = 
                res['timeused'] = rst['timeused']
                res['memoryused'] = rst['memoryused']
                logger.info(f'#{solution_id}# Terminate because memory limit with the signum 11')
                break


        if res['result'] > 8:
            res['result'] = 0
        else:
            res['result'] = mapping[rst['result']]

        res['timeused'] = max(res['timeused'], int(rst['timeused']))
        res['memoryused'] = max(res['memoryused'], int(rst['memoryused']))
      
        if rst['timeused'] > time_limit * 1000:
            res['result'] = OJ_TL
            logger.info(f'#{solution_id}# Terminate because the time limit')
            break
        if language == LANGUAGE.JAVA.value and rst['memoryused'] > (memory_limit - LIMIT.JAVA_SPACE_BONUS.value) * 1024:
            res['result'] = OJ_ML
            logger.info(f'#{solution_id}# Terminate because the memory limit')
            break
        elif language == LANGUAGE.PY2.value and rst['memoryused'] > (memory_limit - LIMIT.PYTHON_SPACE_BONUS.value) * 1024:
            res['result'] = OJ_ML 
            logger.info(f'#{solution_id}# Terminate because the memory limit')
            break
        elif language == LANGUAGE.PY3.value and rst['memoryused'] > (memory_limit - LIMIT.PYTHON_SPACE_BONUS.value) * 1024:
            res['result'] = OJ_ML 
            logger.info(f'#{solution_id}# Terminate because the memory limit')
            break
        elif language == LANGUAGE.KOTLIN.value and rst['memoryused'] > (memory_limit - LIMIT.KT_SAPCE_BONUS.value) * 1024:
            res['result'] = OJ_ML 
            logger.info(f'#{solution_id}# Terminate because the memory limit')
            break
        elif (language == LANGUAGE.C.value or language == LANGUAGE.CPP.value)  and res['memoryused'] > (memory_limit - LIMIT.CPP_SPACE_BONUS.value) * 1024:
            res['result'] == OJ_ML
            logger.info(f'#{solution_id}# Terminate because the memory limit')
            break

        # res['timeused'] = rst['timeused']
        # res['memoryused'] = rst['memoryused']
        error = open(error_file, 'r')
        res['error'] = error.read()
        error.close()
        
        error = open(error_file, 'r')
        res['error'] = error.read()
        if mle_error in res['error']:
            res['result'] = OJ_ML
            logger.info(f'#{solution_id}# Terminate because the memory limit')
            break
        error.close()
        if res['error']:
            logger.info(f"#{solution_id}# Terminate because Runtime error with the error: {res['error']}")
            res['result'] = OJ_RE
            break
        if not compare_output(stan_file, out_file):
            logger.info(f'#{solution_id}# Terminate because wrong answer with the testcase being: {testcase}')
            res['result'] = OJ_WA
            break
    result = open(docker_result_log, 'w+')
    result.write(str(res))
    result.close()

if __name__ == '__main__':
    main(sys.argv)

