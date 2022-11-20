from flask import Flask, render_template, session, url_for, request
import pandas as pd
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#initialize the database
db = SQLAlchemy(app)
app.app_context().push()

#create db model
class Reviews(db.Model):
  #each id is unique so the db knows what we're looking for
  id = db.Column(db.Integer, primary_key = True)
  subjectName = db.Column(db.String(200), nullable = False)
  className = db.Column(db.String(200), nullable = False)
  rating = db.Column(db.Integer, nullable= False)
  dateCreated = db.Column(db.DateTime, default = datetime.utcnow)
  #create a function to return a string when we add something
  def __repr__(self):
    return '<Name %r>' % self.id
app.secret_key = "dljsaklqk24e21cjn!Ew@@dsa5"

def serveButtons(html, content,title):
    URLS = []
    currPath = request.path
    for s in content:
      string = s.replace(' ','')
      URLS.append(f"{currPath}{string}/")
    res =  render_template(html,len = len(content),title=title, URLS = URLS,content=content)
    return res

@app.route('/')
def main():
  print(request.path)
  mainDF = pd.read_csv("Reviews.csv", sep = ",")
  session["mainDF"]= mainDF.to_dict()
  res = serveButtons("mainPage.html", ["Write Reviews", "View Reviews"], "Rate My Class")
  return res

@app.route('/WriteReviews/')
def WriteReviews():
  res = render_template("writeReview.html")
  return res
@app.route('/ViewReviews/')
def ViewReviews():
  #file = session.get("mainDF", None)
  #file= pd.DataFrame.from_dict(file)
  subjectsCursor = db.session.execute('SELECT DISTINCT subjectName FROM Reviews')
  subjectsList = [s[0] for s in subjectsCursor.fetchall()]
  res = serveButtons("subjects.html", subjectsList, "Subjects")
  return res
@app.route('/WriteReviews/Submit', methods = ["GET","POST"])
def reviewSubmit():
  Class = request.form.get("class")
  subject = request.form.get("subject")
  rating = request.form.get("rate")
  new_review = Reviews(subjectName = subject, className = Class, rating = rating)
  try:
    db.session.add(new_review)
    db.session.commit()
    return render_template("submission.html")
  except:
    return render_template("submissionFailed.html")
  print(f"class:{Class}, subject:{subject}, rating:{rating}")
@app.route('/ViewReviews/<subject>/')
def ViewSubject(subject):
  #file = session.get("mainDF",None)
  #file = pd.DataFrame.from_dict(file)
  sql = text('SELECT DISTINCT className from Reviews WHERE subjectName= :subject')
  classesCursor = db.session.execute(sql,{"subject":subject})
  classesList = [c[0] for c in classesCursor.fetchall()]
  #classes = file[file.Subject ==subject]["Classes"].unique()
  return serveButtons("classes.html", classesList,"Classes")
