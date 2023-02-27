from lib import system
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/<proc_id>')
def index(proc_id=None):
    chart_url = f"/chart/{proc_id}" if proc_id else "/chart"

    return render_template('index.html', system=system.information(proc_id=proc_id),
                                         processes=system.processes(),
                                         chart_url=chart_url)

@app.route('/chart/')
@app.route('/chart/<proc_id>')
def chart(proc_id=None):
    return system.chart(proc_id=proc_id)