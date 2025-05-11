import bottle
import datetime
import os
import io
import csv
import sqlite3
import bcrypt
import sys

if len(sys.argv) == 2:
    if sys.argv[1] == "init":
        os.remove("database.db")
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE Books(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, author TEXT NOT NULL, publisher TEXT NOT NULL, date TEXT NOT NULL)")
        cur.execute("CREATE TABLE Users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, number TEXT NOT NULL, email TEXT NOT NULL, hashedpw BLOB NOT NULL, salt BLOB NOT NULL)")
        cur.execute("CREATE TABLE Lend(id INTEGER PRIMARY KEY AUTOINCREMENT, bookid INTEGER NOT NULL, userid INTEGER NOT NULL, lend TEXT NOT NULL, return TEXT)")
        cur.execute("CREATE TABLE Reserve(id INTEGER PRIMARY KEY AUTOINCREMENT, bookid INTEGER NOT NULL, userid INTEGER NOT NULL, ready TEXT, UNIQUE(bookid, userid))")
        cur.execute("CREATE TABLE Reviews(id INTEGER PRIMARY KEY AUTOINCREMENT, bookid INTEGER NOT NULL, review TEXT NOT NULL)")
        password = "12345678"
        salt = bcrypt.gensalt(rounds = 10, prefix = b"2a")
        hashedpw = bcrypt.hashpw(password.encode("utf-8"), salt)    
        cur.execute("INSERT INTO Users(name, number, email, hashedpw, salt) values(?, ?, ?, ?, ?)",("admin", "000", "admin@example.com", hashedpw, salt))
        conn.commit()
        conn.close()
        sys.exit()
    else:
        sys.exit()

SECRETKEY = "secretkey"

class Users:
    users = []
    def __init__(self, id, name, expiration, index):
        self.id = id
        self.name = name
        self.expiration = expiration
        self.index = len(Users.users)
        Users.users.append(self)

def changetospace(content):
    listcontent = list(content)
    for i, element in enumerate(listcontent):
        if element == "+":
            if listcontent[i + 1] == "s":
                listcontent[i] = " "
                listcontent[i + 1] = ""
            elif listcontent[i + 1] == "+":
                listcontent[i + 1] = ""
    return "".join(listcontent)

bottle.BaseTemplate.settings.update({'filters':{'space': changetospace}})

def changetoplus(data):
    tempdata = []
    for element in data:
        listelement = list(element)
        for i, char in enumerate(listelement):
            if char == " ":
                listelement[i] = "+s"
            elif char == "+":
                listelement[i] = "++"
        tempdata.append(listelement)
    changeddata = []
    for element in tempdata:
        element = "".join(element)
        changeddata.append(element)
    return changeddata

def getparams():
    name = bottle.request.params.name
    author = bottle.request.params.author
    publisher = bottle.request.params.publisher
    date = bottle.request.params.date
    return [name, author, publisher, date]

def checklogin(prev):
    id = bottle.request.get_cookie("id", secret = SECRETKEY)
    if id is None:
        bottle.redirect(f"/login?prev={prev}&reason=timeout")
    elif id == 1:
        bottle.redirect(f"/login?prev={prev}&reason=authority")
    i = 0
    for user in Users.users:
        if user.id == id:
            break
        i += 1
    if i == len(Users.users):
        bottle.redirect(f"/login?prev={prev}&reason=invalid")
    if Users.users[i].expiration < datetime.datetime.now():
        bottle.redirect(f"/login?prev={prev}&reason=timeout")
    bottle.response.set_cookie("id", id, secret = SECRETKEY, max_age = 300)
    Users.users[i].expiration = datetime.datetime.now() + datetime.timedelta(minutes = 5)

def checkadmin(prev):
    id = bottle.request.get_cookie("id", secret = SECRETKEY)
    if id is None:
        bottle.redirect(f"/login?prev={prev}&reason=timeout")
    elif id != 1:
        bottle.redirect(f"/login?prev={prev}&reason=authority")
    i = 0
    for user in Users.users:
        if user.id == id:
            break
        i += 1
    if i == len(Users.users):
        bottle.redirect(f"/login?prev={prev}&reason=invalid")
    if Users.users[i].expiration < datetime.datetime.now():
        bottle.redirect(f"/login?prev={prev}&reason=timeout")
    bottle.response.set_cookie("id", id, secret = SECRETKEY, max_age = 300)
    Users.users[i].expiration = datetime.datetime.now() + datetime.timedelta(minutes = 5)


def getindex(id):
    i = 0
    for user in Users.users:
        if user.id == id:
            break
        i += 1
    return i

def getidname():
    id = bottle.request.get_cookie("id", secret = SECRETKEY)
    i = getindex(id)
    return {"uid": Users.users[i].id, "uname": Users.users[i].name}

@bottle.route("/index")
@bottle.view("index")
def root():
    checklogin("index")
    today = datetime.date.today()
    due = today + datetime.timedelta(days = 30)
    returndata = {"today": today, "due": due}
    returndata.update(getidname())
    return returndata

@bottle.route("/")
def viewhome():
    bottle.redirect("/index")

@bottle.route("/static/style.css")
def sendcss():
    return bottle.static_file("style.css", root = "./static")

