
from flask import Flask, render_template, request, redirect, url_for
from database import get_connection
from math import ceil

app = Flask(__name__)


# Homepage: display bikes from PostgreSQL
@app.route("/")
def home():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT bike_id, name, price_per_hour, available
            FROM bikes
            ORDER BY bike_id
            """
        )

        bikes = cursor.fetchall()
        cursor.close()

        return render_template("index.html", bikes=bikes)

    finally:
        connection.close()


# Rent a bike
@app.route("/rent/<int:bike_id>", methods=["POST"])
def rent_bike(bike_id):
    customer_name = request.form.get("customer_name", "").strip()
    customer_phone = request.form.get("customer_phone", "").strip()

    if (
        not customer_name
        or not customer_phone.isdigit()
        or len(customer_phone) != 10
    ):
        return "Please enter a valid name and 10-digit phone number.", 400

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Lock the bike while checking availability
        cursor.execute(
            """
            SELECT available
            FROM bikes
            WHERE bike_id = %s
            FOR UPDATE
            """,
            (bike_id,)
        )

        bike = cursor.fetchone()

        if bike is None:
            connection.rollback()
            return "Bike not found.", 404

        if not bike[0]:
            connection.rollback()
            return "Sorry, this bike is already rented.", 409

        # Save the rental
        cursor.execute(
            """
            INSERT INTO rentals
                (bike_id, customer_name, customer_phone)
            VALUES (%s, %s, %s)
            """,
            (bike_id, customer_name, customer_phone)
        )

        # Mark the bike unavailable
        cursor.execute(
            """
            UPDATE bikes
            SET available = FALSE
            WHERE bike_id = %s
            """,
            (bike_id,)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        app.logger.exception("Rental failed")
        return "Rental failed. Check the PyCharm Run window.", 500

    finally:
        connection.close()

    return redirect(url_for("home"))


# Return a bike and display the receipt
@app.route("/return/<int:bike_id>", methods=["POST"])
def return_bike(bike_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Find the active rental and lock its records
        cursor.execute(
            """
            SELECT
                r.rental_id,
                r.rented_at,
                b.price_per_hour,
                b.name,
                CURRENT_TIMESTAMP
            FROM rentals r
            JOIN bikes b ON r.bike_id = b.bike_id
            WHERE r.bike_id = %s
              AND r.status = 'Rented'
            ORDER BY r.rented_at DESC
            LIMIT 1
            FOR UPDATE OF r, b
            """,
            (bike_id,)
        )

        rental = cursor.fetchone()

        if rental is None:
            connection.rollback()
            return "No active rental found for this bike.", 404

        rental_id, rented_at, price_per_hour, bike_name, returned_at = rental

        # Calculate billable hours, with a minimum of one hour

        from datetime import timezone

        if rented_at.tzinfo is not None:
            rented_at = rented_at.replace(tzinfo=None)

        if returned_at.tzinfo is not None:
            returned_at = returned_at.replace(tzinfo=None)

        duration_seconds = (returned_at - rented_at).total_seconds()
        hours = max(1, ceil(duration_seconds / 3600))

        total_cost = hours * price_per_hour

        # Save the return time, status, and total cost
        cursor.execute(
            """
            UPDATE rentals
            SET returned_at = %s,
                status = 'Returned',
                total_cost = %s
            WHERE rental_id = %s
            """,
            (returned_at, total_cost, rental_id)
        )

        # Make the bike available again
        cursor.execute(
            """
            UPDATE bikes
            SET available = TRUE
            WHERE bike_id = %s
            """,
            (bike_id,)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        app.logger.exception("Bike return failed")
        return "Return failed. Check the PyCharm Run window.", 500

    finally:
        connection.close()

    # Display the receipt after a successful return
    return render_template(
        "receipt.html",
        bike_name=bike_name,
        rented_at=rented_at,
        returned_at=returned_at,
        hours=hours,
        price_per_hour=price_per_hour,
        total_cost=total_cost
    )


# Rental History page

# Rental History page
@app.route("/history")
def rental_history():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        search = request.args.get("search", "").strip()

        cursor.execute(
            """
            SELECT
                r.rental_id,
                b.name,
                r.customer_name,
                r.customer_phone,
                r.rented_at,
                r.returned_at,
                r.status,
                r.total_cost
            FROM rentals r
            JOIN bikes b ON r.bike_id = b.bike_id
            WHERE
                COALESCE(r.customer_name, '') ILIKE %s
                OR COALESCE(r.customer_phone, '') ILIKE %s
            ORDER BY r.rental_id DESC
            """,
            (f"%{search}%", f"%{search}%")
        )

        rentals = cursor.fetchall()

        cursor.execute(
            """
            SELECT
                COUNT(*),
                COUNT(*) FILTER (WHERE status = 'Returned'),
                COUNT(*) FILTER (WHERE status = 'Rented'),
                COALESCE(
                    SUM(total_cost) FILTER (WHERE status = 'Returned'),
                    0
                )
            FROM rentals
            """
        )

        stats = cursor.fetchone()
        cursor.close()

        return render_template(
            "history.html",
            rentals=rentals,
            stats=stats,
            search=search
        )

    finally:
        connection.close()


# Start the website
if __name__ == "__main__":
    app.run(debug=True)
