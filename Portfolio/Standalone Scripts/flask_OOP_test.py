from flask import Flask, Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class CreateRegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()], render_kw={"type": "password"})
    confirm_password = StringField("Confirm Password", validators=[DataRequired()], render_kw={"type": "password"})
    submit = SubmitField("Sign me up!")

class CreateLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()], render_kw={"type": "password"})
    submit = SubmitField("Log me in!")

class myClass():
    def __init__(self, router):
        self.blueprint = Blueprint('myClass', __name__)
        self.user_logged_in = False
        self.users = [{"username": "akhtarH", "email": "akhtarhasan2005@gmail.com", "password": "akh2005", "role": "admin"}]
        router('/')(self.index)
        router('/create_user')(self.create_user)
        router('/login')(self.login)
        router('/register')(self.register)
        router('/logout')(self.logout)

    def index(self):
        return render_template('index.html')

    def create_user(self):
        form = CreateRegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            confirm_password = form.confirm_password.data
            if password == confirm_password:
                self.users.append({"username": username, "email": email, "password": password, "role": "user"})
                return redirect(url_for('login'))
            else:
                return redirect(url_for('create_user'))
        return render_template('create_user.html', form=form)
    
    def login(self):
        form = CreateLoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            for user in self.users:
                if user["email"] == email and user["password"] == password:
                    self.user_logged_in = True
                    return redirect(url_for('index'))
            return redirect(url_for('login'))
        return render_template('login.html', form=form)
    
    def register(self):
        form = CreateRegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            confirm_password = form.confirm_password.data
            if password == confirm_password:
                self.users.append({"username": username, "email": email, "password": password, "role": "user"})
                return redirect(url_for('login'))
            else:
                return redirect(url_for('register'))
        return render_template('register.html', form=form)
    
    def logout(self):
        self.user_logged_in = False
        return redirect(url_for('index'))

app = Flask(__name__)
myObj = myClass( app.route )
Bootstrap5(app)
app.register_blueprint(myObj.blueprint)
app.config['SECRET_KEY'] = 'randomString'
app.run(host='localhost', port=5000)