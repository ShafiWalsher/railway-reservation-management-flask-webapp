from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required,current_user
from .models import Feedback, Station, Ticket, Train, User
from . import db
from datetime import datetime,date

# Creating "views" Blueprint
views = Blueprint('views', __name__)

# HTML page view (home page route)
@views.route('/')
def home():
    return render_template("index.html", user=current_user)


# HTML page view (book-ticket page route)
@views.route('/book-ticket', methods=['GET','POST'])
@login_required
def bookticket():
    
    # Query the Station table in DB
    trains = Train.query.order_by(Train.id).all()
    
    if request.method == 'POST':
        if 'search_submit' in request.form :
            loc_from = request.form.get('loc_from')
            loc_to = request.form.get('loc_to')

            if len(loc_from) < 4: 
                flash('Invalid City Name!.', category='error')
            elif len(loc_to) < 4:
                flash('Invalid City Name!.', category='error')
            else : 
                city_s = Station.query.filter_by(name=loc_from).all()
                city_d = Station.query.filter_by(name=loc_to).all()

                # if found then return
                if city_s and city_d:
                    flash('Succes cities found', category='success')
                    return render_template("book-ticket.html",user=current_user,cities_source=city_s,cities_dest=city_d,trains=trains)  
                else:
                    flash('Unable find any available trains. please try again!.', category='error')
                    
    
    
        if 'book_ticket_submit' in request.form:
            u_id = current_user.id
            name = request.form.get('name')
            mobile = request.form.get('mobile')
            loc_f = request.form.get('from')
            loc_t = request.form.get('to')
            train_no = request.form.get('train_no')
            train_cls = request.form.get('train_cls')
            b_date = request.form.get('booking_date')
            # Convert date into Python DateTime()
            booking_date = datetime.strptime(b_date,'%Y-%m-%d').date()
            #booking_date = date(b_date,'%Y-%m-%d'))


            # Validate Form Data
            if len(name) < 2 :
                flash('Please provide valid Name.!', category='error')
            elif len(mobile) < 10:
                flash('Please provide valid Mobile Number.!', category='error')
            elif len(loc_f) < 2 and len(loc_t) < 2:
                flash('Please provide valid Source/Destination.!', category='error')
            elif len(train_no) < 1:
                flash('Please provide valid Train Number.!', category='error')
            elif len(train_cls) < 4:
                flash('Please provide valid Train Class.!', category='error')
            elif booking_date < date.today():
                flash('Please provide valid Date.!', category='error')
            else :
                # Query the Train table in DB
                train = Train.query.filter_by(id=train_no).first()
                # Access train name
                t_name = train.name

                # Query
                new_ticket = Ticket(user_name=name,user_id=u_id,train_id=train_no,mobile=mobile,location_s=loc_f,location_d=loc_t,train_name=t_name,date=booking_date,train_class=train_cls)

                # Add new Ticket
                db.session.add(new_ticket)
                db.session.commit()

                flash('Your Ticket has been Booked!', category='success')

    return render_template("book-ticket.html", user = current_user, trains=trains)


# HTML page view (contact page route)
@views.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if len(name) < 2 :
            flash('Please provide a valid name.', category="error")
        elif len (email) < 6 :
            flash('Please provide a valid email.', category="error")
        elif len(subject) < 2:
            flash('Please specify subject properly.', category="error")
        elif len(message) < 30 : 
            flash('Message is too short!', category="error")
        else : 
            query = Feedback(email=email,name=name,subject=subject,message=message)

            # Adding new user to database
            db.session.add(query)
            # print('NEW USER ADDED')
            db.session.commit()
            
            flash('Email sent succefully. We\'ll get back too soon!..', category="success")

    return render_template("contact.html", user = current_user )


# HTML page view (about page)
@views.route('/about')
def about():
    return render_template("about.html", user = current_user)

'''
# HTML page view (ADD STAION RECORD Temp)
@views.route('/station', methods=['GET','POST'])
def tempform():
    if request.method == 'POST':
        plat_id = request.form.get('platform_no')
        station = request.form.get('station')
        T_id = request.form.get('t_id')
        arr_time = request.form.get('arr_time')
        depart_time = request.form.get('depart_time')

        new_row = Station(platform_id=plat_id,name=station,train_id=T_id,arrival=arr_time,depart=depart_time)
        
        db.session.add(new_row)
        db.session.commit()
            
        flash('DATA ADDED Succesfully!.', category="success")

    else : 
        flash('Unable to add data', category='error')


    return render_template("tempform.html")
'''

# HTML page view (Dashboard)
@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user = current_user,)