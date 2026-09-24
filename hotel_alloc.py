import random
import time
import json
from datetime import datetime


# =========================================================
# CUSTOMER CLASS
# =========================================================

class Customer:

    def __init__(self, name, age, phone):
        self.name = name
        self.age = age
        self.phone = phone

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "phone": self.phone
        }


# =========================================================
# ROOM CLASS
# =========================================================

class Room:

    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.status = "Available"

    def to_dict(self):
        return {
            "room_number": self.room_number,
            "room_type": self.room_type,
            "price": self.price,
            "status": self.status
        }


# =========================================================
# RESERVATION CLASS
# =========================================================

class Reservation:

    def __init__(
        self,
        booking_id,
        customer,
        room_number,
        room_type,
        price,
        days
    ):

        self.booking_id = booking_id
        self.customer = customer
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.days = days

        self.status = "Reserved"

        self.reservation_time = time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.check_in_time = None
        self.check_out_time = None

    def to_dict(self):

        return {
            "booking_id": self.booking_id,

            "customer": self.customer.to_dict(),

            "room_number": self.room_number,

            "room_type": self.room_type,

            "price": self.price,

            "days": self.days,

            "status": self.status,

            "reservation_time": self.reservation_time,

            "check_in_time": self.check_in_time,

            "check_out_time": self.check_out_time
        }


# =========================================================
# HOTEL CLASS
# =========================================================

