from flask import Flask, request
from Judge_Service import JudgeService
from config import logger
import sys

app = Flask(__name__)
js = JudgeService()


@app.route('/api/judge', methods=['POST'])
def new_task():
    # _token = request.headers.get('Cs309-Token')
    #    if _token != token:
    #       return {
    #          'result': 0,
    #         'info': 'Invalid token'
    #    }
    if not js.running:
        js.run()
        # return {
        #   'result': 0,
        #  'info': 'The judge sevice has not been started yep. Please start the service before transferring the solution id.'
    # }
    _solution_id = request.form.get('solutionId')
    logger.debug(f'Insert task {_solution_id}')
    js.new_task(_solution_id)
    return {
        'result': 1,
        'info': 'solutionId: ' + str(_solution_id) + ' has been added to the task queue.'
    }


if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) > 1 else 5000
    host = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
    debug = sys.argv[3] if len(sys.argv) > 3 else None
    js.run()
    app.run(port=port, host=host, debug=debug)
