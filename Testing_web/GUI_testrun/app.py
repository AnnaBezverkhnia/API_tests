from multiprocessing.connection import Connection
from flask import Flask, render_template, make_response
from flask import redirect, request, jsonify, url_for
import pytest
import multiprocessing
from multiprocessing import Pipe
from multiprocessing.connection import Connection
import socket
from init_db import DataModel
from constants import *
from werkzeug import Response
from waitress import serve
from pathlib import Path


app = Flask(__name__)

# get local machine Ip adress
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
host = s.getsockname()[0]
s.close()

root_dir = str(Path(__file__).parent.parent)

# dict to hold devices testrun statuses
testruns: dict = {}

# Pipe() returns two connection object connected by a pipe
# Allows to receive and update global variable within processes
submit_results, process_results = Pipe()

# generate database and display its data  on main page


@app.route("/")
def base() -> str:
    data = DataModel(database, polygon_devices, db_schema_path, table_name)
    data.generate_database()
    intercoms = data.get_device()
    return render_template('intercoms_table.html', intercoms=intercoms)

# #### start test run on chosen device ###


'''
/POSTMETOD: the route is usded by JS function startTest (see main.js), which collects
the data from user inputs and passed it to the backend. Data are pytestArgs, device_id, html-report info etc.
'''


@app.route("/postmethod", methods=['POST'])
def post_javascript_data() -> list[str]:
    pytestArgs: list[str] = ['-v']
    for key, value in request.form.items():
        match key:
            case 'dev_id':
                dev_id = value
            case 'report_html':
                value = f'--html={root_dir}\\GUI_testrun\\static\\{value}'
                pytestArgs.append(value)
            case _:
                pytestArgs.append(value)
    print(pytestArgs)
    global testruns
    # Change device testrun status to 'in progress'

    testruns[dev_id] = 'in progress'

    # each testrun will be set up as an instance of multiprocessing.Process
    process = multiprocessing.Process(target=pytest_run, args=(pytestArgs, dev_id, submit_results))
    process.start()

    return pytestArgs

# the target function for Processes. Runs the tests and informs the backend about the end of testrun
# using standard post reqest with device id and tesrun status ('completed') as url parametres.


def pytest_run(pytestArgs: list[str], dev_id: str, results: Connection) -> None:
    '''
    :pytestArgs: pytest arguments to be passed when initializing a testrun
    :dev_id: the id of the device used for the restrun
    :results: connection object, used for updating testrun status. When testrun on the device is completed,
    its status will be set up to "completed".
    '''
    pytest.main(pytestArgs)
    results.send({dev_id: 'completed'})

# /STATUS route is used by AJAX requests, sent every 10s to receive testrun status update for each testrun.


@app.route('/status', methods=['GET'])
def process_status() -> dict:
    """ Return the status of the worker process """
    if process_results.poll(timeout=0.1):
        result: dict = process_results.recv()
        testruns.update(result)
    return testruns

# # # ----------------------------------------------------------

# /REPORT route is used for accessing html-reports generated for each testrun.
# reports are identified by DUT Ip addsress


@app.route('/report', methods=['GET', 'POST'])
def report() -> Response:
    ip = request.form['ip']
    return redirect(url_for('static', filename=f'{ip}report.html'))


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5001, url_prefix='/run_autotest')
