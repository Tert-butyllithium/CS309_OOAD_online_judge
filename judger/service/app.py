from flask import Flask, request, make_response
from Judge_Service import JudgeService
from config import logger
from config import TOKEN
from config import DATA_PATH
from config import TMP_PATH
from Judge_Service import js
import sys
import os

app = Flask(__name__)


@app.route('/api/judge', methods=['POST'])
def new_task():
    if not js.running:
        js.run()
    _solution_id = request.json['solutionId'][0]
    logger.info(f'Insert task {_solution_id}')
    # js.new_task(_solution_id)
    return {
        'result': 1,
        'info': 'solutionId: ' + str(_solution_id) + ' has been added to the task queue.'
    }

# @app.route('/getTestData', methods=['GET'])
# def get_test_data():
#     if not js.running:
#         res = make_response('The judger server does not run.', 403)
#         return res
#     _token = request.json['token'][0]
#     _problem_id = request.json['problem_id'][0]
#     if _problem_id == '' or _token == '':
#         res = make_response('Invalid Argument.', 400)
#     if _token != TOKEN:
#         res = make_response('Invalid Token.', 401)
#         return res
#     problem_folder = f'{DATA_PATH}/{_problem_id}'
#     zip_name = f'{TMP_PATH}/{_problem_id}/.zip'
#     command = f'zip {zip_name} -r {problem_folder}'
#     os.system(command)
#     while not os.path.exists(zip_name):
#         time.sleep(1)
#     res = make_response(send_file(zip_name), 200)
#     return res
    
# @app.route('/setTestData', methods=['GET'])
# def set_test_data():
#     if not js.running:
#         res = make_response('The judger server does not run.', 403)
#         return res
    

if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) > 1 else 5000
    host = sys.argv[2] if len(sys.argv) > 2 else '0.0.0.0'
    debug = sys.argv[3] if len(sys.argv) > 3 else None
    js.run()
    app.run(port=port, host=host, debug=debug)
