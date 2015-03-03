import json
import time
import sys
from database import Database
from metric.metric_manager import MetricManager
from diagnostic.diagnoser_manager import DiagnoserManager


if __name__ == '__main__':
    len_argv = len(sys.argv)
    if len_argv == 2:
        cur_time = int(time.time())
        try:
            begin = cur_time - (60*int(sys.argv[1]))
        except ValueError:
            print('error: <last_n_minutes> must be an integer')
            sys.exit(101)
        end = cur_time
    elif len_argv == 3:
        try:
            begin = int(sys.argv[1])
        except ValueError:
            print('error: <initial_timestamp> must be an integer')
            sys.exit(101)
        try:
            end = int(sys.argv[2])
        except ValueError:
            print('error: <final_timestamp> must be an integer')
            sys.exit(101)
        if end < begin:
            error_msg = 'error:\n'
            error_msg += '\t<final_timestamp> cannot be before '
            error_msg += '<initial_timestamp>'
            print(error_msg)
            sys.exit(404)
    else:
        usage_msg = 'usage:\n'
        usage_msg += '\tpython3 repd.py <last_n_minutes>\n'
        usage_msg += '\tpython3 repd.py <initial_timestamp> <final_timestamp>'
        print(usage_msg) 
        sys.exit(505)

    # load database settings and create handler
    with open('settings/database.cfg', 'r') as f:
        s = json.load(f)
        database = Database(s['filename'])

    # create MetricManager
    metric_manager = MetricManager(database)

    # load diagnoser_manager settings and create object
    with open('settings/diagnoser_manager.cfg', 'r') as f:
        diagnosers = json.load(f)
        diagnostic = DiagnoserManager(metric_manager, diagnosers)

    diagnostics = diagnostic.diagnose((begin, end))
    for diag in diagnostics:
        print(diag)
