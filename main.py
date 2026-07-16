from flask import Flask,render_template,request,redirect,url_for
from flask_httpauth import HTTPBasicAuth

import os
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db= SQLAlchemy(app)
auth = HTTPBasicAuth()
users = {"egor_ostro15":"fgfg1234"}
@auth.verify_password
def verify_password(username , password):
    if username in users and users[username]==password:
        return username

class Survey_Result(db.Model):
    __tablename__ = "survey_results"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    favourite_meal = db.Column(db.String(100))
    favourite_game = db.Column(db.String(100))
    games1 = db.Column(db.Text)
    games2 = db.Column(db.Text)
    games3 = db.Column(db.Text)
    games4 = db.Column(db.Text)
    roblox_games = db.Column(db.String(100))
    your_device = db.Column(db.String(100))
    mark = db.Column(db.String(100))
    friend = db.Column(db.String(100))




@app.route("/")
def home():
    return render_template("home.html")
@app.route("/submit",methods =["POST"])
def submit():
    username = request.form.get("username")
    if not username:
        return render_template("home.html",error="введи свой никнейм")
    return redirect(url_for("survey",username=username))



@app.route('/survey',methods=["GET","POST"])
def survey():
    username = request.args.get('username')
    if request.method =="POST":
        favourite_meal=request.form.get("favourite_meal")
        favourite_game=request.form.get("favourite_game")
        games1 = request.form.getlist("games1")
        games2 = request.form.getlist("games2")
        games3 = request.form.getlist("games3")
        games4 = request.form.getlist("games4")
        roblox_games=request.form.get("roblox_games")
        your_device=request.form.get("Your device")
        mark=request.form.get("mark")
        friend=request.form.get("friend")
        games1_str =", ". join(games1)
        games2_str = ", ".join(games2)
        games3_str = ", ".join(games3)
        games4_str =", ". join(games4)





        result= Survey_Result(username = username,
                              favourite_meal = favourite_meal,
                              favourite_game = favourite_game,
                              games1 = games1_str,
                              games2=games2_str,
                              games3=games3_str,
                              games4=games4_str,
                              roblox_games =  roblox_games,
                              your_device = your_device,
                              mark = mark,
                              friend = friend
                              ) #дз
        db.session.add(result)
        db.session.commit()



        return render_template("finish.html")
    return  render_template('survey.html',username=username)

@app.route("/results")
@auth.login_required
def resalts():
    data=Survey_Result.query.all()
    return   render_template("results.html",data=data)

if __name__=="__main__":

    app.run(debug=True)
