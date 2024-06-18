import json
import os

from flask import Flask, render_template, flash, redirect, url_for, session, jsonify, request
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps


# Giriş yapıldı mı decoratoru
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Please login to view.", "warning")
            return redirect(url_for('login'))

    return decorated_function


class RegisterForm(Form):
    name = StringField("Name Surname", validators=[validators.Length(min=4, max=25)])
    username = StringField("Username", validators=[validators.Length(min=5, max=35)])
    email = StringField("E-Mail", validators=[validators.Email()])
    password = PasswordField("Password", validators=[
        validators.DataRequired(),
        validators.EqualTo(fieldname="confirm")
    ])
    confirm = PasswordField("Confirm Password")


class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")


app = Flask(__name__)
app.secret_key = "bitirme_tezi"
database = 'database.txt'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        with open(database, 'r') as f:
            users = f.readlines()
            f.close()

        for user in users:
            saved_name, saved_username, saved_email, saved_password = user.strip().split(',')
            if saved_username == username:
                flash(message="Such a user is already registered with this username...", category="danger")
                return redirect(url_for("register"))
            elif saved_email == email:
                flash(message="Such a user is already registered with this e-mail...", category="danger")
                return redirect(url_for("register"))

        with open(database, 'a') as f:
            f.write(f"{name},{username},{email},{password}\n")
        flash("You have registered successfully.", "success")
        os.makedirs(f"./data/{username}")
        os.makedirs(f"./static/{username}")
        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data

        with open(database, 'r') as f:
            users = f.readlines()

        for user in users:
            name, saved_username, email, password = user.strip().split(',')
            if saved_username == username and sha256_crypt.verify(password_entered, password):
                flash("You have successfully logged in.", "success")

                session["logged_in"] = True
                session["username"] = username

                return redirect(url_for('index'))
        flash("Check your username and password!", "danger")
        return redirect(url_for("login"))

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!", "info")
    return redirect(url_for("index"))


@app.route('/api/emotions', methods=["GET", "POST"])
def get_emotions():
    username = session["username"]

    with open('emotion_results.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)


@app.route('/isikkusgoz_combined.json', methods=["GET", "POST"])
def json_():
    username = session["username"]
    #ids = request.args.getlist('id')
    combined_data = []

    for i in range(5)[::-1]:
        with open(f'data/{username}/{username}_{i}.json', 'r') as file:
            data = json.load(file)
            data['id'] = i  # Add the ID to the data
            combined_data.append(data)
    sorted_data = sorted(combined_data, key=lambda x: x['time'])

    """with open(f'data/{username}/{username}_combined.json', 'w') as file:
        json.dump(combined_data, file, indent=4)"""
    return jsonify(sorted_data)


if __name__ == '__main__':
    app.run(debug=True)
