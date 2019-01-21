from flask import Flask, render_template
# from flask_colorpicker import colorpicker
# Some junk to solve loading module path from parent dir
from sys import path
from os import getcwd, name
splitter = '\\' if name == 'nt' else '/'
path.append(
    splitter.join(
        getcwd().split(
            splitter
        )[:-1]
    )
)
# End of junk
from color import colorpicker

app = Flask(__name__, template_folder='.')

#colorpicker(app, local=['./Python_Projects/flask_colorpicker-master/testing_example/static/js/spectrum.js', './Python_Projects/flask_colorpicker-master/testing_example/static/css/spectrum.css'])

colorpicker(app)

print(colorpicker.loader)

@app.route('/')
def root():
    return render_template('index.html')


app.run(debug=True, port=4000)


