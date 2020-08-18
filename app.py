from flask import Flask, render_template, url_for, request, redirect  #importing the flask, render_template and url_for
from flask_sqlalchemy import SQLAlchemy #importing sql alchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #reletive path
db = SQLAlchemy(app) #initializing the database 

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True) #this is a id in a todo list database and also it is an primary key
    content = db.Column(db.String(200), nullable = False) #this is a text and it is set to not null , 200 represnts the size
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] #reading the input
        new_task = Todo(content = task_content)

        #pushing the input to the database 
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return "There was an issue adding your task"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html')

#new route to delete the task 
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) #get the task by id 

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'there was problem deleting the task'


if __name__ == "__main__":
    app.run(debug = True)



#getting the error -  Instance of 'SQLAlchemy' has no 'Column' memberpylint(no-member)
# at https://www.youtube.com/watch?v=Z1RJmh_OqeA&t=1050s at 30:00