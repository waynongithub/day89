from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# based on NeuralNine Simple Todo List App in Flask - Beginner Project
#  https://www.youtube.com/watch?v=W1r8fVLS-gI

# the database comes from Patrick Loeber https://www.youtube.com/watch?v=yKHJsLUENl0
# Python Flask Beginner Tutorial - Todo App - Crash Course

def load_tasks():
    # Problems:
    # 1. tasks = json.loads()  instead of tasks = json.loads(text)
    # 2. the tasklist had values False not in quotes
    # 3. maybe? there was a comma after the last property of a task
    with open("static/tasks.txt") as f:
        text = f.read()
        # print(text)
        tasklist = json.loads(text)
        print(f"tasks[0]={tasklist[0]}")
        print(f"tasks[0]task={tasklist[0]['task']}")
        print(f"tasks[0]done={tasklist[0]['done']}")

    return tasklist


tasks = [{"task": "sample todo", "done": False}]


@app.route("/edit/<index>", methods=["GET", "POST"])
def edit(index):
    print(f"index={index}, {tasks}")
    task = tasks[int(index)]
    print(f"task={task}")
    if request.method == "POST":
        print(f"request.form['task']={request.form['task']}")
        print(f"request.form.get('task')={request.form.get('task')}")
        task['task'] = request.form['task']
        return redirect( url_for('home'))
    else:
        return render_template("edit.html", task=task, index=index)


@app.route("/check/<int:index>")
def check(index):
    tasks[index]['done'] = not tasks[index]['done']
    return redirect( url_for('home'))


@app.route("/delete/<int:index>")
def delete(index):
    del tasks[index]
    return redirect( url_for('home'))


@app.route("/add", methods=["POST"])
def add():
    if request.method == "POST":
        tasks.append({
            "task": request.form['task'],
            "done": False
        })
        return redirect( url_for('home'))


@app.route("/")
def home():
    return render_template("index.html", tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True, port=5001)