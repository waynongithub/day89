from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json

# based on NeuralNine Simple 'Todo List App in Flask - Beginner Project'
#  https://www.youtube.com/watch?v=W1r8fVLS-gI

# the database comes from Patrick Loeber https://www.youtube.com/watch?v=yKHJsLUENl0
# Python Flask Beginner Tutorial - Todo App - Crash Course

app = Flask(__name__)

app.app_context().push() # this line was not in tutorial, but was given in the comments.
# Is required with Flask-SQLAlchemy 3.0 and above

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100))
    done = db.Column(db.Boolean)


@app.route("/update/<int:todo_id>", methods=["GET", "POST"])
def update(todo_id):
    print(f"todo_id={todo_id}")
    todo = Todo.query.filter_by(id=todo_id).first()
    if request.method == "POST":
        todo.task = request.form['todo']
        db.session.commit()
        return redirect( url_for('home'))
    else:
        return render_template("update.html", todo=todo, todo_id=todo_id)


@app.route("/check/<int:todo_id>")
def check(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.done = not todo.done
    db.session.commit()
    return redirect( url_for('home'))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect( url_for('home'))


@app.route("/add", methods=["POST"])
def add():
    if request.method == "POST":
        new_todo = Todo(task=request.form['task'], done=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect( url_for('home'))



@app.route("/")
def home():
    todos = Todo.query.all()
    return render_template("base.html", tasks=todos)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5001)