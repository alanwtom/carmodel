import os
import uuid
from urllib.parse import quote_plus

import requests

from app import app, db
from models import Car, CarImage


def ensure_directories() -> None:
    uploads_dir = os.path.join('static', 'uploads')
    img_dir = os.path.join('static', 'img')
    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)


def build_stock_image_url(car: Car) -> str:
    # Use Unsplash Source which redirects to a suitable image (no API key needed)
    # Fall back keywords if fields are missing
    keywords = 'car'
    try:
        parts = [str(car.make or ''), str(car.model or ''), 'car']
        parts = [p for p in parts if p]
        if parts:
            keywords = ' '.join(parts)
    except Exception:
        pass
    # Fixed size for consistency; add a random query to avoid caching the same image
    return f"https://source.unsplash.com/featured/1280x720/?{quote_plus(keywords)}&sig={uuid.uuid4().hex}"


def download_image(url: str, dest_path: str) -> bool:
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        with open(dest_path, 'wb') as f:
            f.write(resp.content)
        return True
    except Exception:
        return False


def seed_car_images(max_images_per_car: int = 3) -> None:
    uploads_dir = os.path.join('static', 'uploads')
    cars = Car.query.all()
    for car in cars:
        # Skip if gallery already exists
        if car.images and len(car.images) >= 1:
            continue

        # If legacy image_url exists, keep it for now and just add one stock image as primary
        num_to_add = max_images_per_car
        for idx in range(num_to_add):
            url = build_stock_image_url(car)
            unique_name = f"{uuid.uuid4().hex}.jpg"
            disk_path = os.path.join(uploads_dir, unique_name)
            ok = download_image(url, disk_path)
            if not ok:
                continue
            relative_path = 'static/uploads/' + unique_name
            db.session.add(CarImage(car_id=car.id, file_path=relative_path, is_primary=(idx == 0)))
        db.session.commit()


def seed_hero_background() -> None:
    hero_path = os.path.join('static', 'img', 'hero-bg.jpg')
    if os.path.exists(hero_path):
        return
    url = f"https://source.unsplash.com/featured/1600x900/?car,road&sig={uuid.uuid4().hex}"
    download_image(url, hero_path)


if __name__ == '__main__':
    ensure_directories()
    with app.app_context():
        seed_car_images()
    seed_hero_background()
    print('Seeding complete.')


