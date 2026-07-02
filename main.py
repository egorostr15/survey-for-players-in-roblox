from flask import Flask,render_template,request,redirect,url_for
from flask_httpauth import HTTPBasicAuth

import sqlite3
app = Flask(__name__)
auth = HTTPBasicAuth()
users = {"egor_ostro15":"fgfg1234"}
@auth.verify_password
def verify_password(username , password):
    if username in users and users[username]==password:
        return username

def init_db():
    conn=sqlite3.connect("database.db")
    curser=conn.cursor()
    curser.execute('''CREATE TABLE IF NOT EXISTS survey_results
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    favourite_meal TEXT, 
    favourite_game TEXT,
    games1 TEXT,
    games2 TEXT,
    games3 TEXT,
    games4 TEXT,
    roblox_games TEXT,
    your_device TEXT,
    mark TEXT,
    friend TEXT
    )''')
    conn.commit()
    conn.close()


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




       
        conn = sqlite3.connect("database.db")
        curser = conn.cursor()
        curser.execute(''' INSERT INTO survey_results
        (username,favourite_meal ,  favourite_game , games1 , games2 ,games3 ,games4 ,roblox_games ,your_device ,mark ,friend )
        VALUES(?,?,?,?,?,?,?,?,?,?,?)
        ''', (username,favourite_meal ,  favourite_game , games1_str , games2_str ,games3_str ,games4_str ,roblox_games ,your_device,mark ,friend ))
        conn.commit()

        conn.close()

        return render_template("finish.html")
    return  render_template('survey.html',username=username)

@app.route("/results")
@auth.login_required
def resalts():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    curser =conn.cursor()
    curser.execute("SELECT * FROM survey_results")
    data= curser.fetchall()
    conn.close()
    return   render_template("results.html",data=data)
init_db()
if __name__=="__main__":

    app.run(debug=True)
