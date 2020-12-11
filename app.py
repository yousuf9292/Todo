from flask import Flask,render_template,redirect,url_for,request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,IntegerField,BooleanField,SubmitField
from wtforms.validators import InputRequired,Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import exc


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY']='HA'

db = SQLAlchemy(app)




class List(db.Model):
	ids = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(10),nullable=False)
	description = db.Column(db.Text(),nullable=False)
	datetime = db.Column(db.DateTime,default=datetime.now) 

class ToDo(FlaskForm):
	ids = IntegerField('Id',validators=[InputRequired(message='Data Required')])
	title = StringField('Title',validators=[InputRequired('Data Required'),Length(max=20,message="Not Greater Than 20")])
	description = StringField('Description',validators=[InputRequired(message="Data Required")])
	done = BooleanField('Done',validators=[InputRequired()])
	submit = SubmitField('Submit')




@app.route('/',methods=['GET','POST'])
def form():
	form=ToDo()
	lists=List(ids=form.ids.data,title=form.title.data,description=form.description.data)
	if form.validate_on_submit():
		try:
			db.session.add(lists)
			db.session.commit()
			return redirect(url_for('table'))
		except exc.IntegrityError as e:
			db.session().rollback()
		return redirect(url_for('form'))
	return render_template('todo.html',form=form)


@app.route('/table',methods=['GET','POST'])
def table():
	lists=List.query.all()
	form=ToDo()
	return render_template('table.html',lists=lists,form=form)




@app.route('/update/<int:ids>',methods=['POST','GET'])
def update(ids):
	task=List.query.get_or_404(ids)
	form=ToDo()
	if request.method=='POST':
		task.title=request.form['title']
		task.description=request.form['description']
		
		try:
			db.session.commit()
			return redirect('/table')
		except:
			return '<h1>do it properly </h1>'
	else:
		return render_template('update.html',task=task,form=form)


@app.route('/delete/<int:ids>')
def delete(ids):
	task_to_delete = List.query.get_or_404(ids)
	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect('/table')
	except:
		return '<h1>Task not foud</h1>'




if __name__ == '__main__':
	app.run(debug=True)