@bottle.route("/login")
def loginview():
    prev = bottle.request.params.prev
    reason = bottle.request.params.reason
    if reason == "":
        error = ["", ""]
    elif reason == "timeout":
        error = ["ログインしてください", "このシステムの利用にはログインが必要です。なお、ログイン中に表示された場合は、タイムアウトしています。再度ログインしてください。"]
    elif reason == "authority":
        error = ["権限エラー", "現在ログインしているアカウントでは、この操作は実行できません。適切なアカウントで、再度ログインしてください。"]
        prev = ""
    elif reason == "logout":
        error = ["ログアウト", "ログアウトしました。再度利用するには、ログインしてください。"]
    elif reason == "double":
        error = ["ログインエラー", "二重ログインはできません。このアカウントは、既にログイン状態になっています。"]
    elif reason == "invalid":
        error = ["不正ログイン", "不正なログインです。"]
    elif reason == "notfound":
        error = ["ログインエラー", "アカウントが見つかりません。ユーザ名が正しいことを確認してください。"]
    elif reason == "wrongpw":
        error = ["ログインエラー", "パスワードが正しくありません。"]
    return bottle.template("login", prev = prev, error = error)

@bottle.post("/dologin")
def dologin():
    username = bottle.request.params.name
    password = bottle.request.params.password
    prev = bottle.request.params.prev
    i = 0
    for user in Users.users:
        if user.name == username:
            if user.expiration < datetime.datetime.now():
                del Users.users[i]
                break
            else:
                bottle.redirect("/login?reason=double")
        i += 1
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT id, hashedpw, salt FROM Users WHERE name = ?", (username,))
    userdata = cur.fetchall()
    conn.close()
    if userdata == []:
        bottle.redirect("/login?reason=notfound")
    userdata = userdata[0]
    if userdata[1] == bcrypt.hashpw(password.encode("utf-8"), userdata[2]):
        Users(userdata[0], username, datetime.datetime.now() + datetime.timedelta(minutes = 5), "")
        bottle.response.set_cookie("id", userdata[0], secret = SECRETKEY, max_age = 300)
        if prev != "":
            bottle.redirect("/" + prev)
        elif userdata[0] == 1:
            bottle.redirect("/admin")
        else:
            bottle.redirect("/")
    else:
        bottle.redirect("/login?reason=wrongpw")

@bottle.route("/logout")
def logout():
    id = bottle.request.get_cookie("id", secret = SECRETKEY)
    if id is None:
            bottle.redirect("/login?reason=timeout")
    index = getindex(id)
    del Users.users[index]
    bottle.response.delete_cookie("id")
    bottle.redirect("/login?reason=logout")

@bottle.route("/admin")
@bottle.view("admin")
def admin():
    checkadmin("admin")
    return getidname()

@bottle.route("/register")
@bottle.jinja2_view("register")
def register():
    checkadmin("register")
    returndata = {"data": ["", "", "", ""], "errormsg": ""}
    returndata.update(getidname())
    return returndata

@bottle.post("/register")
def registering():
    checkadmin("register")
    data = getparams()
    modify = bottle.request.params.modify
    errormsg = ""
    if data[0] == "":
        errormsg += "書名、"
    if data[1] == "":
        errormsg += "著者名、"
    if data[2] == "":
        errormsg += "出版社名、"
    try:
        buydate = datetime.date.fromisoformat(data[3])
        if datetime.date.today() < buydate:
            errormsg += "購入日、"
    except:
        errormsg += "購入日、"
    changeddata = changetoplus(data)
    idname = getidname()
    if errormsg != "":
        errormsg = errormsg[:-1] + "に問題があります。"
        return bottle.jinja2_template("register", data = changeddata, uid = idname["uid"], uname = idname["uname"], errormsg = errormsg)
    elif modify == "True":
        return bottle.jinja2_template("register", data = changeddata, uid = idname["uid"], uname = idname["uname"], errormsg = "")
    else:
        return bottle.jinja2_template("registering", data = changeddata, uid = idname["uid"], uname = idname["uname"])

@bottle.post("/registered")
@bottle.view("registered")
def registered():
    checkadmin("register")
    data = getparams()
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Books(name, author, publisher, date) values(?, ?, ?, ?)",
    (data[0], data[1], data[2], data[3]))
    conn.commit()
    conn.close()
    returndata = {"data": data}
    returndata.update(getidname())
    return returndata

@bottle.post("/csv")
@bottle.view("upload")
def csvup():
    checkadmin("upload")
    return getidname()

@bottle.post("/upload")
def upload():
    checkadmin("upload")
    filedata = bottle.request.files.file
    rawdata = filedata.file.read().decode("utf_8_sig")
    data = io.StringIO(rawdata)
    csvdata = []
    for row in csv.reader(data):
        csvdata.append(row)
    totalerror = 0
    errorlist = []
    for row in csvdata:
        error = 0
        for i in range(3):
            if row[i] == "":
                error += 1
        try:
            buydate = datetime.date.fromisoformat(row[3])
            if datetime.date.today() < buydate:
                error += 1
        except:
            error += 1
        totalerror += error
        if error > 0:
            errorlist.append(row)
    idname = getidname()
    if totalerror == 0:
        return bottle.template("uploading", data = csvdata, rawdata = rawdata, uid = idname["uid"], uname = idname["uname"])
    else:
        return bottle.template("csverror", totalerror = totalerror, errorlist = errorlist, uid = idname["uid"], uname = idname["uname"])

