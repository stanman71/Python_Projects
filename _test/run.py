from flask import Flask
from flask_apscheduler import APScheduler
 
import time
 
app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
 
@app.route('/')
def welcome():
    return 'Welcome to flask_apscheduler demo', 200
 
@app.route('/run-tasks')
def run_tasks():
    sched.add_job(my_job, 'cron', hour='1,2', args=['text'])
 
    return 'Scheduled several long running tasks.', 200
 
         
app.run(debug = True)