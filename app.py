from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegistrationForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def index():
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def show_register_form():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        
        db.session.add(new_user)
        db.session.commit()
        session['user'] = new_user.username
        return redirect(f"/users/{new_user.username}")
    else:
        return render_template('register.html', form=form)
    
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user:

            flash(f"Welcome {user.first_name}!", 'success')
            session['user'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            flash('Invalid username/password', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/users/<username>')
def show_secret(username):
    if "user" not in session:
        flash("Please login", 'danger')
        return redirect('/login')
    elif session['user'] != username:
        flash("Not authorized", 'danger')
        return redirect('/login')
    else:
        user = User.query.get(username)
        return render_template('user-info.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if session['user'] != username:
        flash('You are not authorized to perform this function', 'danger')
        return redirect('/login')
    else:
        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        return redirect('/')
    
@app.route('/users/<username>/feedback/add', methods=['POST', 'GET'])
def add_new_feedback(username):
    if session['user'] != username:
        flash('You must be logged in to add feedback.', 'danger')
        return redirect('/login')
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{username}")
    return render_template('add-feedback.html', form=form, username=username)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if feedback.user.username != session['user']:
        flash('You must be logged in to add feedback.', 'danger')
        return redirect('/login')
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{feedback.user.username}")
    return render_template('update-feedback.html', form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if session['user'] != feedback.user.username:
        flash('You are not authorized to perform this function', 'danger')
        return redirect('/login')
    else:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.user.username}")