'''
Задание


Создать страницу, на которой будет форма для ввода имени и электронной почты,
при отправке которой будет создан cookie-файл с данными пользователя,
а также будет произведено перенаправление на страницу приветствия,где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл 
с данными пользователя и произведено перенаправление на страницу ввода имени и электронной почты.

'''


from flask import Flask, make_response, redirect, request, render_template, session, url_for


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome/', methods=['POST'])
def welcome():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        session['user'] = {'name': name, 'email': email}
        response = make_response(redirect('/greet'))
        response.set_cookie('user_data', f'{name}:{email}')

        return response
        
    
    return redirect('/')


@app.route('/greet/')
def greet():
    user_data = session.get('user')

    if user_data is None:
        user_cookie = request.cookies.get('user_data')
        if user_cookie:
            name, email = user_cookie.split(':')
            user_data = {'name': name, 'email': email}

    if user_data:
        return render_template('greet.html', user=user_data)
    
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    response = make_response(redirect('/'))
    response.delete_cookie('user_data')

    return response



app.secret_key = 'geekbrains'
if __name__ == '__main__':
    app.run(debug=True)
