### Deployment Documentation and Setup Guide

This guide will help you set up and deploy your **Car Rental Web Application** using Flask, SQLAlchemy, and Flask-Login. It will also outline how to deploy the app in a production environment and provide documentation for the API endpoints and system architecture.

---

### **1. Setup Instructions**

#### **Step 1: Prerequisites**

Make sure you have the following installed on your machine:

* Python 3.x
* pip (Python package installer)
* Virtualenv (optional but recommended for creating isolated environments)
* Git (for version control)
* PostgreSQL or SQLite (for the database)

#### **Step 2: Clone the Repository**

```bash
git clone https://github.com/your-repository/car-rental-app.git
cd car-rental-app
```

#### **Step 3: Create a Virtual Environment**

It's a good practice to use a virtual environment to avoid dependency conflicts.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

#### **Step 4: Install Dependencies**

Once the virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

#### **Step 5: Configure Environment Variables**

Create a `.env` file in the root of the project with the following settings:

```bash
FLASK_APP=app.py
FLASK_ENV=development  # Use 'production' in production environments
SECRET_KEY=your_secret_key_here  # Make sure to use a secure key for production
SQLALCHEMY_DATABASE_URI=sqlite:///app.db  # Use SQLite or PostgreSQL URI
SQLALCHEMY_TRACK_MODIFICATIONS=False  # Disable Flask-SQLAlchemy modification tracking
```

**Note:** If you are using PostgreSQL, you can replace the `SQLALCHEMY_DATABASE_URI` with the appropriate PostgreSQL URI:

```bash
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/car_rental_db
```

#### **Step 6: Initialize the Database**

Run the following commands to set up the database and create the tables:

```bash
python
from app import db
db.create_all()  # Creates the database tables
```

#### **Step 7: Seed the Database (Optional)**

If you want to add default data (e.g., cars) to the database, run:

```bash
python seed_default_cars.py
python seed_images.py
```

#### **Step 8: Run the Flask Development Server**

Start the Flask development server with:

```bash
flask run
```

The app should now be running at `http://127.0.0.1:5000/`.

---

### **2. Deployment Guide**

#### **Deploying to Heroku**

Heroku is a popular platform for deploying Flask applications. Below are the steps to deploy to Heroku.

##### **Step 1: Install Heroku CLI**

If you don't have it already, install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

##### **Step 2: Create a Heroku App**

Login to Heroku:

```bash
heroku login
```

Create a new Heroku application:

```bash
heroku create your-app-name
```

##### **Step 3: Add Heroku PostgreSQL**

Heroku provides PostgreSQL as a service. Add it to your app:

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

Heroku will automatically set the `DATABASE_URL` environment variable for you, which you can use for the `SQLALCHEMY_DATABASE_URI` in your app.

##### **Step 4: Push Code to Heroku**

Initialize a git repository (if not already initialized), add Heroku as a remote, and push your code:

```bash
git init
git add .
git commit -m "Initial commit"
git push heroku master
```

##### **Step 5: Configure Environment Variables on Heroku**

Set the environment variables on Heroku, including the Flask secret key:

```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your_production_secret_key
```

##### **Step 6: Run Database Migrations on Heroku**

Run migrations to create your database tables:

```bash
heroku run python
from app import db
db.create_all()  # Create the database tables on Heroku
```

##### **Step 7: Open the Application**

Now, your app should be live on Heroku. Open it in a web browser:

```bash
heroku open
```

---

### **3. API Endpoints Documentation**

This section documents the main API endpoints in your application. They are used to manage users, cars, bookings, and more.

#### **Authentication Routes**

* **POST /login**

  * **Description**: Authenticates a user with email and password.
  * **Request**:

    ```json
    {
      "email": "user@example.com",
      "password": "password123"
    }
    ```
  * **Response**: Returns a session cookie upon successful login.

* **POST /register**

  * **Description**: Registers a new user.
  * **Request**:

    ```json
    {
      "name": "John Doe",
      "email": "user@example.com",
      "phone": "1234567890",
      "password": "password123"
    }
    ```
  * **Response**: Returns a success message upon successful registration.

* **POST /logout**

  * **Description**: Logs the current user out of the system.

#### **Car Routes**

* **GET /cars**

  * **Description**: Lists all available cars.
  * **Request**:

    * Optional query parameters:

      * `category`: Filter cars by category (e.g., `sedan`, `SUV`).
      * `sort`: Sort cars by price (`price_low` or `price_high`).
  * **Response**: A list of cars in JSON format.

* **GET /car/<car_id>**

  * **Description**: View details of a specific car.
  * **Request**: No request body, just the `car_id` as part of the URL.
  * **Response**: Car details in JSON format.

#### **Booking Routes**

* **POST /book/<car_id>**

  * **Description**: Books a car for the current user.
  * **Request**:

    ```json
    {
      "start_date": "2023-10-10T10:00:00",
      "end_date": "2023-10-12T10:00:00"
    }
    ```
  * **Response**: A confirmation of the booking along with booking details.

* **GET /my-bookings**

  * **Description**: Lists all bookings made by the current user.
  * **Request**: No request body, just the user’s session.
  * **Response**: A list of the user’s bookings.

* **POST /admin/booking/<booking_id>/cancel**

  * **Description**: Admin can cancel a booking.
  * **Request**: No request body, just the `booking_id` in the URL.
  * **Response**: Confirmation message upon successful cancellation.

#### **Admin Routes**

* **GET /admin/cars**

  * **Description**: Lists all cars in the admin panel.
  * **Response**: List of all cars.

* **POST /admin/car/new**

  * **Description**: Admin can add a new car to the inventory.
  * **Request**:

    ```json
    {
      "make": "Toyota",
      "model": "Corolla",
      "year": 2020,
      "category": "economy",
      "daily_rate": 45.0,
      "description": "A reliable and fuel-efficient car."
    }
    ```
  * **Response**: Confirmation message with the details of the newly added car.

---

### **4. System Architecture**

The architecture of the **Car Rental Web Application** is built with the following components:

#### **Frontend**

* **HTML**: The structure of the web pages.
* **CSS (Bootstrap)**: Used for styling and making the pages responsive.
* **JavaScript (Jinja Templates)**: Dynamic client-side functionality such as form validation and data handling.

#### **Backend**

* **Flask**: The core web framework.

  * **Flask-Login**: Used to handle user authentication and session management.
  * **Flask-SQLAlchemy**: Used to manage the database with SQLAlchemy ORM.

#### **Database**

* **PostgreSQL/SQLite**: Stores users, cars, bookings, and other app data.

  * **Tables**: `User`, `Car`, `Booking`, `CarImage`.

#### **External Services**

* **Unsplash API**: Used to fetch car images.
* **Heroku**: Platform-as-a-Service (PaaS) used to deploy the app.

#### **Application Flow**

1. **User Authentication**: Users register, log in, and manage their profile.
2. **Car Booking**: Users can view available cars and make bookings.
3. **Admin Panel**: Admins can manage cars, users, and bookings.
4. **Analytics**: Admins can view booking statistics and car popularity metrics.

---
