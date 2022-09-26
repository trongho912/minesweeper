from flask import *
from pymongo import *
import getboard
from minesweeper import *

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client["minesweeper_db"]


@app.route('/')
def demo():
    return render_template('base.html')

@app.route('/answer')
def result():
    return render_template('answer.html')

@app.route('/minesweeper')
def minesweeper():
    return render_template('minesweeper.html')

if __name__ == "__main__":
    app.run(debug=True)