from flask import Flask, render_template, redirect, url_for,request
from flask import make_response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("test.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        car_brand = request.form.get("cars", None)
        if car_brand!=None:
            return render_template("test.html", car_brand = car_brand)
    return render_template("test.html")

if __name__ == '__main__':
    app.run(debug=True)
