from flask import Flask, redirect, url_for, render_template, request
from search import olx_search, searching_function_loop, send_msg
import sqlite3
import os

from flask import Flask, request, make_response
from functools import wraps 

app = Flask(__name__)
app.secret_key = "hello"

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'uzytkownik1' and auth.password == 'password888':
            return f(*args, **kwargs)

        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated

@app.route("/")
@auth_required
def main():
    connectDB = sqlite3.connect('search_phrases.db')
    cDB = connectDB.cursor()
    cDB.execute("SELECT rowid, * FROM pharses")
    searches_list = cDB.fetchall()
    connectDB.close()
    connectDB = sqlite3.connect('users.db')
    cDB = connectDB.cursor()
    cDB.execute("SELECT rowid, * FROM users")
    users_list = cDB.fetchall()
    connectDB.close()
    return render_template("index.html", searches_list = searches_list, users_list=users_list)

@app.route("/add", methods = ["POST", "GET"])
@auth_required
def add_pcharse():  
    if request.method == "POST":
        connectDB = sqlite3.connect('search_phrases.db')
        cDB = connectDB.cursor()
        phrase = request.form["phrase"]
        min_price = request.form["min_price"]
        max_price = request.form["max_price"]
        category = request.form["category"]
        try:
           user = request.form["user"]
        except:
            user = 0
        print(category)
        city = request.form["city"]
        max_distance = request.form["max_distance"]
        search_amount = 0
        cDB.execute(f"SELECT * FROM pharses WHERE phrase = '{phrase}'")
        same_items = cDB.fetchall()
        while len(same_items)>0:
            phrase = f'{phrase} '
            cDB.execute(f"SELECT * FROM pharses WHERE phrase = '{phrase}'")
            same_items = cDB.fetchall()
        cDB.execute("INSERT INTO pharses VALUES (?,?,?,?,?,?,?,?)", (phrase, min_price, max_price, category, city, max_distance, search_amount, user))
        connectDB.commit()
        connectDB.close()
        print(phrase, min_price, max_price, category, city, max_distance)
        send_msg(f'Dodano nowe wyszukiwanie: {phrase}', user)
    return redirect(url_for("main"))


@app.route("/delete/<item_id>")
@auth_required
def delete(item_id):
    print(item_id)
    connectDB = sqlite3.connect('search_phrases.db')
    cDB = connectDB.cursor()
    cDB.execute(f"SELECT * FROM pharses WHERE ROWID = '{item_id}'")
    item_name = cDB.fetchall()[0][0]
    
    try:
        os.remove(f"{item_name}.db")
    except:
       pass
    cDB.execute(f"DELETE FROM pharses WHERE ROWID = '{item_id}'")
    
    connectDB.commit()
    connectDB.close()
    return redirect(url_for("main"))

@app.route("/users")
@auth_required
def users():
  
    connectDB = sqlite3.connect('users.db')
    cDB = connectDB.cursor()
    cDB.execute("SELECT rowid, * FROM users")
    users_list = cDB.fetchall()
    connectDB.close()
    return render_template("users.html", users_list = users_list)


@app.route("/add-user", methods = ["POST", "GET"])
@auth_required
def add_user():  
    if request.method == "POST":
        connectDB = sqlite3.connect('users.db')
        cDB = connectDB.cursor()
        name = request.form["user"]
        user_id = request.form["user-id"]
        
        cDB.execute("INSERT INTO users VALUES (?,?)", (name, user_id))
        connectDB.commit()
        connectDB.close()
        
        send_msg(f'Dodano nowego użytkownika: {name}', user_id)
    return redirect(url_for("users"))


@app.route("/delete-user/<user_id>")
@auth_required
def delete_user(user_id):
    connectDB = sqlite3.connect('users.db')
    cDB = connectDB.cursor()
    cDB.execute(f"SELECT * FROM users WHERE ROWID = '{user_id}'")

    cDB.execute(f"DELETE FROM users WHERE ROWID = '{user_id}'")
    
    connectDB.commit()
    connectDB.close()
    return redirect(url_for("users"))



@app.route("/start")
@auth_required
def start():
    searching_function_loop()
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(debug=True)