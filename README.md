# 🚲 Rose & Ride — Bike Rental Management System

A web-based bike rental management system built with **Python, Flask, and PostgreSQL**. Rose & Ride allows users to view available bikes, rent and return bikes, calculate rental charges, generate receipts, and track rental history.

🔗 **Live Demo:** [Open Rose & Ride](https://rose-and-ride-bike-rental.onrender.com)

💻 **Source Code:** [GitHub Repository](https://github.com/riyaa11111/rose-and-ride-bike-rental)

---

## ✨ Features

- 🚲 **Bike Availability:** View bikes, hourly rates, and availability.
- 📝 **Bike Rentals:** Record customer details and rent available bikes.
- 🔄 **Bike Returns:** Process returns and update bike availability.
- 💰 **Automated Billing:** Calculate rental charges based on the rental duration and hourly rate.
- 🧾 **Digital Receipts:** View rental and billing details.
- 📋 **Rental History:** Review previous rental records.
- 🔍 **Customer Search:** Search rental records using customer name or phone number.
- 📊 **Dashboard Statistics:** View key rental information.
- 🗄️ **Persistent Database:** Store bike and rental records in PostgreSQL.


## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Web framework and routing |
| HTML / CSS | Website interface |
| PostgreSQL | Relational database |
| psycopg2 | PostgreSQL connectivity |
| python-dotenv | Local environment configuration |
| Gunicorn | Production application server |
| Render | Web application hosting |
| Neon | Cloud PostgreSQL hosting |
| Git & GitHub | Version control and source code management |

## 🏗️ Architecture

```text
User's Browser
      |
      v
Flask Web Application
      |
      v
PostgreSQL Database
   (Neon Cloud)
```

The application is deployed on Render, while Neon provides the cloud database.

## 🚀 Live Application

Try the deployed application:

**[https://rose-and-ride-bike-rental.onrender.com](https://rose-and-ride-bike-rental.onrender.com)**

Note: The free web service may take a little time to wake up after a period of inactivity.

## 💻 Run Locally

### Prerequisites

- Python installed
- Git installed
- A PostgreSQL database, such as a Neon project

### 1. Clone the repository

```bash
git clone https://github.com/riyaa11111/rose-and-ride-bike-rental.git
cd rose-and-ride-bike-rental
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
DATABASE_URL=your_postgresql_connection_string
```

Replace the placeholder with your own PostgreSQL connection string. Keep the connection string private and never commit `.env` to GitHub.

### 5. Set up the database

Create the required `bikes` and `rentals` tables and insert the initial bike records in your PostgreSQL database before running the application.

### 6. Start the application

```bash
python app.py
```

Open the local address displayed in your terminal, usually `http://127.0.0.1:5000`.

## 🗃️ Database Overview

The application uses two primary tables:

- **`bikes`** — Stores bike IDs, names, hourly rental prices, and availability.
- **`rentals`** — Stores rental IDs, bike IDs, rental and return timestamps, customer details, rental status, and total charges.

## 📌 Project Highlights

This project demonstrates practical experience with:

- Building a web application using Flask.
- Connecting Python applications to PostgreSQL.
- Implementing database-driven CRUD workflows.
- Managing rental availability and return operations.
- Calculating billing based on rental duration.
- Using environment variables for database configuration.
- Deploying a Python application with a cloud-hosted database.

## 🔮 Future Improvements

- User authentication and role-based access.
- An admin panel for managing bikes and rental rates.
- Online payments and booking confirmations.
- Rental reports and revenue analytics.
- Automated database backups and monitoring.

## 👩‍💻 Author

**Riya Jaiswal**

B.Tech Computer Science Engineering — AI & ML

[GitHub Profile](https://github.com/riyaa11111)

---

⭐ If you find this project useful, consider giving the repository a star!
