from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False, index=True)
    model = db.Column(db.String(50), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    category = db.Column(db.String(20), nullable=False, index=True)  # sedan, SUV, economy
    daily_rate = db.Column(db.Float, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    # Legacy single image URL support (kept for backward compatibility)
    image_url = db.Column(db.String(200), nullable=True)
    is_available = db.Column(db.Boolean, default=True, index=True)
    bookings = db.relationship('Booking', backref='car', lazy=True)
    # New: related images
    images = db.relationship(
        'CarImage', backref='car', lazy='selectin', cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<Car {self.make} {self.model} ({self.year})>'

    @property
    def primary_image_path(self):
        # Prefer explicitly marked primary, else first image, else legacy image_url
        if self.images:
            primary = next((img for img in self.images if img.is_primary), None)
            first = primary or self.images[0]
            return first.file_path
        return self.image_url

    @property
    def gallery_image_paths(self):
        if self.images:
            return [img.file_path for img in self.images]
        return [p for p in [self.image_url] if p]


class CarImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False, index=True)
    # Stored as a static-relative path e.g., "uploads/uuid_filename.jpg"
    file_path = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Booking {self.id} - User: {self.user_id}, Car: {self.car_id}>'
    
    def cancel(self):
        self.status = 'canceled'
        db.session.commit()

    def modify(self, new_start_date, new_end_date):
        self.start_date = new_start_date
        self.end_date = new_end_date
        db.session.commit()
