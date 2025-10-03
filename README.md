# Car Rental 7 - Car Rental System

A comprehensive car rental web application built with Flask that allows users to browse, search, and book vehicles.

## Features

- **User Authentication**: Register, login, and manage user accounts
- **Car Inventory Management**: Browse cars with filtering by category and price
- **Booking System**: Book cars with date validation and cost calculation
- **Admin Dashboard**: Manage cars and view bookings

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/carmodel.git
   cd carmodel
   ```

2. Activate the virtual environment
   ```
   # On Windows
   activate.bat
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run the application
   ```
   python app.py
   ```

5. Access the website at http://localhost:5000

## Project Structure

```
Travora/
├── app.py                  # Main application file
├── models.py               # Database models
├── forms.py                # Form classes
├── routes.py               # Application routes
├── requirements.txt        # Project dependencies
├── static/                 # Static files (CSS, JS, images)
│   └── css/
│       └── main.css        # Main stylesheet
└── templates/              # HTML templates
    ├── admin/              # Admin templates
    │   ├── cars.html
    │   └── dashboard.html
    ├── layout.html         # Base template
    ├── home.html           # Homepage
    ├── cars.html           # Car listing
    ├── car_detail.html     # Car details
    ├── login.html          # Login page
    ├── register.html       # Registration page
    ├── booking_confirmation.html
    └── my_bookings.html    # User bookings
```

## Database Schema

- **Users**: Stores user information and authentication details
- **Cars**: Manages vehicle inventory
- **Bookings**: Handles rental reservations

## Development

To contribute to this project:

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## Team Members

- Stephanie Luu
- Nathan Taylor
- Jireh Ayertey

## License

This project is licensed under the MIT License - see the LICENSE file for details.