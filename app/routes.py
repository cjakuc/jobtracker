from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, AddListingForm, ViewEditListingForm, FilterListingsForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Listing, Resume, CoverLetter
from werkzeug.urls import url_parse
from datetime import date, datetime

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # Get all the available jobs
    all_jobs = current_user.listings
    # Forming tuples for location SelectField
    locations_list = ["All"]
    for job in all_jobs:
        if job.location not in locations_list:
            locations_list.append(job.location)
    form = FilterListingsForm()
    form.location.choices = locations_list
    if form.validate_on_submit():
        flash(f"Filtering by: Location - {form.location.data} and Status - {form.status.data}")
        # Check if location filter is 'All' and filter
        if form.location.data != 'All':
            jobs = Listing.query.filter_by(location=form.location.data,
                                           user_id=current_user.id).all()
        else:
            jobs = Listing.query.filter_by(user_id=current_user.id).all()
        # Check if status filter is 'All'
        if form.status.data != 'All':
        # Check if status filter is 'Not rejected, turned down, or accepted' and filter
            if form.status.data == 'Not rejected, turned down, or accepted':
                jobs = [job for job in jobs if job.status not in ['Rejected', 'Turned Down', 'Accepted']]
            else:
                jobs = [job for job in jobs if job.status == form.status.data]
        return render_template('index.html', title='Home', jobs=jobs, form=form)
    else:
        jobs = all_jobs

    return render_template('index.html', title='Home', jobs=jobs, form=form)

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
                          status=form.status.data,
                          user=current_user)
        db.session.add(listing)
        db.session.commit()
        flash(f"Congratulations, you have added a new application for {listing.title} at {listing.company}")
        
        # jobs = current_user.listings
        # return render_template('index.html', title='Home', jobs=jobs, form=FilterListingsForm())
        return redirect(url_for('login'))
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
        # Update the database
        listing.company = form.company.data
        listing.title = form.title.data
        listing.description = form.description.data
        listing.location = form.location.data
        listing.date_added = form.date_added.data
        listing.resume = form.resume.data
        listing.cover_letter = form.cover_letter.data

        flash(f"Congratulations, you have edited an application for {listing.title} at {listing.company}")
        jobs = current_user.listings
        return render_template('index.html', title='Home', jobs=jobs)
    elif request.method == "GET":
        # Populate the form fields with the current values
        form.company.data = listing.company
        form.title.data = listing.title
        form.description.data = listing.description
        form.location.data = listing.location
        form.date_added.data = listing.date_added
        form.resume.data = listing.resume
        form.cover_letter.data = listing.cover_letter
        form.status.data = listing.status
    return render_template('add_edit_listing.html', title='View, Edit or Delete the Listing!', form=form)

@app.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_listing(id):
    listing = Listing.query.filter_by(id=id,
                                      user_id=current_user.id).first()
    
    db.session.delete(listing)
    db.session.commit()
    flash(f"Successfully deleted the {listing.title} listing at {listing.company}")
    return redirect(url_for('index'))