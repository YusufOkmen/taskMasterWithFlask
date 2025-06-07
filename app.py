from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow().date)

    def __repr__(self): 
        return "<Task %r>" % self.id
    
with app.app_context():
    db.create_all()

@app.route("/", methods=["POST", "GET"])

# Task Master main page
def index():
    if request.method == "POST":
        # Name of the content
        taskContent = request.form["content"]
        # Creating a todo object
        newTask = Todo(content=taskContent)

        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding your task"
        
    else:
        tasks = Todo.query.filter_by(completed=0).order_by(Todo.dateCreated).all()
        return render_template("index.html", tasks=tasks)

# Delete tasks
@app.route("/delete/<int:id>")
def delete(id):
    taskToDelete = Todo.query.get_or_404(id)

    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect("/")
    except: 
        return "There was a problem deleting that task!"

# Update tasks
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    taskToUpdate = Todo.query.get_or_404(id)

    if request.method == "POST":
        taskToUpdate.content = request.form["content"]
        
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task!"
    else:
        return render_template("update.html", task=taskToUpdate)

# Turn checkboxes on and off
@app.route("/complete/<int:id>", methods=["POST"])
def complete(id):
    completedTask = Todo.query.get_or_404(id)
    if completedTask.completed == 1:
        completedTask.completed = 0
    else:
        completedTask.completed = 1

    try:
        db.session.commit()
        return redirect("/")
    except:
        return "There was an issue updating the task status"
    
# Show the completed tasks
@app.route("/completedTasks")
def completed_tasks():
    tasks = Todo.query.filter_by(completed=1).order_by(Todo.dateCreated).all()
    return render_template("completedTasks.html", tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)
    