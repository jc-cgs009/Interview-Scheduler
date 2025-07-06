from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno: Mapped[int] = mapped_column(primary_key = True)
    title: Mapped[str] = mapped_column(nullable=False)
    desc: Mapped[str] = mapped_column(nullable=False)
    date_created: Mapped[datetime] = mapped_column(default=datetime.now())

with app.app_context():
    db.create_all()

@app.route("/", methods = ['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()

    all_todo = Todo.query.all()
    return render_template("index.html", all_todo = all_todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    td = Todo.query.filter_by(sno = sno).first()
    db.session.delete(td)
    db.session.commit()

    return redirect('/')

@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        td = Todo.query.filter_by(sno=sno).first()
        td.title = title
        td.desc = desc
        db.session.commit()
        return redirect('/')

    td = Todo.query.filter_by(sno = sno).first()
    return render_template("update.html", td = td)

if __name__ == "__main__":
    app.run(debug=False)