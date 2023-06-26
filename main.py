import os

from flask import Flask, abort
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from data import db_session
from data.users import User
import datetime
from flask import request
from data.works import Works
from flask import render_template
from forms.users import RegisterForm
from flask import redirect
from flask import make_response
from flask import session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlite3
from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image
from test import test
import traceback
import sqlite3

app = Flask(__name__, static_folder="static")
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
lessons = ["Знакомство со средой", "Условный оператор", "Простые встроенные функции",
               "Знакомство с циклом while", "Знакомство с циклом for"]
tasks = [["вывести \"hello yandex\" без кавычек", "вывести сумму 2 и 2", "сложить переменные a = 10 и b = 20"], ["получить на вход два числа. вывести меньшее. не использовать min", "добавить в предыдущую программу начальный ввод, и если пользователь введет +, то вывести самое большое число, а если -, то самое маленькое", "сравнить две введенные строки по длинам, вывести большую"], ["получите сумму 2 и 2 с помощью sum", "найдите модуль -5 * -5 ** 2 + -6", "сделайте простейший калькулятор с помощью eval"], ["получить на вход пять чисел. вывести их сумму", "получать на вход числа, пока не придет 0. когда придет 0, вывести самое маленькое и самое большое число.", "усложните предыдущую задачу: если приходит отрицательное число, то берите его квадрат."], ["напишите функцию факториала. вам дается число, выведите его факториал", "напишите функцию, которая перебирает числа от 1до n, и находит среднее. n вводится"]]
tests = [[["hello yandex\r\n"], ["4\r\n"], ["30\r\n"]], [[b"-3\n", b"5\n", "-3\r\n"], [b"+\n",b"-3\n", b"5\n", "5\r\n"], [b"jhadhsdahsj\n", b"abc\n", "jhadhsdahsj\r\n"]], [["4\r\n"], ["119\r\n"], [b"5*3\n", "15\r\n"]], [[b"1\n", b"2\n", b"3\n", b"4\n", b"5\n", "15\r\n"], [b"-1\n", b"2\n", b"-3\n", b"4\n", b"-5\n", b"0\n", "4\r\n-5\r\n"], [b"-1\n", b"2\n", b"-3\n", b"4\n", b"-5\n", b"0\n", "25\r\n1\r\n"]], [[b"5\n", "120\r\n"], [b"7\n", "4\r\n"]]]


def find_balls():
    ballsob = sqlite3.connect("for_users.db").cursor().execute(f"""SELECT results from works where id={str(current_user.id)}""").fetchall()[0][0]
    return sum(map(int, list(str(ballsob)))) - 14


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    print(email, password, remember_me)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
@login_required
def index():
    lessons = ["Знакомство со средой", "Условный оператор", "Простые встроенные функции",
               "Знакомство с циклом while", "Знакомство с циклом for"]
    lessons.reverse()
    return render_template("main.html", lessons=lessons, name=current_user.name, mail=current_user.email, balls=find_balls(),
                           desc=current_user.about, avatar=current_user.avatar_path)


@app.route("/lessons/<int:lesson_num>")
@login_required
def open_lesson(lesson_num):
    return render_template("lessons.html", lesson_num=lesson_num, list_of_balls=str(sqlite3.connect("for_users.db").cursor().execute(f"SELECT results from works where id={current_user.id}").fetchall()[0][0])[(lesson_num - 1) * 3:(lesson_num - 1) * 3 + 3].replace("1", "незачет№").replace("2", "зачет№").split("№")[:-1], lesson=lessons[lesson_num - 1], name=current_user.name, mail=current_user.email, balls=find_balls(),
                           desc=current_user.about, avatar=current_user.avatar_path, tasks=tasks[lesson_num - 1])

