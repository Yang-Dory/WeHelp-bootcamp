from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import mysql.connector

# 建立MySQL連線
conn = mysql.connector.connect(
    host='localhost',           # 連線主機名稱
    database='website',         # 資料庫名稱
    user='root',                # 登入帳號
    password='5244',  # 登入密碼
)
cursor = conn.cursor()

app=Flask(__name__)
app.secret_key="key"

@app.route("/")
def home():
    if  "id" in session:
        return redirect("/member")
    else :
        return render_template("home.html")

@app.route("/signup", methods=["POST"])
def signup():
    name=request.form["name"]
    account=request.form["account"]
    password=request.form["password"]
    cursor.execute('SELECT username FROM member WHERE username=%s;', [account])
    username=cursor.fetchall()
    if []!=username:
        return redirect("/error?message=帳號已被註冊") 
    sql="INSERT INTO member(name, username, password) VALUES(%s, %s, %s);"
    new_data=(name, account, password)
    cursor.execute(sql, new_data)
    conn.commit()
    return redirect("/")

    

@app.route("/signin", methods=["POST"])
def singin():
    account=request.form["account"]
    password=request.form["password"]
    sql='SELECT id, name, username, password FROM member WHERE username=%s and password=%s;'
    data=(account, password)
    cursor.execute(sql, data)
    result=cursor.fetchall()
    if []!=result:
        session["id"]=result[0][0]
        session["name"]=result[0][1]
        return redirect("/member")
    elif account=="" or password=="":
        return redirect("/error?message=請輸入帳號、密碼")
    else:
        return redirect("/error?message=帳號或密碼輸入錯誤")
    

@app.route("/member")
def member():
    if  "id" in session:
        name=session['name']
        cursor.execute('SELECT member.name, message.content FROM member INNER JOIN message ON member.id=message.member_id;')
        result=cursor.fetchall()
        return render_template("member.html", name=name, result=result)
    else:
        return redirect("/")

@app.route("/signout")
def signout():
    session.clear()
    return redirect("/")

@app.route("/error")
def error():
    message=request.args.get("message", "")
    return render_template("error.html", text=message)

@app.route("/message", methods=["POST"])
def message():
    message=request.form["message"]
    member_id=session["id"]
    sql='INSERT INTO message(member_id, content) VALUES(%s, %s);'
    data=(member_id, message)
    cursor.execute(sql, data)
    conn.commit()
    return redirect("/member")

app.run(port=3000) 