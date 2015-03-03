import json
import time
from database import Database
from metric.metric_manager import MetricManager
from metric.monitor_manager import MonitorManager


def main():
    # load database settings and create handler
    with open('settings/database.cfg', 'r') as f:
        s = json.load(f)
        database = Database(s['filename'])
    
    # create MetricManager
    metric_manager = MetricManager(database)

    # load monitor_manager settings and create object
    with open('settings/monitor_manager.cfg', 'r') as s:
        resources = json.load(s)
        monitor_manager = MonitorManager(metric_manager, resources)
    
    try:
        monitor_manager.start()
        while True:
            print('Press control-c to quit')
            time.sleep(3600)
    except KeyboardInterrupt:
        print('\rQuitting, this may take a while')
        monitor_manager.stop()


if __name__ == '__main__':
    main()