@bottle.post("/uploaded")
@bottle.view("uploaded")
def uploaded():
    checkadmin("upload")
    cancel = bottle.request.params.cancel
    if cancel == "True":
        bottle.redirect("/register")
    data = bottle.request.params.data
    data = io.StringIO(data)
    csvdata = []
    for row in csv.reader(data):
        csvdata.append(row)
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    for row in csvdata:
        cur.execute("INSERT INTO Books(name, author, publisher, date) values(?, ?, ?, ?)",
        (row[0], row[1], row[2], row[3]))
    conn.commit()
    conn.close()
    returndata = {"data": csvdata}
    returndata.update(getidname())
    return returndata

@bottle.route("/all")
@bottle.view("all")
def all():
    checkadmin("all")
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Books")
    allbooks = cur.fetchall()
    conn.close()
    returndata = {"allbooks": allbooks}
    returndata.update(getidname())
    return returndata

@bottle.route("/manage")
@bottle.view("manage")
def manage():
    checkadmin("manage")
    return getidname()

@bottle.route("/manageall")
def manageall():
    checkadmin("manageall")
    id = bottle.request.params.id
    type = bottle.request.params.type
    if id == "" and type == "":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Books")
        allbooks = cur.fetchall()
        conn.close()
        idname = getidname()
        return bottle.template("manageall", allbooks = allbooks, uid = idname["uid"], uname = idname["uname"])
    elif type == "delete":
        bottle.redirect(f"bookdelete?id={id}&fm=a")
    elif type == "modify":
        bottle.redirect(f"bookmodify?id={id}&fm=a")

@bottle.route("/managesearch")
def managesearch():
    checkadmin("managesearch")
    id = bottle.request.params.id
    type = bottle.request.params.type
    if id == "" and type == "":
        idname = getidname()
        return bottle.jinja2_template("managesearch", data = ["", "", "", ""], uid = idname["uid"], uname = idname["uname"])
    elif type == "delete":
        bottle.redirect(f"bookdelete?id={id}&fm=s")
    elif type == "modify":
        bottle.redirect(f"bookmodify?id={id}&fm=s")

@bottle.post("/managesearch")
def managesearched():
    checkadmin("managesearch")
    data = getparams()
    changeddata = changetoplus(data)
    change = bottle.request.params.change
    idname = getidname()
    if change == "change":
        return bottle.jinja2_template("managesearch", data = changeddata, uid = idname["uid"], uname = idname["uname"])
    else:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Books \
        WHERE name = CASE WHEN :name = '' THEN name ELSE :name END AND \
        author = CASE WHEN :author = '' THEN author ELSE :author END AND \
        publisher = CASE WHEN :publisher = '' THEN publisher ELSE :publisher END AND \
        date = CASE WHEN :date = '' THEN date ELSE :date END",
        {"name": data[0], "author": data[1], "publisher": data[2], "date": data[3]})
        searcheddata = cur.fetchall()
        conn.close()
        return bottle.jinja2_template("managesearched", searcheddata = searcheddata, data = changeddata, number = len(searcheddata), uid = idname["uid"], uname = idname["uname"])

@bottle.route("/bookdelete")
def bookdelete():
    checkadmin("manage")
    id = bottle.request.params.id
    fm = bottle.request.params.fm
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Books WHERE id = ?", (id,))
    data = cur.fetchall()
    conn.close()
    data = data[0]
    dicdata = {"id": data[0], "name": data[1], "author": data[2], "publisher": data[3], "date": data[4]}
    idname = getidname()
    return bottle.template("delconfirm", data = dicdata, uid = idname["uid"], uname = idname["uname"], fm = fm, id = id)

@bottle.post("/bookdelete")
def deletecancel():
    fm = bottle.request.params.fm
    if fm == "a":
        bottle.redirect("/manageall")
    elif fm == "s":
        bottle.redirect("/managesearch")

@bottle.post("/bookdeleted")
@bottle.view("bookdeleted")
def bookdeleted():
    checkadmin("manage")
    id = bottle.request.params.id
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM Books WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return getidname()

@bottle.route("/bookmodify")
def bookmodify():
    checkadmin("manage")
    id = bottle.request.params.id
    fm = bottle.request.params.fm
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Books WHERE id = ?", (id,))
    data = cur.fetchall()
    conn.close()
    data = data[0]
    data = data[1:]
    changeddata = changetoplus(data)
    idname = getidname()
    return bottle.jinja2_template("bookmodify",data = changeddata, fm = fm, id = id, errormsg = "", uid = idname["uid"], uname = idname["uname"])

@bottle.post("/bookmodify")
def bookmodifying():
    checkadmin("manage")
    data = getparams()
    modify = bottle.request.params.modify
    id = bottle.request.params.id
    fm = bottle.request.params.fm
    cancel = bottle.request.params.cancel
    if cancel == "True":
        if fm == "a":
            bottle.redirect("/manageall")
        elif fm == "s":
            bottle.redirect("/managesearch")
    errormsg = ""
    if data[0] == "":
        errormsg += "書名、"
    if data[1] == "":
        errormsg += "著者名、"
    if data[2] == "":
        errormsg += "出版社名、"
    try:
        buydate = datetime.date.fromisoformat(data[3])
        if datetime.date.today() < buydate:
            errormsg += "購入日、"
    except:
        errormsg += "購入日、"
    changeddata = changetoplus(data)
    idname = getidname()
    if errormsg != "":
        errormsg = errormsg[:-1] + "に問題があります。"
        return bottle.jinja2_template("bookmodify", data = changeddata, errormsg = errormsg, fm = fm, id = id, uid = idname["uid"], uname = idname["uname"])
    elif modify == "True":
        return bottle.jinja2_template("bookmodify", data = changeddata, errormsg = "", fm = fm, id = id, uid = idname["uid"], uname = idname["uname"])
    else:
        return bottle.jinja2_template("bookmodifying", data = changeddata, fm = fm, id = id, uid = idname["uid"], uname = idname["uname"])

