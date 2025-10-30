from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report-lost')
def report_lost():
    return render_template('rp_L.html')

@app.route('/report-found')
def report_found():
    return render_template('rp_F.html')

if __name__ == '__main__':
    app.run(debug=True)
