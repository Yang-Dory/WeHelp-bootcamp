from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import jsonify
import mysql.connector


conn = mysql.connector.connect(
    host='localhost',           
    database='website',         
    user='root',            
    password='5244', 
)
cursor = conn.cursor()

app=Flask(__name__)
app.secret_key="key"
app.config['JSON_AS_ASCII'] = False


@app.route("/api/member", methods=['GET', 'PATCH'])
def member_api():
    if request.method == 'GET':
        username=request.args.get("username","")
        cursor.execute('SELECT id, name, username FROM member WHERE username=%s ;', [username])
        result=cursor.fetchall()
        try:
            name=session['name']
            data={
                "data":{
                        "id":result[0][0],
                        "name":result[0][1],
                        "username":result[0][2],
                }
            }
        except:
            data={
                "data":None
            }
        return jsonify(data)
    else:
        try:
            sql='UPDATE member SET name=%s WHERE username=%s;'
            data=request.json
            updatedata=(data['name'], session["username"])
            cursor.execute(sql,updatedata)
            conn.commit()
            result={
                "ok":True
            }
        except:
            result={
                "error":True
            }
        return jsonify(result)
         


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
        session["username"]=result[0][2]
        return redirect("/member")
    elif account=="" or password=="":
        return redirect("/error?message=請輸入帳號、密碼")
    else:
        return redirect("/error?message=帳號或密碼輸入錯誤")
    

@app.route("/member")
def member():
    if  "id" in session:
        name=session['name']
        username=session["username"]
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