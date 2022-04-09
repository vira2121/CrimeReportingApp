import flask
from flask import Flask, render_template,request,session
from flask_session import Session

import sqlite3
from werkzeug.utils import redirect

app1 = Flask(__name__)
app1.config["SESSION_PERMANENT"] = False
app1.config["SESSION_TYPE"] = "filesystem"
Session(app1)

con = sqlite3.connect("crimereportapp.db",check_same_thread=False)

listOfTables1 = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='CRIMES' ").fetchall()

if listOfTables1!=[]:
    print("Table 1 Exists ! ")

else:
    con.execute(''' CREATE TABLE CRIMES(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DESCRIPTION TEXT,
    REMARKS TEXT,
    DATE_OF_CRIME TEXT,
    REPORTER TEXT); ''')
    print("Table has created")

listOfTables2 = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='USERDATA' ").fetchall()

if listOfTables2!=[]:
    print("Table 2 Exists ! ")

else:
    con.execute(''' CREATE TABLE USERDATA(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    UNAME TEXT,
    UMOBNO TEXT,
    UEMAIL TEXT,
    UADDRESS TEXT,
    UPASSWORD TEXT); ''')
    print("Table has created")

cur7 = con.cursor()
cur7.execute("SELECT * FROM USERDATA")
res7 = cur7.fetchall()
print(res7)

cur8 = con.cursor()
cur8.execute("SELECT * FROM CRIMES")
res8 = cur8.fetchall()
print(res8)


@app1.route("/")
def start():
    return render_template("home.html")


@app1.route("/guest", methods=["GET", "POST"])
def guest():
    if request.method == "POST":
        getGDesc = request.form["gdesc"]
        getGRem = request.form["gremark"]
        getGDate = request.form["gdate"]
        print(getGDesc)
        print(getGRem)
        print(getGDate)
        con.execute("INSERT INTO CRIMES(DESCRIPTION,REMARKS,DATE_OF_CRIME) VALUES('" + getGDesc + "','" + getGRem + "','" + getGDate + "') ")
        con.commit()
        cur4 = con.cursor()
        cur4.execute("SELECT * FROM CRIMES WHERE DESCRIPTION = '" +getGDesc+ "' ")
        res4 = cur4.fetchall()
        return render_template("guestview.html", crimes4=res4)

    return render_template("guest.html")


@app1.route("/adminlogin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        getUname = request.form["username"]
        getppass = request.form["password"]

        if getUname == "admin":
            if getppass == "12345":
                return redirect("/viewall")
    return render_template("login.html")


@app1.route("/crimeentry", methods=["GET", "POST"])
def crime_entry():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        if request.method == "POST":
            getDesc = request.form["desc"]
            getRem = request.form["remark"]
            getDate = request.form["date"]
            print(getDesc)
            print(getRem)
            print(getDate)
            con.execute("INSERT INTO CRIMES(DESCRIPTION,REMARKS,DATE_OF_CRIME,REPORTER) VALUES('" + getDesc + "','" + getRem + "','" + getDate + "','"+session.get("name")+"') ")
            con.commit()
            print("successfully inserted !")

            cur5 = con.cursor()
            cur5.execute("SELECT * FROM CRIMES WHERE REPORTER = '" +session.get("name")+ "' ")
            res5 = cur5.fetchall()
            return render_template("userview2.html", crimes5=res5)

        return render_template("crimeentry.html")


@app1.route("/filter", methods=["GET", "POST"])
def filter_search():
    if request.method == "POST":
        getCRIDate = request.form["crimdate"]
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM CRIMES WHERE DATE_OF_CRIME = '"+getCRIDate+"' ")
        res2 = cur2.fetchall()
        return render_template("userview.html", crimes3=res2)
    return render_template("filter.html")


@app1.route("/editprofile", methods=["GET","POST"])
def edit_profile():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        if request.method == "POST":
            getoldemail = request.form["oldem"]
            getoldpass = request.form["oldpass"]
            getNewname = request.form["newnam"]
            getNewmob = request.form["newmob"]
            getNewem = request.form["newem"]
            getNewadd = request.form["newadd"]
            getNewpass = request.form["newpass"]
            con.execute(
                "UPDATE USERDATA SET UNAME = '" + getNewname + "',UMOBNO = '" + getNewmob + "',UEMAIL ='" + getNewem + "',UADDRESS = '" + getNewadd + "',UPASSWORD = '" + getNewpass + "' WHERE UEMAIL = '" + getoldemail + "' AND UPASSWORD = '" + getoldpass + "' ")
            print("successfully Updated profile !")
            con.commit()

            return redirect("/userlogin")
        return render_template("editprofile.html")


@app1.route("/viewall")
def view_all():
    cur = con.cursor()
    cur.execute("SELECT * FROM CRIMES")
    res = cur.fetchall()
    return render_template("viewall.html", crimes2=res)


@app1.route("/userreg", methods=["GET", "POST"])
def user_reg():
    if request.method == "POST":
        getUName = request.form["usname"]
        getUmobno = request.form["mobileno"]
        getEmail = request.form["email"]
        getAdd = request.form["address"]
        getPass = request.form["pass"]
        con.execute("INSERT INTO USERDATA(UNAME,UMOBNO,UEMAIL,UADDRESS,UPASSWORD) VALUES('" + getUName + "','" + getUmobno + "','" + getEmail + "','" + getAdd + "','" + getPass + "')")
        print("successfully inserted !")
        con.commit()
        return redirect("/userlogin")
    return render_template("regis.html")


@app1.route("/userlogin", methods=["GET", "POST"])
def user_login():
    global getName
    if request.method == "POST":
        getuseremail = request.form["Uname"]
        getuserpass = request.form["Upass"]
        print(getuseremail)
        print(getuserpass)
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM USERDATA WHERE UEMAIL = '"+getuseremail+"' AND UPASSWORD = '"+getuserpass+"'")
        res2 = cur2.fetchall()
        if len(res2) > 0:
            for i in res2:
                getName = i[1]
            session["name"] = getName

            return redirect("/crimeentry")
    return render_template("userlogin.html")


@app1.route("/userlogout", methods=["GET", "POST"])
def us_logout():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        session["name"] = None
        return redirect("/")


if __name__ == "__main__":
    app1.run()