@bottle.post("/bookmodified")
@bottle.view("bookmodified")
def bookmodified():
    checkadmin("manage")
    data = getparams()
    id = bottle.request.params.id
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE Books SET name = ?, author = ?, publisher = ?, date = ? WHERE id = ?",
    (data[0], data[1], data[2], data[3], id))
    conn.commit()
    conn.close()
    returndata = {"data": data}
    returndata.update(getidname())
    return returndata

@bottle.route("/user")
@bottle.view("usermanage")
def user():
    id = bottle.request.params.id
    if id == "":
        checkadmin("user")
        return getidname()
    elif id == "1":
        checkadmin("user")
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT name, number, email FROM Users WHERE id = ?", (id, ))
        udata = cur.fetchall()[0]
        conn.close()
        idname = getidname()
        return bottle.template("admindata", udata = udata, uid = idname["uid"], uname = idname["uname"], id = id)
    else:
        checklogin(f"user?id={id}")
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT name, number, email FROM Users WHERE id = ?",(id, ))
        udata = cur.fetchall()[0]
        cur.execute("SELECT name, author, publisher, date, lend, return FROM Lend JOIN Books ON bookid = Books.id WHERE userid = ?", (id, ))
        bookdata = cur.fetchall()
        conn.close()
        idname = getidname()
        return bottle.template("userdata", udata = udata, bookdata = bookdata, uid = idname["uid"], uname = idname["uname"], id = id)

@bottle.route("/createuser")
@bottle.view("createuser")
def createuserview():
    checkadmin("createuser")
    returndata = {"data": ["", "", "", "", ""], "errormsg": ""}
    returndata.update(getidname())
    return returndata

@bottle.post("/createuser")
def creatinguser():
    checkadmin("createuser")
    data = [""] * 5
    data[0] = bottle.request.params.name
    data[1] = bottle.request.params.number
    data[2] = bottle.request.params.email
    data[3] = bottle.request.params.password
    data[4] = bottle.request.params.password2
    modify = bottle.request.params.modify
    errormsg = ""
    if data[0] == "" or not data[0].isascii() or " " in data[0]:
        errormsg += "ユーザ名、"
    if data[1] == "" or not data[1].isascii() or " " in data[1]:
        errormsg += "学籍番号、"
    if data[2] == "" or not data[2].isascii() or " " in data[2]:
        errormsg += "メールアドレス、"
    if data[3] == "" or not data[3].isascii() or " " in data[3] or len(data[3]) < 8 or data[3] != data[4]:
        errormsg += "パスワード、"
    if data[4] == "" or not data[4].isascii() or " " in data[4] or len(data[4]) < 8:
        errormsg += "確認用パスワード、"
    if errormsg != "":
        errormsg = errormsg[:-1] + "に問題があります。"
    idname = getidname()
    if errormsg != "":
        return bottle.template("createuser", data = data, errormsg = errormsg, uid = idname["uid"], uname = idname["uname"])
    elif modify == "True":
        return bottle.template("createuser", data = data, errormsg = "", uid = idname["uid"], uname = idname["uname"])
    elif errormsg =="":
        data.append("*" * len(data[3]))
        return bottle.template("creatinguser", data = data, uid = idname["uid"], uname = idname["uname"])

@bottle.post("/createduser")
@bottle.view("createduser")
def createduser():
    checkadmin("createuser")
    data = [""] * 4
    data[0] = bottle.request.params.name
    data[1] = bottle.request.params.number
    data[2] = bottle.request.params.email
    data[3] = bottle.request.params.password
    salt = bcrypt.gensalt(rounds = 10, prefix = b"2a")
    hashedpw = bcrypt.hashpw(data[3].encode("utf-8"), salt)
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Users(name, number, email, hashedpw, salt) values(?, ?, ?, ?, ?)",
    (data[0], data[1], data[2], hashedpw, salt))
    conn.commit()
    conn.close()
    data[3] = "*" * len(data[3])
    returndata = {"data": data}
    returndata.update(getidname())
    return returndata

@bottle.route("/allusers")
@bottle.view("allusers")
def allusers():
    checkadmin("allusers")
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, number, email FROM Users")
    allusers = cur.fetchall()
    conn.close()
    returndata = {"allusers": allusers}
    returndata.update(getidname())
    return returndata

@bottle.route("/manageusers")
@bottle.view("manageusers")
def manageusers():
    checkadmin("manageusers")
    id = bottle.request.params.id
    type = bottle.request.params.type
    if id == "" and type == "":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT id, name, number, email FROM Users")
        allusers = cur.fetchall()
        conn.close()
        returndata = {"allusers": allusers}
        returndata.update(getidname())
        return returndata
    elif type == "delete":
        bottle.redirect(f"userdelete?id={id}")
    elif type == "modify":
        bottle.redirect(f"usermodify?id={id}")

