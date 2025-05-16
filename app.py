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
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): 
        return "<Task %r>" % self.id
    
with app.app_context():
    db.create_all()

@app.route("/", methods=["POST", "GET"])

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
        tasks = Todo.query.order_by(Todo.dateCreated).all()
        return render_template("index.html", tasks=tasks)



if __name__ == "__main__":
    app.run(debug=True)
    