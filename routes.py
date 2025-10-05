from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login_manager
from models import User, Car, Booking
from datetime import datetime
from forms import LoginForm, RegistrationForm, CarForm, BookingForm
from forms import BookingModificationForm
from sqlalchemy import func

import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route
@app.route('/')
def home():
    cars = Car.query.filter_by(is_available=True).all()
    return render_template('home.html', cars=cars)

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Car routes
@app.route('/cars')
def cars():
    category = request.args.get('category', '')
    sort = request.args.get('sort', '')
    
    query = Car.query
    
    if category:
        query = query.filter_by(category=category)
    
    if sort == 'price_low':
        query = query.order_by(Car.daily_rate.asc())
    elif sort == 'price_high':
        query = query.order_by(Car.daily_rate.desc())
    
    cars = query.all()
    return render_template('cars.html', cars=cars, category=category, sort=sort)

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    form = BookingForm()
    return render_template('car_detail.html', car=car, form=form)

# Booking routes
@app.route('/book/<int:car_id>', methods=['GET', 'POST'])
@login_required
def book_car(car_id):
    car = Car.query.get_or_404(car_id)
    if not car.is_available:
        flash('This car is not available for booking.', 'danger')
        return redirect(url_for('cars'))
    
    form = BookingForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        
        # Check if dates are valid
        if start_date >= end_date:
            flash('End date must be after start date.', 'danger')
            return render_template('car_detail.html', car=car, form=form)
        
        # Check if car is available for these dates
        conflicting_bookings = Booking.query.filter(
            Booking.car_id == car_id,
            Booking.end_date >= start_date,
            Booking.start_date <= end_date
        ).all()
        
        if conflicting_bookings:
            flash('Car is not available for the selected dates.', 'danger')
            return render_template('car_detail.html', car=car, form=form)
        
        # Calculate total cost
        days = (end_date - start_date).days
        total_cost = days * car.daily_rate
        
        # Create booking
        booking = Booking(
            user_id=current_user.id,
            car_id=car.id,
            start_date=start_date,
            end_date=end_date,
            total_cost=total_cost
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Your booking has been confirmed!', 'success')
        return redirect(url_for('booking_confirmation', booking_id=booking.id))
    
    return render_template('car_detail.html', car=car, form=form)

@app.route('/booking/<int:booking_id>/confirmation')
@login_required
def booking_confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    return render_template('booking_confirmation.html', booking=booking)

@app.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)

# Admin routes
@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)
    
    return render_template('admin/dashboard.html')

@app.route('/admin/cars')
@login_required
def admin_cars():
    if not current_user.is_admin:
        abort(403)
    
    cars = Car.query.all()
    return render_template('admin/cars.html', cars=cars)

@app.route('/admin/car/new', methods=['GET', 'POST'])
@login_required
def admin_new_car():
    if not current_user.is_admin:
        abort(403)
    
    form = CarForm()
    if form.validate_on_submit():
        car = Car(
            make=form.make.data,
            model=form.model.data,
            year=form.year.data,
            category=form.category.data,
            daily_rate=form.daily_rate.data,
            description=form.description.data,
            image_url=form.image_url.data,
            is_available=True
        )
        
        db.session.add(car)
        db.session.commit()
        
        flash('Car has been added to inventory!', 'success')
        return redirect(url_for('admin_cars'))
    
    return render_template('admin/car_form.html', form=form, title='Add New Car')

