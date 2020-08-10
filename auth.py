@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect('/')
    if request.method == 'POST':
        if (not db.check_user(request.form['login'])) and (request.form['pass1'] == request.form['pass2']):
            db.add_user(request.form['login'], generate_password_hash(request.form['pass1']), db.count_users())
            session['user'] = db.get_id(request.form['login'])
            return redirect('/')
        else:
            return render_template('register.html', flag='Произошла ошибка.Возможно такой логин занят или пароли не повторяются')
    return render_template('register.html')

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