@app.route("/tasks/<int:lesson_num>/<int:task_num>", methods=['GET', 'POST'])
@login_required
def open_task(lesson_num, task_num):
    con = sqlite3.connect("for_users.db")
    cur = con.cursor()
    if request.method == 'POST':
        with open("solution.py", "w") as f:
            f.write(request.values['comment'])
        try:
            n = test(tests[lesson_num - 1][task_num - 1])
            text = "тест пройден" if n[0] == n[1] else "тест не пройден: ввод программы - " + str(n[2]) + " правильный вывод - " + str(n[0]) + " ваш вывод: " + str(n[1])

            p, x = cur.execute(f"SELECT content, results from works where id={current_user.id}").fetchall()[0]
            x = list(str(x))
            print(x, (lesson_num - 1) * 3 + task_num - 1)
            x[(lesson_num - 1) * 3 + task_num - 1] = "2" if n[0] == n[1] else "1"
            print(x)
            p = p.split("*")
            for i in range(len(p)):
                p[i] = p[i].split("~")

            p[lesson_num - 1][task_num - 1] = request.values['comment'].replace("\"", "'")
            print(p)
            for i in range(len(p)):
                p[i] = "~".join(p[i])
            print(p)
            p = "*".join(p)
            print(p, x)
            print(f"""UPDATE works SET content = \"{p}\", SET results = \"{x}\" WHERE id = {current_user.id}""")
            cur.execute(f"""UPDATE works SET content = \"{p}\", results = \"{''.join(x)}\" WHERE id = {current_user.id}""")
            con.commit()

        except BaseException:
            text = "ошибка! " + traceback.format_exc()
        return render_template("tasks.html", last_attempt_text=request.values['comment'], taskhistory=text, num_tusk=task_num, lesson_num=lesson_num, task_num=task_num,
                               task_text=tasks[lesson_num - 1][task_num - 1], name=current_user.name,
                               mail=current_user.email, balls=find_balls(),
                               desc=current_user.about, avatar=current_user.avatar_path)
    return render_template("tasks.html", last_attempt_text=cur.execute(f"SELECT content from works where id={current_user.id}").fetchall()[0][0].split("*")[lesson_num - 1].split("~")[task_num - 1],task_num=task_num, lesson_num=lesson_num, taskhistory="", num_tusk=task_num, task_text=tasks[lesson_num - 1][task_num - 1], name=current_user.name,
                           mail=current_user.email, balls=find_balls(),
                           desc=current_user.about, avatar=current_user.avatar_path)
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name, mail=current_user.email, balls=find_balls(),
                           desc=current_user.about, avatar=current_user.avatar_path)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        print()
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/about")
def about():
    return render_template("about.html")

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if request.method == 'POST' and 'photo' in request.files:
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            filename = photos.save(request.files['photo'])
            img = Image.open("static/img/" + filename)
            img = img.resize((400, int(img.size[1] / img.size[0] * 400)) if img.size[1] > img.size[0] else
                             (int(img.size[0] / img.size[1] * 400), 400))
            img = img.crop(((img.size[0] - 400) // 2, 0,
                            (img.size[0] - 400) // 2 + 400, 400) if
                            img.size[0] > img.size[1] else
                            (0, (img.size[1] - 400) // 2, 400,
                            (img.size[1] - 400) // 2 + 400))
            name = str(int(open("lastsaved.txt").read()) + 1)
            img.save(f"static/img/{name}.png")
            open("lastsaved.txt", "w").write(name)
            os.remove("static/img/" + filename)
            user = User(
                name=form.name.data,
                email=form.email.data,
                about=form.about.data,
                avatar_path=name + ".png"
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            con = sqlite3.connect("for_users.db")
            cur = con.cursor()
            cur.execute(f"INSERT INTO works (id, content, results) VALUES({user.id}, \"{'~' * 2 + '*' + '~' * 2 + '*' +'~' * 2 + '*' + '~' * 2 + '*' + '~' * 1}\", \"{'1' * 14}\")")
            con.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form, message="загрузите аватар")
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("for_users.db")
    app.run()


if __name__ == '__main__':
    main()
