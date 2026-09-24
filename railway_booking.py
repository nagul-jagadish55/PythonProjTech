import random
import time
import json


# =========================================================
# PASSENGER CLASS
# =========================================================

class Passenger:

    def __init__(self, name, age, phone, passenger_type):
        self.name = name
        self.age = age
        self.phone = phone
        self.passenger_type = passenger_type


# =========================================================
# TRAIN CLASS
# =========================================================

class Train:

    def __init__(self, train_number, train_name):

        self.train_number = train_number
        self.train_name = train_name

        # Dictionary:
        # seat number -> current status
        self.seats = {}

        # Create 5 seats for each travel class
        for travel_class in [
            "Sleeper",
            "AC 3-Tier",
            "AC 2-Tier",
            "First Class"
        ]:

            for i in range(1, 6):

                seat_number = f"{travel_class}-{i}"

                self.seats[seat_number] = "Available"


# =========================================================
# TICKET CLASS
# =========================================================

class Ticket:

    def __init__(
        self,
        pnr,
        passenger,
        train_number,
        travel_class,
        seat_number,
        fare
    ):

        self.pnr = pnr
        self.passenger = passenger
        self.train_number = train_number
        self.travel_class = travel_class
        self.seat_number = seat_number
        self.fare = fare

        self.booking_time = time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.status = "Confirmed"

    def to_dict(self):

        return {
            "pnr": self.pnr,

            "passenger": {
                "name": self.passenger.name,
                "age": self.passenger.age,
                "phone": self.passenger.phone,
                "passenger_type":
                    self.passenger.passenger_type
            },

            "train_number": self.train_number,
            "travel_class": self.travel_class,
            "seat_number": self.seat_number,
            "fare": self.fare,
            "booking_time": self.booking_time,
            "status": self.status
        }


# =========================================================
# RESERVATION SYSTEM CLASS
# =========================================================