@app.route('/admin/car/<int:car_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_car(car_id):
    if not current_user.is_admin:
        abort(403)
    
    car = Car.query.get_or_404(car_id)
    form = CarForm()
    
    if form.validate_on_submit():
        car.make = form.make.data
        car.model = form.model.data
        car.year = form.year.data
        car.category = form.category.data
        car.daily_rate = form.daily_rate.data
        car.description = form.description.data
        car.image_url = form.image_url.data
        car.is_available = form.is_available.data
        
        db.session.commit()
        
        flash('Car has been updated!', 'success')
        return redirect(url_for('admin_cars'))
    
    # Pre-populate form
    form.make.data = car.make
    form.model.data = car.model
    form.year.data = car.year
    form.category.data = car.category
    form.daily_rate.data = car.daily_rate
    form.description.data = car.description
    form.image_url.data = car.image_url
    form.is_available.data = car.is_available
    
    return render_template('admin/car_form.html', form=form, title='Edit Car')

@app.route('/admin/car/<int:car_id>/delete', methods=['POST'])
@login_required
def admin_delete_car(car_id):
    if not current_user.is_admin:
        abort(403)
    
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    
    flash('Car has been deleted!', 'success')
    return redirect(url_for('admin_cars'))

@app.route('/admin/bookings')
@login_required
def admin_bookings():
    if not current_user.is_admin:
        abort(403)
    
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template('admin/bookings.html', bookings=bookings)

# Cancel booking route (admin only)
@app.route('/admin/booking/<int:booking_id>/cancel', methods=['POST'])
@login_required
def admin_cancel_booking(booking_id):
    if not current_user.is_admin:
        abort(403)

    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()

    flash('Booking has been canceled.', 'success')
    return redirect(url_for('admin_bookings'))

# Modify booking route (admin only)
@app.route('/admin/booking/<int:booking_id>/modify', methods=['GET', 'POST'])
@login_required
def admin_modify_booking(booking_id):
    if not current_user.is_admin:
        abort(403)

    booking = Booking.query.get_or_404(booking_id)
    form = BookingModificationForm()

    if form.validate_on_submit():
        # Ensure car is available for the new dates
        conflicting_bookings = Booking.query.filter(
            Booking.car_id == booking.car_id,
            Booking.end_date >= form.start_date.data,
            Booking.start_date <= form.end_date.data
        ).all()

        if conflicting_bookings:
            flash('Car is not available for the selected dates.', 'danger')
        else:
            booking.start_date = form.start_date.data
            booking.end_date = form.end_date.data
            booking.total_cost = (booking.end_date - booking.start_date).days * booking.car.daily_rate
            db.session.commit()
            flash('Booking has been updated.', 'success')
            return redirect(url_for('admin_bookings'))

    # Pre-fill form with current booking details
    form.start_date.data = booking.start_date
    form.end_date.data = booking.end_date

    return render_template('admin/booking_modify.html', form=form, booking=booking)


@app.route('/admin/analytics')
@login_required
def admin_analytics():
    if not current_user.is_admin:
        abort(403)

    # Bookings per month
    bookings_per_month = db.session.query(
        func.strftime('%Y-%m', Booking.start_date).label('month'),
        func.count(Booking.id).label('bookings_count')
    ).group_by('month').all()

    # Popular cars (most booked)
    popular_cars = db.session.query(
        Car.make, Car.model, func.count(Booking.id).label('booking_count')
    ).join(Booking, Booking.car_id == Car.id).group_by(Car.id).order_by(func.count(Booking.id).desc()).limit(5).all()

    return render_template('admin/analytics.html', bookings_per_month=bookings_per_month, popular_cars=popular_cars)

# routes.py

# View and manage users
@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)

    users = User.query.all()
    return render_template('admin/users.html', users=users)

# Deactivate/Activate user
@app.route('/admin/user/<int:user_id>/toggle', methods=['POST'])
@login_required
def admin_toggle_user(user_id):
    if not current_user.is_admin:
        abort(403)

    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()

    flash(f'User {"activated" if user.is_active else "deactivated"} successfully!', 'success')
    return redirect(url_for('admin_users'))

# Delete user
@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin:
        abort(403)

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash('User has been deleted.', 'success')
    return redirect(url_for('admin_users'))

# # routes.py
# @app.route('/admin/users')
# @login_required
# def admin_users():
#     if not current_user.is_admin:
#         abort(403)

#     # Fetch all users from the database
#     users = User.query.all()
#     return render_template('admin/users.html', users=users)

@app.route('/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    if not current_user.is_admin:
        abort(403)

    user = User.query.get_or_404(user_id)

    # Form for editing user details (add form logic here)
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        user.is_admin = 'is_admin' in request.form  # Toggle admin status based on checkbox
        db.session.commit()
        flash('User information updated!', 'success')
        return redirect(url_for('admin_users'))

    return render_template('admin/user_edit.html', user=user)

# @app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
# @login_required
# def admin_delete_user(user_id):
#     if not current_user.is_admin:
#         abort(403)

#     user = User.query.get_or_404(user_id)
#     db.session.delete(user)
#     db.session.commit()
#     flash(f'User {user.name} has been deleted.', 'danger')
#     return redirect(url_for('admin_users'))