@bottle.route("/userdelete")
def userdelete():
    checkadmin("manageusers")
    id = bottle.request.params.id
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, number, email FROM Users WHERE id = ?", (id,))
    data = cur.fetchall()
    conn.close()
    data = data[0]
    dicdata = {"id": data[0], "name": data[1], "number": data[2], "email": data[3]}
    idname = getidname()
    return bottle.template("userdelconfirm", data = dicdata, id = id, uid = idname["uid"], uname = idname["uname"])

@bottle.post("/userdelete")
def userdeletecancel():
    bottle.redirect("/manageusers")

@bottle.post("/userdeleted")
@bottle.view("userdeleted")
def userdeleted():
    checkadmin("manageusers")
    id = bottle.request.params.id
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM Users WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return getidname()

@bottle.route("/usermodify")
def usermodify():
    checkadmin("manageusers")
    id = bottle.request.params.id
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT name, number, email FROM Users WHERE id = ?", (id,))
    data = cur.fetchall()
    conn.close()
    data = data[0]
    idname = getidname()
    return bottle.template("usermodify",data = data, id = id, errormsg = "", uid = idname["uid"], uname = idname["uname"])

@bottle.post("/usermodify")
def usermodifying():
    checkadmin("manageusers")
    data = [""] * 3
    data[0] = bottle.request.params.name
    data[1] = bottle.request.params.number
    data[2] = bottle.request.params.email
    modify = bottle.request.params.modify
    id = bottle.request.params.id
    cancel = bottle.request.params.cancel
    if cancel == "True":
        bottle.redirect("/manageusers")
    errormsg = ""
    if data[0] == "" or not data[0].isascii() or " " in data[0]:
        errormsg += "ユーザ名、"
    if data[1] == "" or not data[1].isascii() or " " in data[1]:
        errormsg += "学籍番号、"
    if data[2] == "" or not data[2].isascii() or " " in data[2]:
        errormsg += "メールアドレス、"
    idname = getidname()
    if errormsg != "":
        errormsg = errormsg[:-1] + "に問題があります。"
        return bottle.template("usermodify", data = data, errormsg = errormsg, id = id, uid = idname["uid"], uname = idname["uname"])
    elif modify == "True":
        return bottle.template("usermodify", data = data, errormsg = "", id = id, uid = idname["uid"], uname = idname["uname"])
    else:
        return bottle.template("usermodifying", data = data, id = id, uid = idname["uid"], uname = idname["uname"])

@bottle.post("/usermodified")
@bottle.view("usermodified")
def usermodified():
    checkadmin("manageusers")
    name = bottle.request.params.name
    number = bottle.request.params.number
    email = bottle.request.params.email
    id = bottle.request.params.id
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE Users SET name = ?, number = ?, email = ?WHERE id = ?",
    (name, number, email, id))
    conn.commit()
    conn.close()
    returndata = {"name": name, "number": number, "email": email}
    returndata.update(getidname())
    return returndata

@bottle.route("/uall")
@bottle.view("uall")
def uall():
    checklogin("uall")
    id = bottle.request.params.id
    type = bottle.request.params.type
    if id == "" and type == "":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT id, name, author, publisher, date FROM Books")
        allbookstuple = cur.fetchall()
        cur.execute("SELECT bookid FROM Lend WHERE return IS NULL")
        lendingbookstuple = cur.fetchall()
        cur.execute("SELECT DISTINCT bookid FROM Reserve")
        reservedbookstuple = cur.fetchall()
        conn.close()
        lendingbooks = []
        reservedbooks = []
        for id in lendingbookstuple:
            lendingbooks.append(id[0])
        for id in reservedbookstuple:
            reservedbooks.append(id[0])
        allbooks = []
        for bookstuple in allbookstuple:
            books = list(bookstuple)
            if books[0] in lendingbooks and books[0] in reservedbooks:
                books.append("貸出中・予約有")
            elif books[0] in lendingbooks:
                books.append("貸出中")
            elif books[0] in reservedbooks:
                books.append("予約有")
            else:
                books.append("貸出可能")
            allbooks.append(books)
        returndata = {"allbooks": allbooks, "lend": lendingbooks}
        returndata.update(getidname())
        return returndata
    elif type == "lend":
        bottle.redirect(f"lend?id={id}&fm=a")
    elif type == "reserve":
        bottle.redirect(f"reserve?id={id}&fm=a")
    elif type == "review":
        bottle.redirect(f"review?id={id}&fm=a")

@bottle.route("/usearch")
def usearch():
    checklogin("usearch")
    id = bottle.request.params.id
    type = bottle.request.params.type
    if id == "" and type == "":
        idname = getidname()
        return bottle.jinja2_template("usearch", data = ["", "", "", ""], uid = idname["uid"], uname = idname["uname"])
    elif type == "lend":
        bottle.redirect(f"lend?id={id}&fm=s")
    elif type == "reserve":
        bottle.redirect(f"reserve?id={id}&fm=s")
    elif type == "review":
        bottle.redirect(f"review?id={id}&fm=s")

