
from flask import Flask, render_template, session, url_for, request
import pandas as pd
import json
app = Flask(__name__)
app.secret_key = "dljsaklqk24e21cjn!Ew@@dsa5"
def stats(self):
  print(self.file.columns.values)
  print(f"Max Price: {max(self.file['Price'])}")
  print(f"Lowest User Rating: {min(self.file['User Rating'])}")
  print(f"Years of data: {max(self.file['Year'])-min(self.file['Year'])}")
  print(f"Average Price: {self.file['Price'].mean()}")
  print(f"Unique Authors: {len(self.file['Author'].unique())}")
def yearlyBest(self, year):
#     Define a function yearlyBest() that will take in the dataset and a year, and will display the Top 5 Best Sellers by the highest number of reviews.
# Next, try to find the top 5 authors by number of books they have on this list.
# Next, try to find the top 5 authors by total number of reviews for all of their books on the list
# Lastly, try to find the top 5 authors by highest average review score for their books on the list
  self.file.sort_values(by = "Reviews")
  print(f"Top 5 Best Sellers:\n{self.file.head(5)['Name']}")
  print(f"Top 5 Best Sellers:\n{self.file['Author']}")
  return render_template("base.html")

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
  file = session.get("mainDF", None)
  file= pd.DataFrame.from_dict(file)
  res = serveButtons("subjects.html", file["Subject"].unique(), "Subjects")
  return res
@app.route('/ViewReviews/Submit', methods = ["POST"])
def reviewSubmit():
  Class = request.form.get("class")
  subject = request.form.get("subject")
  rating = request.form.get("rate")
  print(f"class:{Class}, subject:{subject}, rating:{rating}")
  return render_template("submission.html")
@app.route('/ViewReviews/<subject>/')
def ViewSubject(subject):
  file = session.get("mainDF",None)
  file = pd.DataFrame.from_dict(file)
  classes = file[file.Subject ==subject]["Classes"].unique()
  return serveButtons("classes.html", classes,"Classes")
