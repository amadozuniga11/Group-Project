
from flask import Flask, render_template, session, url_for, request
import pandas as pd
import json
app = Flask(__name__)
app.secret_key = "dljsaklqk24e21cjn!Ew@@dsa5"
#@app.route("/")
#def home_page():
class fileIn:
  def __init__(self, filename):
    self.file = pd.read_csv(filename, sep = ",")
  def information(self):
    print(list(self.file.columns.values))
    Math = self.file[self.file.Subject =="Math"]
    print(Math.Classes.unique())
    print(self.file.info())
  def display(self,Subject,SubjectName):
    DF = self.file.loc(self.file[Subject] == SubjectName)
    print(DF)
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

class fileInfo:
  def __init__(self, filename):
    self.file = pd.read_csv(filename, sep = ",")
  def displayColumns(self,title, type):
    res =  render_template("subjects.html",title=title, Subjects=self.file[type].unique())
    return res

def serveButtons(html, content,title):
    URLS = []
    print("-------------------------------------------------------------------------------")
    print(request.path)
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
  return render_template("mainPage.html", writeReviewsURL= url_for('writeReviews'), viewReviewsURL = url_for('viewReviews'))

@app.route('/WriteReviews/')
def WriteReviews():
  file = session.get("mainDF", None)
  file= pd.DataFrame.from_dict(file)
  res = serveButtons("subjects.html", file["Subject"].unique(), "Subjects")
  return res

@app.route('/ViewReviews/')
def ViewReviews():
  file = session.get("mainDF", None)
  file= pd.DataFrame.from_dict(file)
  res = serveButtons("subjects.html", file["Subject"].unique(), "Subjects")
  return res

@app.route('/ViewReviews/<subject>/')
def ViewSubject(subject):
  file = session.get("mainDF",None)
  file = pd.DataFrame.from_dict(file)
  classes = file[file.Subject ==subject]["Classes"].unique()
  return serveButtons("classes.html", classes,"Classes")


#@app.route('/user/<name>')
#def greet(name):
    #return f'<p>Hello, {name}!</p>'

#if __name__ == '__main__':
    #app.run(debug=True)
