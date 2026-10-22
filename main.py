from database import get_connection

class Bike:

    def __init__(self, bike_id, name, price_per_hour):
        self.bike_id = bike_id
        self.name = name
        self.price_per_hour = price_per_hour
        self.available = True

    def display(self):
        print(f"Bike ID: {self.bike_id}")
        print(f"Bike Name: {self.name}")
        print(f"Price per hour: ₹{self.price_per_hour}")
        print(f"Available: {self.available}")

    def rent(self):
            if self.available:
                self.available = False
                print(f"{self.name} has been rented successfully!")
            else:
                print(f"Sorry, {self.name} is already rented.")

    def return_bike(self):
        if not self.available:
            self.available = True
            print(f"{self.name} has been returned successfully!")
        else:
            print(f"{self.name} was not rented.")


class RentalSystem:

    def __init__(self):
        self.bikes = []

    def add_bike(self, bike):
        self.bikes.append(bike)
        print(f"{bike.name} added successfully!")

    def display_bikes(self):
        print("\n===== AVAILABLE BIKES =====")

        for bike in self.bikes:
            if bike.available:
                bike.display()
                print("--------------------")

    def find_bike(self, bike_id):
        for bike in self.bikes:
            if bike.bike_id == bike_id:
                return bike

        return None

    def load_bikes(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT bike_id, name, price_per_hour, available FROM bikes"
        )
        rows = cursor.fetchall()

        self.bikes = []

        for row in rows:
            bike = Bike(row[0], row[1], row[2])
            bike.available = row[3]
            self.bikes.append(bike)

        cursor.close()
        connection.close()

        print("Bikes loaded from PostgreSQL successfully!")

    def return_bike(self, bike_id):
        bike = self.find_bike(bike_id)

        if bike is None:
            print("Sorry, bike ID not found.")
        elif bike.available:
            print("This bike has not been rented.")
        else:
            connection = get_connection()
            cursor = connection.cursor()

            try:
                cursor.execute("""
                    SELECT rental_id, rented_at
                    FROM rentals
                    WHERE bike_id = %s
                      AND status = 'Rented'
                    ORDER BY rented_at DESC, rental_id DESC
                    LIMIT 1
                """, (bike_id,))

                rental = cursor.fetchone()

                if rental is None:
                    print("No active rental record found for this bike.")
                    return

                rental_id = rental[0]

                cursor.execute("""
                    UPDATE rentals
                    SET returned_at = CURRENT_TIMESTAMP,
                        status = 'Returned',
                        total_cost = GREATEST(
                            1,
                            CEIL(
                                EXTRACT(
                                    EPOCH FROM (
                                        CURRENT_TIMESTAMP - rented_at
                                    )
                                ) / 3600.0
                            )
                        ) * %s
                    WHERE rental_id = %s
                """, (bike.price_per_hour, rental_id))

                cursor.execute("""
                    UPDATE bikes
                    SET available = TRUE
                    WHERE bike_id = %s
                """, (bike_id,))

                cursor.execute("""
                    SELECT total_cost
                    FROM rentals
                    WHERE rental_id = %s
                """, (rental_id,))

                total_cost = cursor.fetchone()[0]

                connection.commit()
                bike.available = True

                print(f"{bike.name} has been returned successfully!")
                print(f"Total rental cost: ₹{total_cost}")
                print("Return time and cost saved to PostgreSQL.")

            except Exception as error:
                connection.rollback()
                print("Could not save return:", error)

            finally:
                cursor.close()
                connection.close()

    def rent_bike(self, bike_id):
        bike = self.find_bike(bike_id)

        if bike is not None and bike.available:
                customer_name = input("Enter customer name: ").strip()
                customer_phone = input("Enter customer phone number: ").strip()

                if not customer_name or not customer_phone:
                    print("Name and phone number cannot be empty.")
                    return

        if bike is None:
            print("Sorry, bike ID not found.")
        elif not bike.available:
            print("Sorry, this bike is already rented.")
        else:
            connection = get_connection()
            cursor = connection.cursor()

            try:
                cursor.execute(
                    "UPDATE bikes SET available = FALSE WHERE bike_id = %s",
                    (bike_id,)
                )

                cursor.execute(
                    """
                    INSERT INTO rentals (bike_id, customer_name, customer_phone)
                    VALUES (%s, %s, %s)
                    """,
                    (bike_id, customer_name, customer_phone)
                )

                connection.commit()
                bike.available = False

                print(f"{bike.name} has been rented successfully!")
                print("Rental history saved to PostgreSQL.")

            except Exception as error:
                connection.rollback()
                print("Could not complete rental:", error)
            finally:
                cursor.close()
                connection.close()


    def view_rental_history(self):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT rentals.rental_id,
                       bikes.name,
                       rentals.rented_at,
                       rentals.returned_at,
                       rentals.status,
                       rentals.total_cost,
                       rentals.customer_name,
                       rentals.customer_phone
                FROM rentals
                JOIN bikes ON rentals.bike_id = bikes.bike_id
                ORDER BY rentals.rental_id DESC
            """)

            records = cursor.fetchall()

            print("\n===== RENTAL HISTORY =====")

            if not records:
                print("No rental records found.")
            else:
                for record in records:
                    print(f"\nRental ID: {record[0]}")
                    print(f"Bike: {record[1]}")
                    print(f"Rented at: {record[2]}")
                    print(f"Returned at: {record[3]}")
                    print(f"Status: {record[4]}")

                    cost = record[5]
                    if cost is not None:
                        print(f"Total cost: ₹{cost}")
                    else:
                        print("Total cost: Not calculated yet")

                    print(f"Customer name: {record[6] or 'Not available'}")
                    print(f"Customer phone: {record[7] or 'Not available'}")
                    print("--------------------")

        except Exception as error:
            print("Could not load rental history:", error)

        finally:
            cursor.close()
            connection.close()



rental_system = RentalSystem()
rental_system.load_bikes()
while True:

    print("\n===== BIKE RENTAL SYSTEM =====")
    print("1. View available bikes")
    print("2. Rent a bike")
    print("3. Return a bike")
    print("4. View rental history")
    print("5. Exit")


    choice = input("Enter your choice: ")

    if choice == "1":
        rental_system.display_bikes()


    elif choice == "2":
        try:
            bike_id = int(input("Enter bike ID to rent: "))
            rental_system.rent_bike(bike_id)
        except ValueError:
            print("Invalid input! Please enter a numeric bike ID.")

    elif choice == "3":
        try:
            bike_id = int(input("Enter bike ID to return: "))
            rental_system.return_bike(bike_id)
        except ValueError:
            print("Invalid input! Please enter a numeric bike ID.")


    elif choice == "4":
        rental_system.view_rental_history()

    elif choice == "5":
        print("Thank you for using the Bike Rental System!")
        break


    else:
        print("Invalid choice. Please select 1, 2, 3, or 4.")
