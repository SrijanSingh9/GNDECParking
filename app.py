from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as DateTime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///details.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Details(db.Model):
    Sno=db.Column(db.Integer, primary_key=True)
    Vehicle_No=db.Column(db.String(20), nullable=False)
    Name=db.Column(db.String(30), nullable=False)
    date_created=db.Column(db.DateTime,default=DateTime.utcnow, nullable=False)

    def __repr__(self) -> str: 
        return f"{self.Vehicle_No} - {self.Name}"


@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        Vehicle_No=request.form['Vehicle_No']
        Name=request.form['Name']
        details=Details(Vehicle_No=Vehicle_No,Name=Name)
        db.session.add(details)
        db.session.commit()
    allDetails=Details.query.all()
    return render_template('index.html',allDetails=allDetails)

@app.route('/delete/<int:Sno>')
def delete(Sno):
    details=Details.query.filter_by(Sno=Sno).first()
    db.session.delete(details)
    db.session.commit()
    return redirect('/') 

if __name__ == '__main__':
    app.run(debug=True)