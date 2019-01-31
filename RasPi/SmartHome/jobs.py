from flask import Flask
from flask_scheduler import APScheduler


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'jobs:job1',
            'args': (1, 3),
            'trigger': 'interval',
            'seconds': 10
        },
        {
            'id': 'job2',
            'func': 'jobs:job2',
            'args': (5, 0),
            'trigger': 'cron',
            'minute': 46
        }
    ]

    SCHEDULER_API_ENABLED = True


def job1(a, b):
    print(str(a) + ' ' + str(b))

    # Frage Datenbank ab:
    # Eintrag für aktuelle Minute vorhanden ?
    # Prozess starten
    

def job2(c, d):
    print(str(c))


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config())

    scheduler = APScheduler()
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run()