class Hotel:

    def __init__(self):

        self.rooms = []

        self.reservations = {}

        self.customers = []

        self.booking_history = []

        self.filename = "hotel_data.json"

        self.create_rooms()

        self.load_data()

    # -----------------------------------------------------
    # CREATE ROOMS
    # -----------------------------------------------------

    def create_rooms(self):

        # Single rooms
        for number in range(101, 106):

            self.rooms.append(
                Room(
                    number,
                    "Single",
                    1500
                )
            )

        # Double rooms
        for number in range(201, 206):

            self.rooms.append(
                Room(
                    number,
                    "Double",
                    2500
                )
            )

        # Deluxe rooms
        for number in range(301, 306):

            self.rooms.append(
                Room(
                    number,
                    "Deluxe",
                    4000
                )
            )

        # Suite rooms
        for number in range(401, 406):

            self.rooms.append(
                Room(
                    number,
                    "Suite",
                    6000
                )
            )

    # -----------------------------------------------------
    # GENERATE BOOKING ID
    # -----------------------------------------------------

    def generate_booking_id(self):

        while True:

            booking_id = "HTL" + str(
                random.randint(
                    100000,
                    999999
                )
            )

            if booking_id not in self.reservations:

                return booking_id

    # -----------------------------------------------------
    # FIND AVAILABLE ROOM
    # -----------------------------------------------------

    def find_available_room(self, room_type):

        for room in self.rooms:

            if (
                room.room_type == room_type
                and room.status == "Available"
            ):

                return room

        return None

    # -----------------------------------------------------
    # ADD CUSTOMER
    # -----------------------------------------------------

    def add_customer(self):

        print("\n========== ADD CUSTOMER ==========")

        name = input(
            "Enter customer name: "
        ).strip()

        if not name:

            print("Invalid name.")

            return

        try:

            age = int(
                input("Enter age: ")
            )

            if age <= 0:

                print("Invalid age.")

                return

        except ValueError:

            print("Age must be a number.")

            return

        phone = input(
            "Enter phone number: "
        ).strip()

        if not phone.isdigit():

            print("Invalid phone number.")

            return

        customer = Customer(
            name,
            age,
            phone
        )

        self.customers.append(customer)

        self.save_data()

        print("\nCustomer added successfully.")

    # -----------------------------------------------------
    # BOOK ROOM
    # -----------------------------------------------------

    def book_room(self):

        print("\n========== BOOK ROOM ==========")

        name = input(
            "Enter customer name: "
        ).strip()

        if not name:

            print("Invalid name.")

            return

        # Check if customer already exists
        customer = None

        for existing_customer in self.customers:

            if existing_customer.name.lower() == name.lower():

                customer = existing_customer

                break

        # If customer does not exist
        if customer is None:

            print("\nCustomer not found.")
            print("Please enter customer details.")

            try:

                age = int(
                    input("Enter age: ")
                )

                if age <= 0:

                    print("Invalid age.")

                    return

            except ValueError:

                print("Invalid age.")

                return

            phone = input(
                "Enter phone number: "
            ).strip()

            if not phone.isdigit():

                print("Invalid phone number.")

                return

            customer = Customer(
                name,
                age,
                phone
            )

            self.customers.append(customer)

        print("\nRoom Types")

        print("1. Single")
        print("2. Double")
        print("3. Deluxe")
        print("4. Suite")

        choice = input(
            "Enter room type: "
        )

        room_types = {

            "1": "Single",
            "2": "Double",
            "3": "Deluxe",
            "4": "Suite"

        }

        if choice not in room_types:

            print("Invalid room type.")

            return

        room_type = room_types[choice]

        try:

            days = int(
                input(
                    "Enter number of days: "
                )
            )

            if days <= 0:

                print("Invalid number of days.")

                return

        except ValueError:

            print("Days must be a number.")

            return

        # Find room
        room = self.find_available_room(
            room_type
        )

        if room is None:

            print(
                "\nNo available",
                room_type,
                "rooms."
            )

            return

        booking_id = self.generate_booking_id()

        reservation = Reservation(

            booking_id,

            customer,

            room.room_number,

            room.room_type,

            room.price,

            days
        )

        # Mark room as reserved
        room.status = "Reserved"

        self.reservations[
            booking_id
        ] = reservation

        self.save_data()

        print("\n***** BOOKING SUCCESSFUL *****")

        print(
            "Booking ID:",
            booking_id
        )

        print(
            "Customer:",
            customer.name
        )

        print(
            "Room:",
            room.room_number
        )

        print(
            "Room Type:",
            room.room_type
        )

        print(
            "Price per day: ₹",
            room.price
        )

        print(
            "Number of days:",
            days
        )

    # -----------------------------------------------------
    # CALCULATE BILL
    # -----------------------------------------------------

    def calculate_bill(self, reservation):

        base_amount = (
            reservation.price
            * reservation.days
        )

        # Weekend charge
        weekend_charge = 0

        if reservation.days >= 2:

            weekend_charge = (
                base_amount * 0.10
            )

        # Long stay discount
        discount = 0

        if reservation.days > 5:

            discount = (
                base_amount * 0.15
            )

        total = (
            base_amount
            + weekend_charge
            - discount
        )

        return (
            base_amount,
            weekend_charge,
            discount,
            total
        )

    # -----------------------------------------------------
    # CHECK IN
    # -----------------------------------------------------

    def check_in(self):

        print("\n========== CHECK IN ==========")

        booking_id = input(
            "Enter booking ID: "
        ).strip()

        if booking_id not in self.reservations:

            print("Booking not found.")

            return

        reservation = self.reservations[
            booking_id
        ]

        if reservation.status != "Reserved":

            print(
                "This booking cannot be checked in."
            )

            return

        reservation.status = "Checked-In"

        reservation.check_in_time = (
            time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        # Update room status
        for room in self.rooms:

            if (
                room.room_number
                == reservation.room_number
            ):

                room.status = "Checked-In"

                break

        self.save_data()

        print(
            "\nCustomer",
            reservation.customer.name,
            "checked in successfully."
        )

        print(
            "Room:",
            reservation.room_number
        )

        print(
            "Check-in time:",
            reservation.check_in_time
        )

    # -----------------------------------------------------
    # CHECK OUT
    # -----------------------------------------------------

    def check_out(self):

        print("\n========== CHECK OUT ==========")

        booking_id = input(
            "Enter booking ID: "
        ).strip()

        if booking_id not in self.reservations:

            print("Booking not found.")

            return

        reservation = self.reservations[
            booking_id
        ]

        if reservation.status != "Checked-In":

            print(
                "Customer has not checked in."
            )

            return

        reservation.status = "Checked-Out"

        reservation.check_out_time = (
            time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        (
            base_amount,
            weekend_charge,
            discount,
            total
        ) = self.calculate_bill(
            reservation
        )

        # Late checkout option
        late_choice = input(
            "Was the checkout late? (y/n): "
        ).lower()

        late_charge = 0

        if late_choice == "y":

            late_charge = 500

            total += late_charge

        # Free room
        for room in self.rooms:

            if (
                room.room_number
                == reservation.room_number
            ):

                room.status = "Available"

                break

        # Add to booking history
        self.booking_history.append(
            reservation.to_dict()
        )

        self.save_data()

        print("\n========== FINAL BILL ==========")

        print(
            "Customer:",
            reservation.customer.name
        )

        print(
            "Room:",
            reservation.room_number
        )

        print(
            "Base amount: ₹",
            base_amount
        )

        print(
            "Weekend charge: ₹",
            weekend_charge
        )

        print(
            "Long-stay discount: ₹",
            discount
        )

        print(
            "Late checkout charge: ₹",
            late_charge
        )

        print(
            "------------------------------"
        )

        print(
            "TOTAL BILL: ₹",
            total
        )

        print(
            "\nCheckout completed."
        )

    # -----------------------------------------------------
    # CANCEL RESERVATION
    # -----------------------------------------------------

    def cancel_reservation(self):

        print("\n========== CANCEL BOOKING ==========")

        booking_id = input(
            "Enter booking ID: "
        ).strip()

        if booking_id not in self.reservations:

            print("Booking not found.")

            return

        reservation = self.reservations[
            booking_id
        ]

        if reservation.status != "Reserved":

            print(
                "Only reserved bookings can be cancelled."
            )

            return

        (
            base_amount,
            weekend_charge,
            discount,
            total
        ) = self.calculate_bill(
            reservation
        )

        # Cancellation charge
        cancellation_charge = (
            total * 0.10
        )

        refund = (
            total
            - cancellation_charge
        )

        # Free room
        for room in self.rooms:

            if (
                room.room_number
                == reservation.room_number
            ):

                room.status = "Available"

                break

        reservation.status = "Cancelled"

        self.booking_history.append(
            reservation.to_dict()
        )

        del self.reservations[
            booking_id
        ]

        self.save_data()

        print(
            "\nBooking cancelled successfully."
        )

        print(
            "Cancellation charge: ₹",
            cancellation_charge
        )

        print(
            "Refund amount: ₹",
            refund
        )

    # -----------------------------------------------------
    # SEARCH BOOKING
    # -----------------------------------------------------

    def search_booking(self):

        print("\n========== SEARCH BOOKING ==========")

        booking_id = input(
            "Enter booking ID: "
        ).strip()

        if booking_id not in self.reservations:

            print("Booking not found.")

            return

        reservation = self.reservations[
            booking_id
        ]

        print("\nBooking Details")

        print(
            "Booking ID:",
            reservation.booking_id
        )

        print(
            "Customer:",
            reservation.customer.name
        )

        print(
            "Room:",
            reservation.room_number
        )

        print(
            "Room Type:",
            reservation.room_type
        )

        print(
            "Days:",
            reservation.days
        )

        print(
            "Price per day: ₹",
            reservation.price
        )

        print(
            "Status:",
            reservation.status
        )

        print(
            "Reservation Time:",
            reservation.reservation_time
        )

    # -----------------------------------------------------
    # ROOM AVAILABILITY
    # -----------------------------------------------------

    def room_availability(self):

        print("\n========== ROOM AVAILABILITY ==========")

        room_types = [
            "Single",
            "Double",
            "Deluxe",
            "Suite"
        ]

        for room_type in room_types:

            available = 0
            total = 0

            for room in self.rooms:

                if room.room_type == room_type:

                    total += 1

                    if room.status == "Available":

                        available += 1

            print(
                f"{room_type}: "
                f"{available}/{total} available"
            )

    # -----------------------------------------------------
    # BOOKING HISTORY
    # -----------------------------------------------------

    def view_booking_history(self):

        print("\n========== BOOKING HISTORY ==========")

        if not self.booking_history:

            print("No booking history.")

            return

        for booking in self.booking_history:

            print(
                "\nBooking ID:",
                booking["booking_id"]
            )

            print(
                "Customer:",
                booking["customer"]["name"]
            )

            print(
                "Room:",
                booking["room_number"]
            )

            print(
                "Room Type:",
                booking["room_type"]
            )

            print(
                "Status:",
                booking["status"]
            )

    # -----------------------------------------------------
    # SAVE DATA
    # -----------------------------------------------------

    def save_data(self):

        data = {

            "customers": [
                customer.to_dict()
                for customer in self.customers
            ],

            "rooms": [
                room.to_dict()
                for room in self.rooms
            ],

            "reservations": {
                booking_id:
                reservation.to_dict()

                for booking_id, reservation
                in self.reservations.items()
            },

            "booking_history":
                self.booking_history
        }

        with open(
            self.filename,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------

    def load_data(self):

        try:

            with open(
                self.filename,
                "r"
            ) as file:

                data = json.load(file)

            # Load customers
            self.customers = []

            for customer_data in data.get(
                "customers",
                []
            ):

                customer = Customer(

                    customer_data["name"],

                    customer_data["age"],

                    customer_data["phone"]
                )

                self.customers.append(
                    customer
                )

            # Load room status
            saved_rooms = data.get(
                "rooms",
                []
            )

            for saved_room in saved_rooms:

                for room in self.rooms:

                    if (
                        room.room_number
                        == saved_room["room_number"]
                    ):

                        room.status = (
                            saved_room["status"]
                        )

                        break

            # Load reservations
            self.reservations = {}

            for booking_id, reservation_data \
                    in data.get(
                        "reservations",
                        {}
                    ).items():

                customer_data = (
                    reservation_data["customer"]
                )

                customer = Customer(

                    customer_data["name"],

                    customer_data["age"],

                    customer_data["phone"]
                )

                reservation = Reservation(

                    reservation_data[
                        "booking_id"
                    ],

                    customer,

                    reservation_data[
                        "room_number"
                    ],

                    reservation_data[
                        "room_type"
                    ],

                    reservation_data[
                        "price"
                    ],

                    reservation_data[
                        "days"
                    ]
                )

                reservation.status = (
                    reservation_data["status"]
                )

                reservation.reservation_time = (
                    reservation_data[
                        "reservation_time"
                    ]
                )

                reservation.check_in_time = (
                    reservation_data[
                        "check_in_time"
                    ]
                )

                reservation.check_out_time = (
                    reservation_data[
                        "check_out_time"
                    ]
                )

                self.reservations[
                    booking_id
                ] = reservation

            self.booking_history = data.get(
                "booking_history",
                []
            )

        except FileNotFoundError:

            print(
                "No previous hotel data found."
            )

        except json.JSONDecodeError:

            print(
                "Hotel data file is corrupted."
            )


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    hotel = Hotel()

    while True:

        print("\n")
        print("=" * 50)

        print(
            "       SMART HOTEL RESERVATION SYSTEM"
        )

        print("=" * 50)

        print("1. Add Customer")
        print("2. Book Room")
        print("3. Cancel Booking")
        print("4. Check In")
        print("5. Check Out")
        print("6. Search Booking")
        print("7. View Booking History")
        print("8. View Room Availability")
        print("9. Exit")

        choice = input(
            "\nEnter your choice: "
        )

        if choice == "1":

            hotel.add_customer()

        elif choice == "2":

            hotel.book_room()

        elif choice == "3":

            hotel.cancel_reservation()

        elif choice == "4":

            hotel.check_in()

        elif choice == "5":

            hotel.check_out()

        elif choice == "6":

            hotel.search_booking()

        elif choice == "7":

            hotel.view_booking_history()

        elif choice == "8":

            hotel.room_availability()

        elif choice == "9":

            print(
                "\nThank you for using "
                "Smart Hotel Reservation System!"
            )

            break

        else:

            print(
                "Invalid choice. "
                "Please select 1-9."
            )


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":
    main()