class ReservationSystem:

    def __init__(self):

        self.train = Train(
            "12601",
            "Chennai Express"
        )

        # Confirmed tickets
        self.tickets = {}

        # Cancelled tickets
        self.cancelled_tickets = {}

        # Waiting list
        self.waiting_list = []

        # Data file
        self.filename = "railway_data.json"

        self.load_data()

    # =====================================================
    # PNR GENERATION
    # =====================================================

    def generate_pnr(self):

        while True:

            pnr = str(
                random.randint(
                    1000000000,
                    9999999999
                )
            )

            if pnr not in self.tickets:

                return pnr

    # =====================================================
    # FARE CALCULATION
    # =====================================================

    def calculate_fare(
        self,
        travel_class,
        passenger_type
    ):

        fares = {
            "Sleeper": 500,
            "AC 3-Tier": 1000,
            "AC 2-Tier": 1500,
            "First Class": 2000
        }

        fare = fares[travel_class]

        if passenger_type == "Child":

            fare = fare * 0.5

        elif passenger_type == "Senior":

            fare = fare * 0.7

        return fare

    # =====================================================
    # FIND AVAILABLE SEAT
    # =====================================================

    def find_available_seat(self, travel_class):

        for seat, status in self.train.seats.items():

            if (
                seat.startswith(travel_class)
                and status == "Available"
            ):

                return seat

        return None

    # =====================================================
    # BOOK TICKET
    # =====================================================

    def book_ticket(self):

        print("\n========== BOOK TICKET ==========")

        name = input(
            "Enter passenger name: "
        ).strip()

        if not name:

            print("Invalid name.")

            return

        # Prevent duplicate active booking
        for ticket in self.tickets.values():

            if (
                ticket.passenger.name.lower()
                == name.lower()
            ):

                print(
                    "This passenger already has "
                    "an active booking."
                )

                return

        # Age
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

        # Phone
        phone = input(
            "Enter phone number: "
        ).strip()

        if not phone.isdigit():

            print("Invalid phone number.")

            return

        # Passenger type
        print("\nPassenger Type")

        print("1. Adult")
        print("2. Child")
        print("3. Senior")

        type_choice = input(
            "Enter choice: "
        )

        passenger_types = {
            "1": "Adult",
            "2": "Child",
            "3": "Senior"
        }

        if type_choice not in passenger_types:

            print("Invalid passenger type.")

            return

        passenger_type = passenger_types[
            type_choice
        ]

        # Travel class
        print("\nTravel Classes")

        print("1. Sleeper")
        print("2. AC 3-Tier")
        print("3. AC 2-Tier")
        print("4. First Class")

        class_choice = input(
            "Enter choice: "
        )

        classes = {
            "1": "Sleeper",
            "2": "AC 3-Tier",
            "3": "AC 2-Tier",
            "4": "First Class"
        }

        if class_choice not in classes:

            print("Invalid travel class.")

            return

        travel_class = classes[
            class_choice
        ]

        passenger = Passenger(
            name,
            age,
            phone,
            passenger_type
        )

        # Find seat
        seat = self.find_available_seat(
            travel_class
        )

        # =================================================
        # CONFIRMED BOOKING
        # =================================================

        if seat:

            pnr = self.generate_pnr()

            fare = self.calculate_fare(
                travel_class,
                passenger_type
            )

            self.train.seats[seat] = pnr

            ticket = Ticket(
                pnr,
                passenger,
                self.train.train_number,
                travel_class,
                seat,
                fare
            )

            self.tickets[pnr] = ticket

            self.save_data()

            print("\n***** BOOKING SUCCESSFUL *****")

            print("PNR:", pnr)
            print("Passenger:", name)
            print("Train:", self.train.train_name)
            print("Class:", travel_class)
            print("Seat:", seat)
            print("Fare: ₹", fare)
            print("Status: Confirmed")

        # =================================================
        # WAITING LIST
        # =================================================

        else:

            print(
                "\nNo seats available in",
                travel_class
            )

            choice = input(
                "Do you want to join the "
                "waiting list? (y/n): "
            ).lower()

            if choice != "y":

                print("Booking cancelled.")

                return

            waiting_id = self.generate_pnr()

            waiting_data = {

                "waiting_id": waiting_id,

                "passenger": {

                    "name": name,
                    "age": age,
                    "phone": phone,
                    "passenger_type": passenger_type
                },

                "train_number":
                    self.train.train_number,

                "travel_class":
                    travel_class,

                "request_time":
                    time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
            }

            self.waiting_list.append(
                waiting_data
            )

            self.save_data()

            print(
                "\nAdded to waiting list."
            )

            print(
                "Waiting ID:",
                waiting_id
            )

            print(
                "Position:",
                len(self.waiting_list)
            )

    # =====================================================
    # CANCEL TICKET
    # =====================================================

    def cancel_ticket(self):

        print("\n========== CANCEL TICKET ==========")

        pnr = input(
            "Enter PNR: "
        ).strip()

        if pnr not in self.tickets:

            print("Invalid PNR.")

            return

        ticket = self.tickets[pnr]

        print(
            "\nPassenger:",
            ticket.passenger.name
        )

        print(
            "Seat:",
            ticket.seat_number
        )

        print(
            "Fare:",
            ticket.fare
        )

        confirm = input(
            "Are you sure you want to cancel? (y/n): "
        ).lower()

        if confirm != "y":

            print("Cancellation aborted.")

            return

        # 20% cancellation charge
        cancellation_charge = (
            ticket.fare * 0.20
        )

        refund = (
            ticket.fare
            - cancellation_charge
        )

        # Free the seat
        self.train.seats[
            ticket.seat_number
        ] = "Available"

        ticket.status = "Cancelled"

        self.cancelled_tickets[pnr] = (
            ticket.to_dict()
        )

        del self.tickets[pnr]

        print(
            "\nTicket cancelled successfully."
        )

        print(
            "Cancellation charge: ₹",
            cancellation_charge
        )

        print(
            "Refund amount: ₹",
            refund
        )

        # Promote waiting passenger
        self.promote_waiting_passenger(
            ticket.travel_class,
            ticket.seat_number
        )

        self.save_data()

    # =====================================================
    # WAITING LIST PROMOTION
    # =====================================================

    def promote_waiting_passenger(
        self,
        travel_class,
        seat_number
    ):

        for index, waiting in enumerate(
            self.waiting_list
        ):

            if (
                waiting["travel_class"]
                == travel_class
            ):

                passenger_data = (
                    waiting["passenger"]
                )

                passenger = Passenger(
                    passenger_data["name"],
                    passenger_data["age"],
                    passenger_data["phone"],
                    passenger_data[
                        "passenger_type"
                    ]
                )

                pnr = self.generate_pnr()

                fare = self.calculate_fare(
                    travel_class,
                    passenger.passenger_type
                )

                ticket = Ticket(
                    pnr,
                    passenger,
                    self.train.train_number,
                    travel_class,
                    seat_number,
                    fare
                )

                self.tickets[pnr] = ticket

                self.train.seats[
                    seat_number
                ] = pnr

                del self.waiting_list[index]

                print(
                    "\n***** WAITING LIST PROMOTION *****"
                )

                print(
                    passenger.name,
                    "has been promoted "
                    "to confirmed booking."
                )

                print(
                    "New PNR:",
                    pnr
                )

                print(
                    "Seat:",
                    seat_number
                )

                return

    # =====================================================
    # SEARCH BY PNR
    # =====================================================

    def search_pnr(self):

        print("\n========== SEARCH PNR ==========")

        pnr = input(
            "Enter PNR: "
        ).strip()

        if pnr in self.tickets:

            ticket = self.tickets[pnr]

            print("\nPNR:", ticket.pnr)
            print(
                "Passenger:",
                ticket.passenger.name
            )
            print(
                "Train:",
                ticket.train_number
            )
            print(
                "Class:",
                ticket.travel_class
            )
            print(
                "Seat:",
                ticket.seat_number
            )
            print(
                "Fare:",
                ticket.fare
            )
            print(
                "Booking Time:",
                ticket.booking_time
            )
            print(
                "Status:",
                ticket.status
            )

        elif pnr in self.cancelled_tickets:

            print(
                "This ticket has been cancelled."
            )

        else:

            print("PNR not found.")

    # =====================================================
    # SEARCH PASSENGER
    # =====================================================

    def search_passenger(self):

        print(
            "\n========== PASSENGER SEARCH =========="
        )

        name = input(
            "Enter passenger name: "
        ).strip()

        found = False

        for ticket in self.tickets.values():

            if (
                ticket.passenger.name.lower()
                == name.lower()
            ):

                print(
                    "\nPassenger:",
                    ticket.passenger.name
                )

                print(
                    "PNR:",
                    ticket.pnr
                )

                print(
                    "Class:",
                    ticket.travel_class
                )

                print(
                    "Seat:",
                    ticket.seat_number
                )

                print(
                    "Fare:",
                    ticket.fare
                )

                found = True

        if not found:

            print("Passenger not found.")

    # =====================================================
    # SEAT AVAILABILITY
    # =====================================================

    def seat_availability(self):

        print(
            "\n========== SEAT AVAILABILITY =========="
        )

        classes = [
            "Sleeper",
            "AC 3-Tier",
            "AC 2-Tier",
            "First Class"
        ]

        for travel_class in classes:

            total = 0
            available = 0

            for seat, status in (
                self.train.seats.items()
            ):

                if seat.startswith(
                    travel_class
                ):

                    total += 1

                    if status == "Available":

                        available += 1

            print(
                f"{travel_class}: "
                f"{available}/{total} seats available"
            )

    # =====================================================
    # DISPLAY WAITING LIST
    # =====================================================

    def display_waiting_list(self):

        print(
            "\n========== WAITING LIST =========="
        )

        if len(self.waiting_list) == 0:

            print(
                "Waiting list is empty."
            )

            return

        for position, waiting in enumerate(
            self.waiting_list,
            start=1
        ):

            passenger = waiting[
                "passenger"
            ]

            print(
                f"{position}. "
                f"{passenger['name']} - "
                f"{waiting['travel_class']}"
            )

    # =====================================================
    # DISPLAY CONFIRMED BOOKINGS
    # =====================================================

    def display_bookings(self):

        print(
            "\n========== CONFIRMED BOOKINGS =========="
        )

        if len(self.tickets) == 0:

            print(
                "No confirmed bookings."
            )

            return

        for ticket in self.tickets.values():

            print(
                "PNR:",
                ticket.pnr,
                "| Passenger:",
                ticket.passenger.name,
                "| Class:",
                ticket.travel_class,
                "| Seat:",
                ticket.seat_number
            )

    # =====================================================
    # SAVE DATA
    # =====================================================

    def save_data(self):

        data = {

            "tickets": {

                pnr: ticket.to_dict()

                for pnr, ticket
                in self.tickets.items()
            },

            "cancelled_tickets":
                self.cancelled_tickets,

            "waiting_list":
                self.waiting_list,

            "seats":
                self.train.seats
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

    # =====================================================
    # LOAD DATA
    # =====================================================

    def load_data(self):

        try:

            with open(
                self.filename,
                "r"
            ) as file:

                data = json.load(file)

            self.cancelled_tickets = (
                data.get(
                    "cancelled_tickets",
                    {}
                )
            )

            self.waiting_list = (
                data.get(
                    "waiting_list",
                    []
                )
            )

            saved_seats = data.get(
                "seats",
                {}
            )

            for seat, status in (
                saved_seats.items()
            ):

                if seat in self.train.seats:

                    self.train.seats[
                        seat
                    ] = status

            saved_tickets = data.get(
                "tickets",
                {}
            )

            for pnr, ticket_data in (
                saved_tickets.items()
            ):

                passenger_data = (
                    ticket_data["passenger"]
                )

                passenger = Passenger(
                    passenger_data["name"],
                    passenger_data["age"],
                    passenger_data["phone"],
                    passenger_data[
                        "passenger_type"
                    ]
                )

                ticket = Ticket(
                    ticket_data["pnr"],
                    passenger,
                    ticket_data["train_number"],
                    ticket_data["travel_class"],
                    ticket_data["seat_number"],
                    ticket_data["fare"]
                )

                ticket.booking_time = (
                    ticket_data[
                        "booking_time"
                    ]
                )

                ticket.status = (
                    ticket_data["status"]
                )

                self.tickets[pnr] = ticket

        except FileNotFoundError:

            print(
                "No previous booking data found."
            )

        except json.JSONDecodeError:

            print(
                "Booking file is empty "
                "or corrupted."
            )


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    system = ReservationSystem()

    while True:

        print("\n")
        print("=" * 45)

        print(
            "     RAILWAY TICKET RESERVATION SYSTEM"
        )

        print("=" * 45)

        print("1. Book Ticket")
        print("2. Cancel Ticket")
        print("3. Search by PNR")
        print("4. Search Passenger")
        print("5. Check Seat Availability")
        print("6. Display Waiting List")
        print("7. Display Confirmed Bookings")
        print("8. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            system.book_ticket()

        elif choice == "2":

            system.cancel_ticket()

        elif choice == "3":

            system.search_pnr()

        elif choice == "4":

            system.search_passenger()

        elif choice == "5":

            system.seat_availability()

        elif choice == "6":

            system.display_waiting_list()

        elif choice == "7":

            system.display_bookings()

        elif choice == "8":

            print(
                "\nThank you for using "
                "the Railway Reservation System."
            )

            break

        else:

            print(
                "Invalid menu choice. "
                "Please try again."
            )


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    main()