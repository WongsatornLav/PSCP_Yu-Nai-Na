from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report_lost')
def report_lost():
    return render_template('rp_L.html')

@app.route('/report_found')
def report_found():
    return render_template('rp_F.html')

@app.route('/sign-in')
def signin():
    return render_template('signin.html')

if __name__=="__main__":
    app.run()