@bottle.post("/usearch")
def usearched():
    checklogin("usearch")
    data = getparams()
    changeddata = changetoplus(data)
    change = bottle.request.params.change
    idname = getidname()
    if change == "change":
        return bottle.jinja2_template("usearch", data = changeddata, uid = idname["uid"], uname = idname["uname"])
    else:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Books \
        WHERE name = CASE WHEN :name = '' THEN name ELSE :name END AND \
        author = CASE WHEN :author = '' THEN author ELSE :author END AND \
        publisher = CASE WHEN :publisher = '' THEN publisher ELSE :publisher END AND \
        date = CASE WHEN :date = '' THEN date ELSE :date END",
        {"name": data[0], "author": data[1], "publisher": data[2], "date": data[3]})
        searcheddata = cur.fetchall()
        searchedid = []
        for data in searcheddata:
            searchedid.append(data[0])
        lendingbooks = []
        reservedbooks = []
        for id in searchedid:
            cur.execute("SELECT EXISTS(SELECT * FROM Lend WHERE return IS NULL AND bookid = ?)", (id,))
            if cur.fetchall()[0][0] == 1:
                lendingbooks.append(id)
        for id in searchedid:
            cur.execute("SELECT EXISTS(SELECT * FROM Reserve WHERE bookid = ?)", (id,))
            if cur.fetchall()[0][0] == 1:
                reservedbooks.append(id)
        allbooks = []
        for bookstuple in searcheddata:
            books = list(bookstuple)
            if books[0] in lendingbooks and books[0] in reservedbooks:
                books.append("貸出中・予約有")
            elif books[0] in lendingbooks:
                books.append("貸出中")
            elif books[0] in reservedbooks:
                books.append("予約有")
            else:
                books.append("貸出可能")
            allbooks.append(books)
        conn.close()
        return bottle.jinja2_template("usearched", data = changeddata, allbooks = allbooks, number = len(searcheddata), uid = idname["uid"], uname = idname["uname"])

@bottle.route("/lend")
def lend():
    checklogin("uall")
    id = bottle.request.params.id
    fm = bottle.request.params.fm
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Books WHERE id = ?", (id,))
    data = cur.fetchall()
    conn.close()
    data = data[0]
    dicdata = {"id": data[0], "name": data[1], "author": data[2], "publisher": data[3], "date": data[4]}
    dicdata["today"] = datetime.date.today()
    dicdata["due"] = datetime.date.today() + datetime.timedelta(days = 30)
    idname = getidname()
    return bottle.template("lendconfirm", data = dicdata, uid = idname["uid"], uname = idname["uname"], fm = fm, id = id)

@bottle.post("/lend")
def lendcancel():
    fm = bottle.request.params.fm
    if fm == "a":
        bottle.redirect("/uall")
    elif fm == "s":
        bottle.redirect("/usearch")
    elif fm == "r":
        bottle.redirect("/cancel")

@bottle.post("/lended")
@bottle.view("lended")
def lended():
    checklogin("uall")
    idname = getidname()
    id = bottle.request.params.id
    fm = bottle.request.params.fm
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Books WHERE id = ?", (id,))
    data = cur.fetchall()
    cur.execute("INSERT INTO Lend(bookid, userid, lend) values(?, ?, ?)", (id, idname["uid"], datetime.date.today()))
    conn.commit()
    if fm == "r":
        cur.execute("DELETE FROM Reserve WHERE bookid = ? AND userid = ?", (id, idname["uid"]))
        conn.commit()
    conn.close()
    data = data[0]
    dicdata = {"id": data[0], "name": data[1], "author": data[2], "publisher": data[3], "date": data[4]}
    dicdata["today"] = datetime.date.today()
    dicdata["due"] = datetime.date.today() + datetime.timedelta(days = 30)
    dicdata["fm"] = fm
    dicdata.update(idname)
    return dicdata

@bottle.route("/reserve")
def reserve():
    checklogin("uall")
    id = bottle.request.params.id
    fm = bottle.request.params.fm
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Books WHERE id = ?", (id,))
    data = cur.fetchall()
    conn.close()
    data = data[0]
    dicdata = {"id": data[0], "name": data[1], "author": data[2], "publisher": data[3], "date": data[4]}
    idname = getidname()
    return bottle.template("reserveconfirm", data = dicdata, uid = idname["uid"], uname = idname["uname"], fm = fm, id = id)

@bottle.post("/reserve")
def reservecancel():
    fm = bottle.request.params.fm
    if fm == "a":
        bottle.redirect("/uall")
    elif fm == "s":
        bottle.redirect("/usearch")

@bottle.post("/reserved")
@bottle.view("reserved")
def reserved():
    checklogin("uall")
    idname = getidname()
    id = bottle.request.params.id
    fm = bottle.request.params.fm
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Books WHERE id = ?", (id,))
    data = cur.fetchall()
    try:
        cur.execute("INSERT INTO Reserve(bookid, userid) values(?, ?)", (id, idname["uid"]))
    except:
        conn.close()
        return bottle.template("reservefailure", uid = idname["uid"], uname = idname["uname"], fm = fm)
    conn.commit()
    conn.close()
    data = data[0]
    dicdata = {"id": data[0], "name": data[1], "author": data[2], "publisher": data[3], "date": data[4]}
    dicdata["fm"] = fm
    dicdata.update(idname)
    return dicdata


