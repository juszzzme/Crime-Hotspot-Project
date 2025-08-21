from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db
from app.forms.auth_forms import LoginForm, SignupForm

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
            
        flash('Invalid email or password. Please try again.', 'danger')
        
    return render_template('auth/login.html', form=form, now=datetime.utcnow())

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = SignupForm()
    if form.validate_on_submit():
        # Generate username from email (before @)
        username = form.email.data.split('@')[0]
        
        user = User(
            email=form.email.data,
            username=username,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
            is_active=True,
            is_admin=False,
            email_confirmed=False
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Successfully registered! Please log in.', 'success')
        return redirect(url_for('auth.login'))
        
    from datetime import datetime
    return render_template('auth/signup.html', form=form, now=datetime.utcnow())

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
