from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import httplib2
from htmlCode import html_data
#from html_code import html_data # html code
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import pymongo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///course.db'
db = SQLAlchemy(app)

class Course(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   course_name = db.Column(db.String(100)) 
   course_link = db.Column(db.String(100))  
   instructor_name = db.Column(db.String(200))
   course_price = db.Column(db.String(10))
   description = db.Column(db.String(750))  

def __init__(self):
   return f"{self.course_name},{self.course_link }, {self.instructor_name},{self.course_price},{self.course_price}"
#go to python
#import db from filename - app_in ete
#db.create_all()      
#https://inloop.github.io/sqlite-viewer/      
#https://cloud.mongodb.com/v2/62486957f2284b0817cadb23#metrics/replicaSet/62486a4c829842294c78ba8d/explorer/web_scrape/ineuron/find

@app.route('/',methods=['GET'])
@cross_origin()
def home():
    return render_template('home.html')


@app.route('/review',methods=['GET','POST'])
@cross_origin()
def index():
    if request.method == "POST":
        url = request.form['content']
        res = requests.get(url)
        soup = bs(res.text, "html.parser")
        data= []
        links = soup.find_all()
        soup = bs(res.text, "html.parser")
        for i in soup.findAll():
            if i.find("div",{"class":"card-content"}) != None:
                name = i.find("div",{"class":"card-content"}).h5.text
                post = i.find("div",{"class":"card-content"}).p.text
                my_site = {"Name":name, "Post":post}
                data.append(my_site)      
        return render_template("results.html",reviews = data[0:(len(data))])
    

@app.route('/site_data',methods=['GET','POST'])
@cross_origin()   
def full_site():
    if request.method == "POST":
        etc = request.form['enter']   
        data = []
        ineuron_html = bs(html_data,"html.parser")
        x = ineuron_html.findAll("div",{'class':"Course_course-card__1_V8S Course_card__2uWBu card"})
        for i in x:
            name = i.find("h5",{'class':"Course_course-title__2rA2S"}).text             
            link = "https://courses.ineuron.ai" + i.a['href']  
            if i.find("div",{'class':"Course_course-instructor__1bsVq"}) != None:
                instructor = i.find("div",{'class':"Course_course-instructor__1bsVq"}).text             
            if i.span !=None:
                price = i.span.text    
            desc = i.find("div",{'class':"Course_course-desc__2G4h9"}).text
                         
            my_data = {"Name":name, "Link":link,"Instructor":instructor,"Price":price, "Desc":desc,}
            data.append(my_data)         
        return render_template("all_data.html",reviews = data[0:(len(data))])
            

@app.route('/sql_data',methods=['GET','POST'])
@cross_origin()   
def sql_data():
    if request.method == "POST":
        etc = request.form['sql'] 
        data = []
        ineuron_html = bs(html_data,"html.parser")
        x = ineuron_html.findAll("div",{'class':"Course_course-card__1_V8S Course_card__2uWBu card"})
        for i in x:
            name = i.find("h5",{'class':"Course_course-title__2rA2S"}).text # course name          
            link = "https://courses.ineuron.ai" + i.a['href'] # link of course            
            desc = i.find("div",{'class':"Course_course-desc__2G4h9"}).text #course description             
            if i.find("div",{'class':"Course_course-instructor__1bsVq"}) != None:
                instructor = i.find("div",{'class':"Course_course-instructor__1bsVq"}).text                
            if i.span !=None: #price
                price = i.span.text #price                
                my_data = {"Name":name, "Link":link, "Desc":desc, "Instructor":instructor,"Price":price}
            data.append(my_data)
            
        for i in data:
            sql_table = Course(course_name = i["Name"],course_link = i["Link"],description = i["Desc"],instructor_name = i["Instructor"],course_price = i["Price"],)
            db.session.add(sql_table)
            db.session.commit()
                 
        all_query = Course.query.all()           
        return render_template('sql_data.html', all_query=all_query)
       


@app.route('/mongo_data',methods=['GET','POST'])
@cross_origin()  
def mongo_data():
     if request.method == "POST":
        etc = request.form['mongo'] 
        #client = MongoClient("mongodb+srv://Flask_MDB:FlaskMonogDB@flaskmdb.ph24j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client.test    
        db = client['scrape']
        collection = db['ineuron']       

        data = []
        ineuron_html = bs(html_data,"html.parser")
        x = ineuron_html.findAll("div",{'class':"Course_course-card__1_V8S Course_card__2uWBu card"})
        for i in x:
            name = i.find("h5",{'class':"Course_course-title__2rA2S"}).text # course name          
            link = "https://courses.ineuron.ai" + i.a['href'] # link of course            
            desc = i.find("div",{'class':"Course_course-desc__2G4h9"}).text #course description             
            if i.find("div",{'class':"Course_course-instructor__1bsVq"}) != None:
                instructor = i.find("div",{'class':"Course_course-instructor__1bsVq"}).text                
            if i.span !=None: #price
                price = i.span.text #price                
            my_data = {"Name":name, "Link":link, "Desc":desc, "Instructor":instructor,"Price":price}
            collection.insert_one(my_data) 
            data.append(my_data)
        
        return render_template('mongo_data.html', mongos=data[0:])








if __name__ =='__main__':
    app.run(debug=True,port=5000)