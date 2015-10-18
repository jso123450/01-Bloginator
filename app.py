# imports

from flask import Flask, render_template, request, session, redirect, url_for,Markup
import sqlite3, utils

#flask
app = Flask(__name__)

#link to the index; just a render_template & login
@app.route("/", methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
def home():
    if 'un' in session and session['un'] != 0:
        return render_template("home.html",un=session['un'])
    else:
        return login_register()


#link to the about page; just a render_template
@app.route("/about")
def about():
    if 'un' in session and session['un'] != 0:
        return render_template("about.html",un=session['un'])
    else:
        return render_template("about.html")

#woo cool popup!
@app.route("/login",methods=["GET","POST"])
def login_register():
    if request.method=="GET":
        if 'un' in session and session['un'] != 0:
            user = session['un']
            return redirect(url_for("home"))
        else:
            return render_template("home.html",unlogged="You are not currently logged in.")
    else:
        #button = request.form['button']
        if 'in_username' in request.form:
            user = request.form['in_username']
            passwd = request.form['in_password']
            if utils.authenticate(user,passwd):
                session['un'] = user
                session['pw'] = passwd
                return redirect(url_for("blog"))
            else:
                error = "INVALID USERNAME AND/OR PASSWORD"
                return render_template("home.html",error=error)
        else:
            user = request.form['regis_username']
            passwd = request.form['regis_password']
            conn = sqlite3.connect('bloginator.db')
            c = conn.cursor()
            c.execute('select * from users where username="'+user+'"')
            r = c.fetchall()
            conn.commit()
            if len(r) == 0:
                utils.newUser(user,passwd)
                success = "Account Created!"
                return render_template("home.html",created=success)
            else:
                failure = "There is already an account with this username"
                return render_template("home.html",created=failure)

# reset the username & pw in the session
@app.route("/logout")
def logout():
    session['un'] = 0
    session['pw'] = 0
    return redirect(url_for("home"))

"""
# register funct adds un and pw to a database with them
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("home.html")
    else:
        user = request.form['regis_username']
        passwd = request.form['regis_password']
        conn = sqlite3.connect('bloginator.db')
        c = conn.cursor()
        c.execute('select * from users where username="'+user+'"')
        r = c.fetchall()
        conn.commit()
        if len(r) == 0:
            utils.newUser(user,passwd)
            success = "Account Created!"
            return render_template("home.html",created=success)
        else:
            failure = "There is already an account with this username"
            return render_template("home.html",created=failure)
"""

# view all stories currently posted       
@app.route("/blog", methods=["GET", "POST"])
def blog():
    if request.method=="GET":
        if 'un' not in session or session['un']==0:
            return redirect(url_for("home"))
        else:
            user = session['un']
            s = ""
            stories = utils.getAllPosts()
            for p in stories:
                s += "<br>"
                s += "<div class='boxed2 type center'>"
                s += "<h1> <a href='story/%s'> %s</a> </h1>" %(p[1], p[1])
                s += "<h2> Posted by: %s </h2>" %p[0]
                s += "<h3> %s </h3>" %p[2] + "</div><br>"
            s = Markup(s)
            return render_template("blog.html",un=user,stories=s)
    else:
        ti = request.form["title"]
        con = request.form["post_content"]
        utils.Post(session['un'],ti,con)
        return redirect(url_for("blog"))

#view individual stories
@app.route("/story/<title>", methods=["GET", "POST"])
def story(title=""):
    if 'un' not in session or session['un']==0:
        return redirect(url_for("home"))
    else:
        user = session['un']
        story = utils.getPost(title)
        if len(story) == 0:
            return redirect(url_for("blog"))
            #return render_template("home.html")
        else:
            story = story[0]
            return render_template("story.html",un=user,title=story[1],user=story[0],content=story[2])

"""
#write your own story
@app.route('/write', methods=["GET","POST"])
def write():
    if request.method=="GET":
        if 'un' not in session or session['un']==0:
            return redirect(url_for("home"))
        else:
            return render_template("write.html")
    else:
        utils.Post(session['un'],request.form['title'],request.form['post_content'])
        return redirect(url_for("blog"))
"""

#running
if __name__ == "__main__":
    app.debug = True
    app.secret_key = "whatsthisfor"
    app.run(host='0.0.0.0',port=8000)
