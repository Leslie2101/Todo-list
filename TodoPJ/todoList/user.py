from flask import Blueprint, render_template, request, flash, redirect, url_for
from todoList.model import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user 
from .import db 

user = Blueprint("user", __name__)

@user.route('/',methods=["GET","POST"])
@user.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email = email).first()
        remember = request.form.get("remember")
        if user:
            if check_password_hash(user.password, password):
                #session.permanent = True 
                login_user(user, remember=(str(remember) == "checked"))  
                flash(f"Welcome back, {user.user_name}!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Wrong password, please check again!", category="error")
        else:
            flash("User does not exist", category="error")
    return render_template("login.html", user= current_user)

@user.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.query.filter_by(email= email).first()

        # validate user 
        if user:
            flash("User existed!", category="error")
        elif (len(email) < 4):
            flash("Email must be greater than 3 characters. ", category="error")
        elif len(password) < 7:
            flash("Email must be greater than 7 characters. ", category="error")
        elif password != confirm_password:
            flash("Passwords does not match! ", category="error")
        else:
            password = generate_password_hash(password, method="sha256")
            new_user = User(email, password, username)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash(f"Welcome {new_user.user_name}!", category="success")
                login_user(new_user)
                return redirect(url_for("views.home"))
            except:
                "error"

    return render_template("signup.html", user=current_user)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))