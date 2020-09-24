from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, AddListingForm, ViewEditListingForm, FilterListingsForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Listing, Resume, CoverLetter
from werkzeug.urls import url_parse
from datetime import date, datetime
import plotly
import plotly.graph_objects as go
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # Get all the available jobs
    all_jobs = current_user.listings
    # Forming tuples for location SelectField
    locations_list = ["All Locations"]
    for job in all_jobs:
        if job.location not in locations_list:
            locations_list.append(job.location)
    form = FilterListingsForm()
    form.location.choices = locations_list
    
    filter_dict = {
        "All Locations": locations_list[1:],
        "All Statuses" : ['No Response', 'Interviewing', 'Rejected', 'Received Offer', 'Turned Down', 'Accepted'],
        "Not rejected, turned down, or accepted" : ['No Response', 'Interviewing', 'Received Offer']
    }
    if form.validate_on_submit():
        if form.location.data in filter_dict.keys():
            loc = filter_dict[form.location.data]
        else:
            loc = [form.location.data]
        if form.status.data in filter_dict.keys():
            stat = filter_dict[form.status.data]
        else:
            stat = [form.status.data]
        # Do the query
        jobs = Listing.query.filter(Listing.location.in_(loc),
                                    Listing.status.in_(stat),
                                    Listing.user_id==current_user.id)
        return render_template('index.html', title='Home', jobs=jobs, form=form)

    return render_template('index.html', title='Home', jobs=all_jobs, form=form)

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
        listing.resume.file_name = form.resume.data
        listing.cover_letter.file_name = form.cover_letter.data
        listing.status = form.status.data
        # db.session.add(listing)
        db.session.commit()

        flash(f"Congratulations, you have edited an application for {listing.title} at {listing.company}")
        jobs = current_user.listings
        return render_template('index.html', title='Home', jobs=jobs, form=FilterListingsForm())
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

@app.route('/analysis', methods=['GET'])
@login_required
def analysis():
    jobs = current_user.listings
    date_dict = {}
    for job in jobs:
        if job.date_added not in date_dict:
            date_dict[job.date_added.strftime('%Y-%m-%d')] = 1
        else:
            date_dict[job.date_added.strftime('%Y-%m-%d')] += 1

    x = list(date_dict.keys())
    y = list(date_dict.values())

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x = x,
        y = y
    ))

    fig.update_layout(
        title = {'text': "Number of Applications",
                 'y':0.9,
                 'x':0.5,
                 'xanchor': 'center',
                 'yanchor': 'top'},
        xaxis_title = "Date",
        yaxis_title = "Number of Applications",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(step="all"),
                    dict(count=7, label="1 Week", step="day", stepmode="backward"),
                    dict(count=1, label="1 Month", step="month", stepmode="backward")
                ])
            )
        )
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('analysis.html', title="Your Job Search Analysis",graphJSON=graphJSON)