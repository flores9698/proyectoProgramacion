from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class students(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))
   addr = db.Column(db.String(200)) 
   pin = db.Column(db.String(10))

   def __repr__(self):
   	return '<Task %r>' % self.id


   def __init__(self, name, city, addr,pin):
   	self.name= name
   	self.city=city
   	self.addr=addr
   	self.pin=pin
   	




@app.route('/')
def show_all():
   return render_template('show_all.html', students = students.query.all() )

@app.route('/nueva', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student = students(request.form['name'], request.form['city'],
            request.form['addr'], request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         flash('Agregado Correctamente')
         return redirect(url_for('show_all'))
   return render_template('new.html')


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = students.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'



app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        student = students(request.form['name'], request.form['city'],
            request.form['addr'], request.form['pin'])

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)