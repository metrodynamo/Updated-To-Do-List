# imports
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


# db.Model is inheritance (comes from SQLAlchemy). It doesn't need any self or def init properties as this is written into the db.Model code

app = Flask(__name__) #Creates an instance of the Flask class and assigns it to the app variable. The __name__ argument helps Flask determine the root path for the application, which is useful for finding resources and templates.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app) #This line initialises an instance of the SQLAlchemy class and associates it with the Flask app. It is assigned to the variable DB. The db variable now represents the database connection and is used for database operations.

class MyTask(db.Model): #Class that takes the instance of SQLAlchemy(app) variable
   id = db.Column(db.Integer, primary_key=True)
   content = db.Column(db.String(100), nullable=False)
   complete = db.Column(db.Integer,default=0)
   created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

#Home page
@app.route("/", methods=["POST", "GET"]) #This is a decorator that Flask provides to bind a function to a URL. In this case, it binds the index function to the root URL ("/") of the web application. When a user visits the root URL, this function will be called.
def index():
  if request.method =="POST":
     current_task = request.form['content'] #Whatever the user has provided via the name="content" part of the form in the index.html page. Assign that to variable 'current_task'
     new_task = MyTask(content=current_task) #Assign 'current_task' information 'content', which is used by index.html. new-task is a new object of MyTask class.
     try:
        db.session.add(new_task) #Connect to DB
        db.session.commit() #Send task through
        return redirect("/")
     except Exception as e:
        print(f"ERROR:{e}")
        return f"ERROR:{e}"
     #See all current tasks
  else:
     tasks = MyTask.query.order_by(MyTask.created).all()
     return render_template('index.html', tasks = tasks) #First variable of tasks is used by index.html. Assigned to it are all the tasks that were created on line above this one. So tasks(html) = tasks(Python)

@app.route("/delete/<int:id>")
def delete(id:int): #Delete by ID which is an integer
   delete_task = MyTask.query.get_or_404(id) #Will either delete or give 404 error. Delete by ID.
   try:
      db.session.delete(delete_task)
      db.session.commit()
      return redirect("/")
   except Exception as e:
        return f"ERROR:{e}"
   
@app.route("/edit/<int:id>", methods =["GET", "POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
      task.content = request.form['content'] 
      try:
         db.session.commit()
         return redirect("/")
      except Exception as e:
        return f"ERROR:{e}"
    else:
      return render_template('edit.html', task=task)

if __name__ == "__main__": #This code block ensures that the Flask application runs only if the script is executed directly (not imported as a module).
    app.run(debug=True) #Starts in debug mode.