from flask import Flask, render_template, session, url_for, request, redirect
import pandas as pd
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
app = Flask(__name__)
#NEED TO FIND WAY TO HIDE THIS BEFORE DEPLOYMENT
app.config['SECRET_KEY'] = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.app_context().push()

'''GOALS:
  -Handle faulty user inputs
  -make codebase more modular
  -possibly add login stuff
''' 
#TODO: User Db is created, now need to make a form to actually handle creation of users :D
#TODO: Also need to begin using Flask Forms, can find more on flask fridays

#create db model
class Reviews(db.Model):
  #each id is unique so the db knows what we're looking for
  id = db.Column(db.Integer, primary_key = True)
  subjectName = db.Column(db.String(200), nullable = False)
  className = db.Column(db.String(200), nullable = False)
  rating = db.Column(db.Integer, nullable= False)
  textReview = db.Column(db.Text())
  dateCreated = db.Column(db.DateTime, default = datetime.utcnow)
  #create a function to return a string when we add something
  def __repr__(self):
    return '<Name %r>' % self.id

class ReviewForm(FlaskForm):
  className = StringField("Class Name:", validators = [DataRequired()])
  SubjectName = StringField("Subject Name:", validators = [DataRequired()])
  rate = RadioField('Rating', choices =[(5,"star5"),(4,"star4"), (3,"star3"), (2, "star2"), (1, "star1")])
  reviewText = TextAreaField("Review:", validators = [DataRequired()])
  submit = SubmitField("Submit")

class Users(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(200), nullable = False)
  email = db.Column(db.String(120), nullable= True)
  date_added = db.Column(db.DateTime, default = datetime.utcnow)
  password_hash = db.Column(db.String(128))
  #what to return when try to read password
  @property
  def password(self):
    raise AttributeError('password is not a readable attribute!')
  
  #hashes pass
  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)
  #verifies pass by checking its hash
  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
app.secret_key = "dljsaklqk24e21cjn!Ew@@dsa5"

def serveButtons(html, content,title):
    URLS = []
    currPath = request.path
    for s in content:
      string = s.replace(' ','')
      URLS.append(f"{currPath}{string}/")
    res =  render_template(html,len = len(content),title=title, URLS = URLS,content=content)
    return res

def serveReviews(html, subject, Class, title):
  sql = text(
    "SELECT rating, textReview " 
    "FROM Reviews "
    "WHERE subjectName= :subject " 
    "AND className = :class ")
  reviewsCursor = db.session.execute(sql,{"subject":subject, "class": Class})
  reviewListMapping=reviewsCursor.mappings().all()
  res = render_template(html, reviewListMapping = reviewListMapping, len =len(reviewListMapping), title = title)
  return res

@app.route('/')
def main():
  print(request.path)
  res = serveButtons("mainPage.html", ["Write Reviews", "View Reviews"], "Rate My Class")
  return res

@app.route('/WriteReviews/', methods = ['GET', 'POST'])
def WriteReviews():
  Class = None
  subject = None
  rating = None
  reviewText = None
  form = ReviewForm()
  if form.validate_on_submit():
    Class = form.className.data
    form.className.data =''
    subject = form.SubjectName.data
    form.SubjectName.data =''
    rating = form.rate.data
    form.rate.data =0
    reviewText = form.reviewText.data
    form.reviewText.data = ''
    return redirect(url_for('reviewSubmit', Class = Class, subject = subject,rating= rating, reviewText = reviewText))
  res = render_template("writeReview.html", Class = Class,subject = subject,rating = rating, form = form)
  return res
@app.route('/ViewReviews/')
def ViewReviews():
  subjectsCursor = db.session.execute('SELECT DISTINCT subjectName FROM Reviews')
  subjectsList = [s[0] for s in subjectsCursor.fetchall()]
  res = serveButtons("subjects.html", subjectsList, "Subjects")
  return res
@app.route('/WriteReviews/Submit', methods = ["GET","POST"])
def reviewSubmit():
  subject = request.args['subject']
  Class = request.args['Class']
  rating = request.args['rating']
  reviewText= request.args['reviewText']
  new_review = Reviews(subjectName = subject, className = Class, rating = rating, textReview = reviewText)
  try:
    db.session.add(new_review)
    db.session.commit()
    return render_template("submission.html")
  except:
    return render_template("submissionFailed.html")
@app.route('/ViewReviews/<subject>/')
def ViewSubject(subject):
  sql = text('SELECT DISTINCT className from Reviews WHERE subjectName= :subject')
  classesCursor = db.session.execute(sql,{"subject":subject})
  classesList = [c[0] for c in classesCursor.fetchall()]
  return serveButtons("classes.html", classesList,"Classes")

@app.route('/ViewReviews/<subject>/<Class>/')
def ViewClass(subject,Class):
  print(subject)
  res = serveReviews("reviews.html",subject, Class, f"{Class} Reviews")
  return res