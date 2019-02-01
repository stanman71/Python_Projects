from flask import Flask
from app import app_index


""" ################# """
""" genernal settings """
""" ################# """

sys.path.insert(0, "C:/Users/stanman/Desktop/Unterlagen/GIT/Python_Projects/RasPi/SmartHome/")
sys.path.insert(0, "C:/Users/mstan/GIT/Python_Projects/RasPi/SmartHome/led")
sys.path.insert(0, "/home/pi/Python/SmartHome/led")

# Windows Home
PATH_CSS = 'C:/Users/stanman/Desktop/Unterlagen/GIT/Python_Projects/RasPi/SmartHome/static/CDNJS/'

# Windows Work
#PATH_CSS = 'C:/Users/mstan/GIT/Python_Projects/RasPi/SmartHome/static/CDNJS/'

# RasPi:
#PATH_CSS = '/home/pi/Python/static/CDNJS/'


from colorpicker_local import colorpicker
from LED_database import *
from LED_control import *


""" ######### """
""" schedular """
""" ######### """

from flask_apscheduler import APScheduler

scheduler = APScheduler()

@scheduler.task('cron', id='scheduler_job', minute='*')
def scheduler_job():
    now = datetime.datetime.now()
    print(now.strftime('%a'))
    print(now.strftime('%H'))
    print(now.strftime('%M'))


""" ##### """
""" flask """
""" ##### """

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
Bootstrap(app)
colorpicker(app)

if __name__ == '__main__':
    scheduler.start()
    app.run()