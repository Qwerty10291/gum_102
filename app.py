from flask import Flask, request, redirect, render_template, url_for, session, json, abort
from werkzeug.security import generate_password_hash, check_password_hash
import asyncio
import websockets
import datetime
from edu import parser, check_edu
import datetime as dt
from db import Database
from event import Event
import requests
import lxml.html

db = Database('main.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'oiwgvbib43ri34btui4b3tib43jutrn23jtbfo23qigfh'
chat = [['1', '1']]
events = []

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
    return render_template('index.html', not_auth=False, events=events, login=db.get_login(session['user']), messages=chat, days=parser(db.get_edu(session['user'])[0], db.get_edu(session['user'])[1]))


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

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'admin' in session:
        return redirect('/admin')
    if request.method == 'POST':
        if (request.form['login'] == 'root') and (request.form['password'] == 'qwerty1029'):
            session['admin'] = True
            return redirect('/admin')
        else:
            return render_template('login.html', flag='Неправильный логин или пароль')
    return render_template('admin_login.html')

@app.route('/admin')
def admin_panel():
    if 'admin' not in session:
        return abort(404)
    return render_template('admin.html', elements=events)

@app.route('/event_add', methods=['POST'])
def add_event():
    global events
    if 'admin' not in session:
        return abort(404)
    events.append(Event(request.form['sub'], request.form['type'], request.form['description'], request.form['date'], len(events)))
    return redirect('/admin')

@app.route('/event_update', methods=['POST'])
def update_event():
    global events
    if 'admin' not in session:
        return abort(404)
    for i in events:
        if i.id == int(request.form['id']):
            i.update(request.form['sub'], request.form['type'], request.form['description'], request.form['date'])
    return redirect('/admin')

@app.route('/event_del', methods=['POST'])
def delete_event():
    global events
    if 'admin' not in session:
        return abort(404)
    for num, i in enumerate(events):
        if i.id == int(request.form['id']):
            del events[num]
            break
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
