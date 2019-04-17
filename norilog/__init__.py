import json
from datetime import datetime

from flask import Flask, render_template, redirect, request, Markup, escape

application = Flask(__name__)

DATA_FILE = 'norilog.json'


def save_data(start, finish, memo, created_at):
    """
    Save the norilog data

    Parameters
    ----------
    start : str
    finish : str
    memo : str
    created_at : datetime
    """
    try:
        database = json.load(open(DATA_FILE, mode='r', encoding='utf-8'))
    except FileNotFoundError:
        database = []

    database.insert(0, {
        'start': start,
        'finish': finish,
        'memo': memo,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M")
    })

    json.dump(database, open(DATA_FILE, mode='w', encoding='utf-8'),
              indent=4, ensure_ascii=False)


def load_data():
    """
    Load the norilog data

    Returns
    -------
    database : json
    """
    try:
        database = json.load(open(DATA_FILE, mode='r', encoding='utf-8'))
    except FileNotFoundError:
        database = []
    return database


@application.route('/')
def index():
    rides = load_data()
    return render_template('index.html', rides=rides)


@application.route('/save', methods=['POST'])
def save():
    start = request.form.get('start')
    finish = request.form.get('finish')
    memo = request.form.get('memo')
    created_at = datetime.now()
    save_data(start, finish, memo, created_at)
    return redirect('/')


@application.template_filter('nl2br')
def nl2br_filter(s):
    return escape(s).replace('\n', Markup('<br>'))


def main():
    application.run('0.0.0.0', 8000, debug=True)


if __name__ == '__main__':
    application.run('0.0.0.0', 8000, debug=True)
