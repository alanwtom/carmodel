Certainly! Below is the updated **Deployment Documentation and Setup Guide** with commands for **Windows**, **Linux**, and **macOS**. This ensures cross-platform compatibility for setting up the Car Rental Web Application.

---

### **Deployment Documentation and Setup Guide**

This guide provides detailed steps for setting up the **Car Rental Web Application** on different platforms, including **Windows**, **Linux**, and **macOS**.

---

### **1. Setup Instructions**

#### **Step 1: Prerequisites**

Ensure you have the following tools installed:

* **Python 3.x**
* **pip** (Python package installer)
* **Virtualenv** (recommended for isolated environments)
* **Git** (for version control)
* **PostgreSQL or SQLite** (for the database)

### **For Windows**

1. **Install Python 3.x** from [python.org](https://www.python.org/downloads/).
2. **Install Git** from [git-scm.com](https://git-scm.com/download/win).
3. **Install PostgreSQL** from [postgresql.org](https://www.postgresql.org/download/windows/).

### **For Linux (Ubuntu/Debian)**

1. Install Python and pip:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git
   ```

2. Install PostgreSQL:

   ```bash
   sudo apt install postgresql postgresql-contrib
   ```

### **For macOS**

1. **Install Python 3.x** using Homebrew:

   ```bash
   brew install python
   ```

2. **Install Git** using Homebrew:

   ```bash
   brew install git
   ```

3. **Install PostgreSQL** using Homebrew:

   ```bash
   brew install postgresql
   ```

---

#### **Step 2: Clone the Repository**

Open a terminal and clone the repository:

```bash
git clone https://github.com/your-repository/car-rental-app.git
cd car-rental-app
```

---

#### **Step 3: Create a Virtual Environment**

For **Windows**:

```bash
python -m venv venv
venv\Scripts\activate
```

For **Linux/macOS**:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

#### **Step 4: Install Dependencies**

Once the virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

---

#### **Step 5: Configure Environment Variables**

Create a `.env` file in the root of the project with the following settings:

For **Windows**:

```bash
copy .env.example .env
```

For **Linux/macOS**:

```bash
cp .env.example .env
```

Edit the `.env` file to match your setup. Below is an example configuration:

```bash
FLASK_APP=app.py
FLASK_ENV=development  # Use 'production' in production environments
SECRET_KEY=your_secret_key_here  # Use a secure key for production
SQLALCHEMY_DATABASE_URI=sqlite:///app.db  # SQLite or PostgreSQL URI
SQLALCHEMY_TRACK_MODIFICATIONS=False  # Disable Flask-SQLAlchemy modification tracking
```

For **PostgreSQL** (in `.env`):

```bash
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/car_rental_db
```

---

#### **Step 6: Initialize the Database**

Launch Python shell to initialize the database:

```bash
python
from app import db
db.create_all()  # Creates the database tables
```

---

#### **Step 7: Seed the Database (Optional)**

(Optional: If you want to seed some default data, such as cars, use the following commands.)

```bash
python seed_default_cars.py
python seed_images.py
```

---

#### **Step 8: Run the Flask Development Server**

Now that everything is set up, run the Flask server:

For **Windows**:

```bash
flask run
```

For **Linux/macOS**:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development  # Set to production in production
flask run
```

You can now access the app at `http://127.0.0.1:5000/`.

---

### **2. Deployment Guide**

If you want to deploy the app to your own server or a cloud platform, follow the steps below.

---

#### **Deploying to a Virtual Private Server (VPS)**

##### **Step 1: Set up a Virtual Machine (VM)**

You can deploy to any VPS like **AWS EC2**, **DigitalOcean**, or **Linode**. Once the server is set up, SSH into it:

```bash
ssh user@your-server-ip
```

---

##### **Step 2: Install Dependencies on the Server**

1. **Update the system:**

   For **Linux** (Ubuntu/Debian):

   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv postgresql
   ```

2. **Clone the repository** to the server:

   ```bash
   git clone https://github.com/your-repository/car-rental-app.git
   cd car-rental-app
   ```

3. **Create a virtual environment** on the server:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

##### **Step 3: Configure PostgreSQL (If Using PostgreSQL)**

1. **Create a new PostgreSQL database**:

   ```bash
   sudo -u postgres psql
   CREATE DATABASE car_rental_db;
   CREATE USER car_rental_user WITH PASSWORD 'your_password';
   ALTER ROLE car_rental_user SET client_encoding TO 'utf8';
   ALTER ROLE car_rental_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE car_rental_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE car_rental_db TO car_rental_user;
   ```

2. **Update the `.env` file** with the PostgreSQL connection string:

   ```bash
   SQLALCHEMY_DATABASE_URI=postgresql://car_rental_user:your_password@localhost/car_rental_db
   ```

---

##### **Step 4: Initialize the Database**

Run the following Python commands to initialize the database:

```bash
python
from app import db
db.create_all()  # Creates the database tables
```

---

##### **Step 5: Configure Environment Variables**

Make sure your environment variables are set correctly on the server, either through the `.env` file or using systemd for production environments.

---

##### **Step 6: Set Up Nginx as a Reverse Proxy**

1. Install **Nginx**:

   For **Linux**:

   ```bash
   sudo apt install nginx
   ```

2. Create an Nginx configuration for your app:

   ```bash
   sudo nano /etc/nginx/sites-available/car-rental-app
   ```

   Add the following configuration:

   ```nginx
   server {
       listen 80;
       server_name your-server-ip-or-domain;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

3. **Enable the site** and restart Nginx:

   ```bash
   sudo ln -s /etc/nginx/sites-available/car-rental-app /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

---

##### **Step 7: Set Up Gunicorn to Serve Flask**

1. Install **Gunicorn**:

   ```bash
   pip install gunicorn
   ```

2. **Start Gunicorn** with 4 worker processes:

   ```bash
   gunicorn -w 4 app:app
   ```

You can use **systemd** to set Gunicorn to run as a service and ensure it starts automatically.

---

### **3. API Endpoints Documentation**

**Authentication Routes:**

* **POST /login**
  Authenticates a user with email and password.

  **Request**:

  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

  **Response**: Session cookie upon successful login.

* **POST /register**
  Registers a new user.

  **Request**:

  ```json
  {
    "name": "John Doe",
    "email": "user@example.com",
    "phone": "1234567890",
    "password": "password123"
  }
  ```

  **Response**: Success message upon registration.

---

This guide should help you set up the **Car Rental Web Application** on Windows, Linux,

#### **Application Flow**

1. **User Authentication**: Users register, log in, and manage their profile.
2. **Car Booking**: Users can view available cars and make bookings.
3. **Admin Panel**: Admins can manage cars, users, and bookings.
4. **Analytics**: Admins can view booking statistics and car popularity metrics.

---
