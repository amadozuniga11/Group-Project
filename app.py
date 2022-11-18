
from flask import Flask, render_template

app = Flask(__name__)

#@app.route("/")
#def home_page():
import pandas as pd
class fileInfo:
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

class fileTest:
  def __init__(self, filename):
    self.file = pd.read_csv(filename, sep = ",")
  def displaySubjects(self,title, type):
    res =  render_template("Subjects.html",title=title, subjects=self.file[type].unique())
    return res
@app.route('/')
def render():
  test = fileTest("Reviews.csv")
  res = test.displaySubjects("Subjects", "Subject")
  return res


#@app.route('/user/<name>')
#def greet(name):
    #return f'<p>Hello, {name}!</p>'

#if __name__ == '__main__':
    #app.run(debug=True)
