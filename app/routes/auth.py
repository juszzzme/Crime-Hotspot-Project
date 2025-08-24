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
        email = form.email.data.lower().strip()
        password = form.password.data

        print(f"[AUTH] Login attempt: {email}")  # Debug logging

        # Demo credentials for immediate testing
        demo_credentials = {
            'admin@crimesense.com': 'admin123',
            'user@crimesense.com': 'user123',
            'demo@crimesense.com': 'demo123'
        }

        # Check demo credentials first
        if email in demo_credentials and password == demo_credentials[email]:
            print(f"[SUCCESS] Demo login successful for {email}")  # Debug logging

            # Find or create user
            user = User.query.filter_by(email=email).first()
            if not user:
                # Create user on the fly for demo
                user = User(
                    email=email,
                    username=email.split('@')[0],
                    first_name='Demo',
                    last_name='User',
                    is_active=True,
                    is_admin=(email == 'admin@crimesense.com'),
                    email_confirmed=True
                )
                user.password = password  # This will hash it
                db.session.add(user)
                db.session.commit()
                print(f"[SUCCESS] Created new demo user: {email}")

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            print(f"[REDIRECT] Redirecting to: {next_page or url_for('main.index')}")  # Debug logging
            return redirect(next_page or url_for('main.index'))

        # Fallback to database verification
        user = User.query.filter_by(email=email).first()

        if user:
            print(f"[SUCCESS] User found in database: {user.email}, Active: {user.is_active}")  # Debug logging

            # Direct password verification using werkzeug
            from werkzeug.security import check_password_hash
            password_valid = check_password_hash(user.password_hash, password)

            print(f"[AUTH] Database password verification: {password_valid}")  # Debug logging

            if password_valid and user.is_active:
                print(f"[SUCCESS] Database login successful for {user.email}")  # Debug logging
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                print(f"[REDIRECT] Redirecting to: {next_page or url_for('main.index')}")  # Debug logging
                return redirect(next_page or url_for('main.index'))
            else:
                print(f"[ERROR] Database login failed - Password valid: {password_valid}, Active: {user.is_active}")  # Debug logging
        else:
            print(f"[ERROR] User not found in database: {email}")  # Debug logging

        flash('Invalid email or password. Please try again.', 'danger')
    else:
        if form.errors:
            print(f"[ERROR] Form validation errors: {form.errors}")  # Debug logging

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
