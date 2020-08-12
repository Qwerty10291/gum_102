from flask import Flask, request, redirect, render_template, url_for, session, json, abort
from werkzeug.security import generate_password_hash, check_password_hash
import asyncio
import websockets
from edu import parser, check_edu
import datetime as dt
from db import Database
import requests
import lxml.html

db = Database('main.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'oiwgvbib43ri34btui4b3tib43jutrn23jtbfo23qigfh'
chat = [['1', '1'], ['2','2']]

def add_message(login, text):
    global chat
    print(login)
    print(text)
    if len(chat) <= 50:
        chat.append([login, text])
    else:
        chat = chat[1:] + [[login, text]]


@app.route('/')
def main():
    if 'user' not in session:
        return render_template('index.html', not_auth=True)
    return render_template('index.html', not_auth=False, login=db.get_login(session['user']), messages=chat, days=parser(db.get_edu(session['user'])[0], db.get_edu(session['user'])[1]))


@app.route('/add_message', methods=['GET', 'POST'])
def input_message():
    if 'user' not in session:
        return 'Error'
    if request.method == 'POST':
        try:
            add_message(db.get_login(session['user']), request.form['text'])
            print(request.form['text'])
            return 'done'
        except:
            return 'error'
    return ''


@app.route('/load_messages')
def load_messages():
    if 'user' not in session:
        return abort(404)
    return json.dumps(chat)


@app.route('/load_message')
def load_message():
    if 'user' not in session:
        return redirect('/')
    return json.dumps(chat[-1])


@app.route('/check_message', methods=['GET', 'POST'])
def check_message():
    if request.method == 'POST':
        if request.form['message'] != chat[-1][1] or request.form['login'] != chat[-1][0]:
            return 'yes'
        else:
            return 'no'
    return ''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/')
    if request.method == 'POST':
        if db.check_user(request.form['login']):
            if check_password_hash(db.get_password(request.form['login']), request.form['password']):
                session['user'] = db.get_id(request.form['login'])
                return redirect('/')
            else:
                return render_template('login.html', flag='Неправильный пароль')
        else:
            return render_template('login.html', flag='Такого пользователя нет')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect('/')
    if request.method == 'POST':
        if (not db.check_user(request.form['login'])) and (request.form['pass1'] == request.form['pass2']):
            if check_edu(request.form['edu_login'], request.form['edu_pass']):
                db.add_user(request.form['login'], generate_password_hash(request.form['pass1']), request.form['edu_login'], request.form['edu_pass'], db.count_users())
                session['user'] = db.get_id(request.form['login'])
                return redirect('/')
            else:
                return render_template('register.html', flag='Неправильный логин или пароль от edu tatar.')
        else:
            return render_template('register.html', flag='Произошла ошибка.Возможно такой логин занят или пароли не повторяются')
    return render_template('register.html')


@app.route('/logout')
def logout():
    if 'user' not in session:
        return redirect('/')
    session.pop('user')
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
