from flask import (
    Blueprint, render_template, redirect, url_for, request, g, current_app
)

from myapp.db import get_db


bp = Blueprint('todo', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    con = get_db()
    cur = con.cursor()
    
    tasks = cur.execute(
        "SELECT * FROM task"
    ).fetchall()

    return render_template('todo/index.html', tasks=tasks)


@bp.route('/create', methods=['POST'])
def create():
    con = get_db()
    cur = con.cursor()
    taskname = request.form['taskname']

    cur.execute(
        "INSERT INTO task (taskname) VALUES (?)",
        (taskname,)
    )
    con.commit()

    return redirect(url_for('todo.index'))


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    con = get_db()
    cur = con.cursor()
    task = cur.execute(
        'SELECT * FROM task WHERE id = ?',
        (id,)
    ).fetchone()

    if request.method == 'POST':
        taskname = request.form['taskname']
        status = request.form['status']
        cur.execute(
            "UPDATE task SET taskname = ?, status = ? WHERE id = ?",
            (taskname, status, id)
        )
        con.commit()
        return redirect(url_for('todo.index'))

    return render_template('todo/update.html', task=task)


@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    con = get_db()
    cur = con.cursor()
    task = cur.execute(
        'DELETE FROM task WHERE id = ?',
        (id,)
    )
    con.commit()
    
    return redirect(url_for('todo.index'))