from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import make_response

app=Flask(__name__)

@app.route("/")
def home():
    if  request.cookies.get("login")=="":
        return redirect("/member")
    else :
        return render_template("home.html")

@app.route("/signin", methods=["POST"])
def singin(): 
    account=request.form["account"]
    password=request.form["password"]
    if account=="test" and password=="test":
        resp=make_response(redirect("/member"))
        resp.set_cookie("login", "")
        return resp
    elif account=="" or password=="":
        return redirect("/error?message=請輸入帳號、密碼")
    elif account!="test" or password!="test":
        return redirect("/error?message=帳號或密碼輸入錯誤")
    

@app.route("/member")
def member():
    if  request.cookies.get("login")=="":
        return render_template("member.html")
    else:
        return redirect("/")


@app.route("/signout")
def signout():
    resp=make_response(redirect("/"))
    resp.delete_cookie("login")
    return resp

@app.route("/error")
def error():
    message=request.args.get("message", "")
    if message=="請輸入帳號、密碼":
        return render_template("error.html", text=message)
    elif message=="帳號或密碼輸入錯誤":
        return render_template("error.html", text=message)


@app.route("/square/<num>")
def squarenum(num):
    num=int(num)
    result=num**2
    return render_template("square.html", result=result)

app.run(port=3000) 