@bottle.route("/return")
@bottle.view("return")
def bookreturn():
    checklogin("return")
    id = bottle.request.params.id
    idname = getidname()
    if id == "":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT Books.id, name, author, publisher, date, lend FROM Lend JOIN Books ON bookid = Books.id WHERE return IS NULL AND userid = ?", (idname["uid"],))
        lendingbookstuple = cur.fetchall()
        conn.close()
        lendingbooks = []
        for book in lendingbookstuple:
            book = list(book)
            book[5] = datetime.date.fromisoformat(book[5]) + datetime.timedelta(days = 30)
            lendingbooks.append(book)
        returndata = {"allbooks": lendingbooks}
        returndata.update(idname)
        return returndata
    else:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Books WHERE id = ?", (id,))
        data = cur.fetchall()[0]
        conn.close()
        return bottle.template("returnconfirm", data = data, uid = idname["uid"], uname = idname["uname"], id = id)

@bottle.post("/return")
def returncancel():
    bottle.redirect("/return")

@bottle.post("/returned")
@bottle.view("returned")
def bookreturned():
    checklogin("return")
    id = bottle.request.params.id
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Books WHERE id = ?", (id,))
    data = cur.fetchall()
    cur.execute("UPDATE Lend SET return = ? WHERE bookid = ? AND return IS NULL", (datetime.date.today(), id))
    conn.commit()
    cur.execute("SELECT id FROM Reserve WHERE bookid = ? LIMIT 1", (id,))
    readyid = cur.fetchall()
    if readyid != []:
        cur.execute("UPDATE Reserve SET ready = ? WHERE id = ?", (datetime.date.today(), readyid[0][0]))
        conn.commit()
    conn.close()
    data = data[0]
    dicdata = {"id": data[0], "name": data[1], "author": data[2], "publisher": data[3], "date": data[4]}
    dicdata.update(getidname())
    return dicdata

@bottle.route("/cancel")
def reservemanage():
    checklogin("cancel")
    id = bottle.request.params.id
    type = bottle.request.params.type
    idname = getidname()
    if id == "" and type == "":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT Books.id, name, author, publisher, date, ready FROM Reserve JOIN Books ON bookid = Books.id WHERE userid = ?", (idname["uid"],))
        reservedata = cur.fetchall()
        conn.close()
        readybooks = []
        notreadybooks = []
        for book in reservedata:
            if book[5] is None:
                notreadybooks.append(book)
            else:
                readybooks.append(book)
        return bottle.template("reservemanage", readybooks = readybooks, notreadybooks = notreadybooks, uid = idname["uid"], uname = idname["uname"])
    elif type == "lend":
        bottle.redirect(f"/lend?id={id}&fm=r")
    elif type == "cancel":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Books WHERE id = ?", (id,))
        data = cur.fetchall()[0]
        conn.close()
        return bottle.template("cancelconfirm", data = data, uid = idname["uid"], uname = idname["uname"], id = id)

@bottle.post("/cancel")
def cancelcancel():
    bottle.redirect("/cancel")

@bottle.post("/canceled")
@bottle.view("canceled")
def canceled():
    checklogin("cancel")
    id = bottle.request.params.id
    idname = getidname()
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM Reserve WHERE bookid = ? AND userid = ?",(id, idname["uid"]))
    conn.commit()
    conn.close()
    return idname

@bottle.route("/addreview")
@bottle.view("addreview")
def addreview():
    checklogin("return")
    id = bottle.request.params.id
    returndata = {"id": id, "review": ""}
    returndata.update(getidname())
    return returndata

@bottle.post("/addreview")
def addcancel():
    checklogin("return")
    if bottle.request.params.modify == "True":
        id = bottle.request.params.id
        review = bottle.request.params.review
        idname = getidname()
        return bottle.template("addreview", review = review, id = id, uid = idname["uid"], uname = idname["uname"])
    else:
        bottle.redirect("/return")

@bottle.post("/addingreview")
@bottle.view("addingreview")
def addingreview():
    checklogin("return")
    id = bottle.request.params.id
    review = bottle.request.params.review
    returndata = {"id": id, "review": review}
    returndata.update(getidname())
    return returndata

@bottle.post("/addedreview")
@bottle.view("addedreview")
def addedreview():
    checklogin("return")
    id = bottle.request.params.id
    review = bottle.request.params.review
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Reviews(bookid, review) values(?, ?)",(id, review))
    conn.commit()
    conn.close()
    return getidname()

@bottle.route("/review")
@bottle.view("review")
def review():
    checklogin("uall")
    id = bottle.request.params.id
    fm = bottle.request.params.fm
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT review FROM Reviews WHERE bookid = ?",(id,))
    reviews = cur.fetchall()
    conn.close()
    number = len(reviews)
    returndata = {"reviews": reviews, "number": number, "fm": fm}
    returndata.update(getidname())
    return returndata

@bottle.route("/uchange")
@bottle.view("uchange")
def uchange():
    id = bottle.request.params.id
    if id == "1":
        checkadmin("user")
    else:
        checklogin("index")
    data = [""] * 5    
    returndata = {"id": id, "data": data, "errormsg": "", "item": ""}
    returndata.update(getidname())
    return returndata

