from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, AddListingForm, ViewEditListingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Listing, Resume, CoverLetter
from werkzeug.urls import url_parse
from datetime import date, datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    jobs = current_user.listings
    return render_template('index.html', title='Home', jobs=jobs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is authenticated, redirect to index/home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Else, go through the login form
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        # Save next page, if anon user was redirected from protected
        ## page to login page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            # url_parse ensures the URL is relative
            # if it's not, an attacker, could set the next value to
            # a malicious site
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/add_listing', methods=['GET', 'POST'])
@login_required
def add_listing():
    form = AddListingForm()
    if form.validate_on_submit():
        # See if the resume exists in the Resume table
        new_resume = Resume.query.filter_by(file_name=form.resume.data,
                                           user_id=current_user.id).first()
        # If it doesn't exist, insert it
        if new_resume is None:
            new_resume = Resume(file_name=form.resume.data,
                                user_id=current_user.id)
            # Add and commit new resume
            db.session.add(new_resume)
            db.session.commit()

        # Do the same thing for cover letter
        ## Turn this into a helper function later?
        new_cl = CoverLetter.query.filter_by(file_name=form.cover_letter.data,
                                            user_id=current_user.id).first()
        if new_cl is None:
            new_cl = CoverLetter(file_name=form.cover_letter.data,
                                 user_id=current_user.id)
            # Add and commit new cl
            db.session.add(new_cl)
            db.session.commit()

        # Create a new listing object w/ form details and insert it
        listing = Listing(company=form.company.data, title=form.title.data, 
                          description=form.description.data, location=form.location.data,
                          date_added=form.date_added.data,
                          resume=new_resume, cover_letter=new_cl,
                          user=current_user)
        db.session.add(listing)
        db.session.commit()
        flash(f"Congratulations, you have added a new application for {listing.title} at {listing.company}")
        
        jobs = current_user.listings
        return render_template('index.html', title='Home', jobs=jobs)
    return render_template('add_edit_listing.html', title='Add a New Application/Listing!', form=form)

@app.route('/view_edit_listing/<listing_id>', methods=['GET', 'POST'])
@login_required
def view_edit_listing(listing_id):
    form = ViewEditListingForm()
    listing = Listing.query.filter_by(id=listing_id,
                                      user_id=current_user.id).first()
    # If it doesn't exist for the user, throw custom error
    if listing is None:
        return render_template('404_listing.html')
    if form.validate_on_submit():

        flash(f"Congratulations, you have edited an application for {listing.title} at {listing.company}")
        jobs = current_user.listings
        return render_template('index.html', title='Home', jobs=jobs)
    elif request.method == "GET":
        form.company.data = listing.company
        form.title.data = listing.title
        form.description.data = listing.description
        form.location.data = listing.location
        form.date_added.data = listing.date_added
        form.resume.data = listing.resume
        form.cover_letter.data = listing.cover_letter
    return render_template('add_edit_listing.html', title='View, Edit or Delete the Listing!', form=form)