# 🌹 Rose & Ride — Bike Rental Management System

A web-based bike rental management system built with **Python, Flask, PostgreSQL, HTML, and CSS**. Rose & Ride allows users to view available bikes, rent and return bikes, calculate rental charges, generate receipts, and track rental history through a dashboard.

## ✨ Features

- **Bike Listing:** View bikes, hourly rental prices, and availability.
- **Bike Rental:** Rent a bike by entering customer details.
- **Bike Return:** Return rented bikes and automatically calculate rental charges.
- **Billing & Receipts:** Generate a receipt with rental duration, hourly rate, and total cost.
- **Rental History:** View previous and current rental records.
- **Search Functionality:** Search rental records by customer name or phone number.
- **Dashboard Statistics:** View total rentals, completed rentals, active rentals, and total revenue.
- **Database Integration:** Store and manage bike and rental records using PostgreSQL.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and billing calculations |
| Flask | Web application framework |
| PostgreSQL | Relational database |
| Psycopg2 | Python–PostgreSQL connection |
| python-dotenv | Load database configuration from environment variables |
| HTML | Web page structure |
| CSS | Styling and layout |
| Jinja2 | Dynamic HTML templates |

## 📁 Project Structure

```text
PythonProject2Bike/
│
├── app.py                 # Main Flask application
├── database.py            # PostgreSQL connection
├── BikeRentalSystem.py    # Additional Python project module
├── main.py                # Additional Python entry-point module
├── requirements.txt       # Python dependencies
├── .gitignore             # Excludes private and unnecessary files
├── .env                   # Local database configuration (not committed)
│
└── templates/
    ├── index.html         # Homepage and bike listings
    ├── receipt.html       # Rental receipt
    └── history.html       # Rental history and dashboard
```

## ⚙️ Prerequisites

Before running the project, install:

- Python 3.10 or a compatible version
- PostgreSQL
- Git
- A code editor such as PyCharm

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/riyaa11111/rose-and-ride-bike-rental.git
cd rose-and-ride-bike-rental
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Open PostgreSQL or pgAdmin and create a database named:

```sql
CREATE DATABASE bike_rental_db;
```

Create the `bikes` and `rentals` tables using the schema provided in the project documentation or your database setup. The `rentals` table should reference `bikes` through `bike_id`.

### 5. Configure environment variables

Create a local `.env` file in the project root. Add your own PostgreSQL credentials:

```dotenv
DB_HOST=localhost
DB_NAME=bike_rental_db
DB_USER=postgres
DB_PASSWORD=YOUR_LOCAL_DATABASE_PASSWORD
DB_PORT=5432
```

Replace the password placeholder with your local PostgreSQL password.

**Security note:** Never commit `.env` or publish database passwords. The repository's `.gitignore` should exclude `.env`.

### 6. Start the application

```bash
python app.py
```

Open the local URL displayed in your terminal, typically:

```text
http://127.0.0.1:5000/
```

## 💰 Rental Billing Logic

The application calculates rental charges based on the bike's hourly rate and rental duration.

- Partial hours are rounded up to the next full hour.
- The minimum billable duration is one hour.
- Total cost = billable hours × price per hour.

**Example:** A bike costing ₹100 per hour rented for 2 hours and 10 minutes is charged for 3 hours, giving a total of ₹300.

## 🗄️ Database Overview

### Bikes

Stores bike information such as:

- Bike ID
- Bike name
- Price per hour
- Availability status

### Rentals

Stores rental information such as:

- Rental ID
- Bike ID
- Customer name and phone number
- Rental and return timestamps
- Rental status
- Total cost

A foreign key connects each rental to its bike record.

## 🔒 Security and Configuration

- Database credentials are loaded from `.env`.
- `.env`, `.venv`, and Python cache files are excluded through `.gitignore`.
- Do not commit real passwords, API keys, or personal customer data.
- Use appropriate validation and security measures before deploying the application publicly.

## 🔮 Future Enhancements

- Customer registration and login
- Online payment integration
- Booking dates and time-slot management
- Administrative authentication and role-based access
- Downloadable PDF receipts
- Revenue charts and analytics
- Deployment to a cloud hosting platform

## 👩‍💻 Author

**Riya Jaiswal**

B.Tech — Computer Science Engineering (Artificial Intelligence and Machine Learning)

## 📄 License

This project is intended for educational and portfolio purposes. Add a license file if you wish to specify permissions for reuse and distribution.