@bottle.post("/uchange")
def uchanging():
    checklogin("")
    id = bottle.request.params.id
    if bottle.request.params.cancel == "True":
        bottle.redirect(f"/user?id={id}")
    data = [""] * 5
    item = bottle.request.forms.getall("item")
    modify = bottle.request.params.modify
    errormsg = ""
    if "name" in item:
        data[0] = bottle.request.params.name
        if data[0] == "" or not data[0].isascii() or " " in data[0]:
            errormsg += "ユーザ名、"
    if "email" in item:
        data[1] = bottle.request.params.email
        if data[1] == "" or not data[1].isascii() or " " in data[1]:
            errormsg += "メールアドレス、"
    if "password" in item:
        data[2] = bottle.request.params.currentpassword
        data[3] = bottle.request.params.newpassword
        data[4] = bottle.request.params.newpassword2
        if data[2] == "" or not data[2].isascii() or " " in data[2] or len(data[2]) < 8:
            errormsg += "現在のパスワード、"
        if data[3] == "" or not data[3].isascii() or " " in data[3] or len(data[3]) < 8 or data[3] != data[4]:
            errormsg += "新しいパスワード、"
        if data[4] == "" or not data[4].isascii() or " " in data[4] or len(data[4]) < 8:
            errormsg += "新しいパスワード(確認用)、"    
    idname = getidname()
    if errormsg != "":
        errormsg = errormsg[:-1] + "に問題があります。"
        return bottle.template("uchange", data = data, errormsg = errormsg, id = id, uid = idname["uid"], uname = idname["uname"], item = item)
    elif modify == "True":
        return bottle.template("uchange", data = data, errormsg = "", id = id, uid = idname["uid"], uname = idname["uname"], item = item)
    else:
        if "password" in item:
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            cur.execute("SELECT hashedpw, salt FROM Users WHERE id = ?", (idname["uid"],))
            userdata = cur.fetchall()[0]
            conn.close()
            if userdata[0] == bcrypt.hashpw(data[2].encode("utf-8"), userdata[1]):
                data.append("*" * len(data[3]))
                return bottle.template("uchanging", data = data, id = id, uid = idname["uid"], uname = idname["uname"], item = item)
            else:
                return bottle.template("uchange", data = data, errormsg = "現在のパスワードが間違っています。", id = id, uid = idname["uid"], uname = idname["uname"], item = item)        
        else:
            data.append("*" * len(data[3]))
            return bottle.template("uchanging", data = data, id = id, uid = idname["uid"], uname = idname["uname"], item = item)

@bottle.post("/uchanged")
@bottle.view("uchanged")
def uchanged():
    checklogin("")
    id = bottle.request.params.id
    item = bottle.request.forms.getall("item")
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    if "name" in item:
        name = bottle.request.params.name
        cur.execute("UPDATE Users SET name = ? WHERE id = ?",(name, id))
        conn.commit()
    if "email" in item:
        email = bottle.request.params.email
        cur.execute("UPDATE Users SET email = ? WHERE id = ?",(email, id))
        conn.commit()
    if "password" in item:
        password = bottle.request.params.newpassword
        salt = bcrypt.gensalt(rounds = 10, prefix = b"2a")
        hashedpw = bcrypt.hashpw(password.encode("utf-8"), salt)
        cur.execute("UPDATE Users SET hashedpw = ?, salt = ? WHERE id = ?",(hashedpw, salt, id))
        conn.commit()
    conn.close()
    return getidname()

@bottle.route("/pwchange")
@bottle.view("pwchange")
def pwchange():
    checkadmin("pwchange")
    returndata = {"errormsg": "", "data": ["", "", ""]}
    returndata.update(getidname())
    return returndata

@bottle.post("/pwchange")
def pwchanging():
    checkadmin("pwchange")
    if bottle.request.params.cancel == "True":
        bottle.redirect("/user?id=1")
    data = [""] * 3
    data[0] = bottle.request.params.currentpassword
    data[1] = bottle.request.params.newpassword
    data[2] = bottle.request.params.newpassword2
    modify = bottle.request.params.modify
    errormsg = ""
    if data[0] == "" or not data[0].isascii() or " " in data[0] or len(data[0]) < 8:
        errormsg += "現在のパスワード、"
    if data[1] == "" or not data[1].isascii() or " " in data[1] or len(data[1]) < 8 or data[1] != data[2]:
        errormsg += "新しいパスワード、"
    if data[2] == "" or not data[2].isascii() or " " in data[2] or len(data[2]) < 8:
        errormsg += "新しいパスワード(確認用)、"
    idname = getidname()
    if errormsg != "":
        errormsg = errormsg[:-1] + "に問題があります。"
        return bottle.template("pwchange", data = data, errormsg = errormsg, id = id, uid = idname["uid"], uname = idname["uname"])
    elif modify == "True":
        return bottle.template("pwchange", data = data, errormsg = "", id = id, uid = idname["uid"], uname = idname["uname"])
    else:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT hashedpw, salt FROM Users WHERE id = ?", (idname["uid"],))
        userdata = cur.fetchall()[0]
        conn.close()
        if userdata[0] == bcrypt.hashpw(data[0].encode("utf-8"), userdata[1]):
            data.append("*" * len(data[1]))
            return bottle.template("pwchanging", data = data, uid = idname["uid"], uname = idname["uname"])
        else:
            return bottle.template("pwchange", data = data, errormsg = "現在のパスワードが間違っています。", uid = idname["uid"], uname = idname["uname"])        
    
@bottle.post("/pwchanged")
@bottle.view("pwchanged")
def pwchanged():
    checkadmin("pwchange")
    password = bottle.request.params.newpassword
    salt = bcrypt.gensalt(rounds = 10, prefix = b"2a")
    hashedpw = bcrypt.hashpw(password.encode("utf-8"), salt)
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE Users SET hashedpw = ?, salt = ? WHERE id = ?",(hashedpw, salt, 1))
    conn.commit()
    conn.close()
    return getidname()

bottle.run(host = "0.0.0.0")