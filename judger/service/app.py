from flask import Flask, request
from Judge_Service import JudgeService
# from config import token
import sys

app = Flask(__name__)
js = JudgeService()


# @app.route('/api/startJudger', methods=['POST'])
# def start():
#     # _token = request.headers.get('Cs309-Token')
#  #   if _token != token:
#   #      return {
#    #         'result': 0,
#     #        'info': 'Invalid token'
#      #   }
#     js.run()
#     return {
#         'result': 1,
#         'info': "The judgeService has been started successfully."
#     }


@app.route('/api/judge', methods=['POST'])
def new_task():
    # _token = request.headers.get('Cs309-Token')
#    if _token != token:
 #       return {
  #          'result': 0,
   #         'info': 'Invalid token'
    #    }
    if not js.running:
        return {
            'result': 0,
            'info': 'The judge sevice has not been started yep. Please start the service before transferring the solution id.'
        }
    _solution_id = request.form.get('solutionId')
    js.new_task(_solution_id)
    return {
        'result': 1,
        'info': 'solutionId: ' + str(_solution_id) + ' has been added to the task queue.'
    }


if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) > 1 else None
    host = sys.argv[2] if len(sys.argv) > 2 else None
    debug = sys.argv[3] if len(sys.argv) > 3 else None
    js.run()
    app.run(port=port, host=host, debug=debug)
