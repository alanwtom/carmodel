from app import app, db
from models import Car
import os
import requests


def ensure_placeholder() -> None:
    img_dir = os.path.join('static', 'img')
    os.makedirs(img_dir, exist_ok=True)
    placeholder = os.path.join(img_dir, 'car-placeholder.jpg')
    if not os.path.exists(placeholder):
        url = 'https://source.unsplash.com/featured/800x500/?car&sig=placeholder'
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            with open(placeholder, 'wb') as f:
                f.write(resp.content)
        except Exception:
            # fallback to a tiny 1x1 gif to avoid 404s if download fails
            with open(placeholder, 'wb') as f:
                f.write(b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')


def seed_cars() -> None:
    defaults = [
        dict(make='Toyota', model='Corolla', year=2020, category='economy', daily_rate=45.0, description='Reliable and fuel-efficient.'),
        dict(make='Honda', model='Civic', year=2021, category='sedan', daily_rate=55.0, description='Comfortable sedan with modern features.'),
        dict(make='Ford', model='Escape', year=2019, category='suv', daily_rate=65.0, description='Spacious SUV for family trips.'),
        dict(make='BMW', model='3 Series', year=2022, category='sedan', daily_rate=120.0, description='Luxury performance sedan.'),
        dict(make='Jeep', model='Wrangler', year=2018, category='suv', daily_rate=95.0, description='Adventure-ready off-road capability.'),
        dict(make='Kia', model='Rio', year=2020, category='economy', daily_rate=40.0, description='Compact and budget-friendly.')
    ]

    # Only add if no cars exist
    if Car.query.count() > 0:
        return

    for d in defaults:
        car = Car(
            make=d['make'],
            model=d['model'],
            year=d['year'],
            category=d['category'],
            daily_rate=d['daily_rate'],
            description=d['description'],
            is_available=True
        )
        db.session.add(car)
    db.session.commit()


if __name__ == '__main__':
    ensure_placeholder()
    with app.app_context():
        seed_cars()
    print('Default cars seeded and placeholder ensured.')
