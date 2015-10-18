#Utilities File

import sqlite3
import md5


#hash password
def encrypt(password):
    m = md5.new()
    m.update(password)
    return m.hexdigest()

#check if user and pass match
def authenticate(username, password):
    username = username.lower()
    conn = sqlite3.connect("bloginator.db")
    c = conn.cursor()
    l = c.execute('select * from users where username = "'+username+'" and password = "'+encrypt(password)+'";') 
    for i in l:
        return True;
    return False;

#create new account
def newUser(username,password):
    username = username.lower()
    conn = sqlite3.connect("myDataBase.db")
    c = conn.cursor()
    l = c.execute('select * from users where username = "%s";' % username)
    for i in l:
        return False
    ans = c.execute('insert into users values("'+username+'","'+encrypt(password)+'");')
    conn.commit()
    return True

def loginauth(un,pw):
    if un=="HERES" and pw=="JOHNNY":
        return True;
    else:
        return False;

#database functions

#gets all posts from database
def getAllPosts():
    conn = sqlite3.connect('bloginator.db')
    c = conn.cursor()
    c.execute('select * from post;')
    return c.fetchall()

#adds posts to database
def Post(username,title,content):
    conn = sqlite3.connect('bloginator.db')
    c = conn.cursor()
    r = c.execute('select * from post where title = "'+title+'"')
    for i in r:
        return False
    c.execute('insert into post values("'+username+'","'+title+'","'+content+'")')
    conn.commit()

#gets an individual post
def getPost(title):
    conn = sqlite3.connect('bloginator.db')
    c = conn.cursor()
    c.execute('select * from post where title = "'+title+'"')
    return c.fetchall()

#how to read post table, for loop, index 0 is user, 1 is title, 2 is content

#edits a post
def edit(user, title, new_content):
    conn = sqlite3.connect('bloginator.db')
    c = conn.cursor()
    q = """
    UPDATE post
    SET content="' + new_content +'"
    WHERE user="'+ user + '"
    AND title="'+ title + '"
    """
    c.execute(q)
    conn.commit()
    conn.close()

#deletes a post from database
def delete(user, title):
    conn = sqlite3.connect('bloginator.db')
    c = conn.cursor()
    q = """
    DELETE FROM post
    WHERE user="'+ user +'"
    AND title="'+ title +'" 
    """
    c.execute(q)
    conn.commit()
    conn.close()
