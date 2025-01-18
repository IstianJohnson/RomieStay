# RomieStay a Hotel Booking System 
# Librarys for the program
from datetime import datetime, date, timedelta

# --- Intro Message ---
def intro():
    print("\nWelcome to RomieStay the Finest Hotel Booking System!\n")
    print("Your one-stop solution for hassle-free hotel bookings, exclusive discounts, and premium comfort.")
    print("\n-----------------------------------------------\n")

# --- About Us ---
def about_us():
    print("\n--- About Us ---")
    print("Welcome to RomieStay the Finest Hotel Booking System! 🌟")
    print("We are committed to revolutionizing your hotel booking experience with:")
    print("- A curated selection of top-rated hotels across the globe.")
    print("- Transparent pricing and exclusive discounts.")
    print("- A seamless and user-friendly booking process.")
    print("- 24/7 customer support to assist you every step of the way.")
    print("\nWhether you're traveling for business or leisure, we ensure that your stay is comfortable,")
    print("luxurious, and unforgettable experience you would ever had.")
    print("\n-----------------------------------------------\n")

# --- Holiday Management ---
holidays = {
    date(2025, 1, 26): "Republic Day",
    date(2025, 8, 15): "Independence Day",
    date(2025, 10, 2): "Gandhi Jayanti",
    date(2025, 11, 12): "Diwali",
    date(2025, 3, 17): "Holi"
}

# --- Hotels Data ---
hotels = {
    "Trinity Hotel": {"total_rooms": 100, "per_day_charge": 5000, "bookings": {}, "location": "Paris", "rating": "5-Star", "earnings": 0},
    "Grand Palace": {"total_rooms": 150, "per_day_charge": 800, "bookings": {}, "location": "New York", "rating": "4.5-Star", "earnings": 0},
    "Sunrise Inn": {"total_rooms": 100, "per_day_charge": 700, "bookings": {}, "location": "Tokyo", "rating": "3.5-Star", "earnings": 0},
    "Ocean View": {"total_rooms": 120, "per_day_charge": 600, "bookings": {}, "location": "Maldives", "rating": "4-Star", "earnings": 0},
    "Mountain Retreat": {"total_rooms": 50, "per_day_charge": 1200, "bookings": {}, "location": "Switzerland", "rating": "5-Star", "earnings": 0}
}

# --- User Management ---
users = {"admin": "admin"}  # Default admin user
user_bookings = {}  # Stores bookings per user

# --- Register User ---
def register(username, password):
    if username in users:
        return False
    users[username] = password
    user_bookings[username] = []
    return True

# --- Authenticate User ---
def authenticate(username, password):
    return username in users and users[username] == password

# --- Check for Holidays ---
def check_holiday(input_date):
    return input_date in holidays

# --- Display Bill ---
def display_bill(username, hotel_name, start_date, end_date, total_cost, discount_applied, rooms_booked):
    print("\n\n******** BILL ********")
    print("Customer Name:", username)
    print("Hotel Booked:", hotel_name)
    print("Location:", hotels[hotel_name]["location"])
    print("Check-in Date:", start_date)
    print("Check-out Date:", end_date)
    print("Rooms Booked:", rooms_booked)
    print("Total Cost:", total_cost, "INR")
    if discount_applied > 0:
        print("Discount Applied (10% for holidays):", discount_applied, "INR")
    print("\nThank you for booking with RomieStay!")
    print("*******************************\n")

# --- View My Bookings ---
def view_my_bookings(username):
    print("\n----- Your Bookings -----\n")
    if not user_bookings[username]:
        print("You have no bookings yet...\n")
        return

    total_cost = 0
    for a in range(len(user_bookings[username])):
        booking = user_bookings[username][a]
        print("Booking", a + 1)
        print("Hotel:", booking['hotel'])
        print("Location:", hotels[booking['hotel']]['location'])
        print("From:", booking['start_date'], "To:", booking['end_date'])
        print("Rooms:", booking['rooms'])
        print("Cost:", booking['total_cost'], "INR")
        print("-" * 40)
        total_cost += booking['total_cost']

    print("\nTotal Number of Bookings:", len(user_bookings[username]))
    print("Total Amount Spent:", total_cost, "INR\n")

# --- Book Room ---
def book_room(username):
    # Input dates
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    # Date format validation
    if not start_date or not end_date:
        print("Both start date and end date are required.")
        return

    # Convert string to date object
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format! Please use YYYY-MM-DD.")
        return

    # Validate date
    if start_date > end_date:
        print("End date cannot be before the start date!")
        return
    if start_date.year < 2025 or end_date.year > 2027:
        print("Bookings are only allowed between 2025 and 2027.")
        return

    # Display available hotels and rooms
    print("\nAvailable Hotels from", start_date, "to", end_date)
    hotel_list = list(hotels.items())
    available_hotels = []

    for i in range(len(hotel_list)):
        hotel, data = hotel_list[i]
        current_date = start_date
        available = True
        while current_date <= end_date:
            if data["bookings"].get(current_date, 0) >= data["total_rooms"]:
                available = False
                break
            current_date += timedelta(days=1)
        available_rooms = data["total_rooms"] - sum(data["bookings"].get(date_key, 0) for date_key in [start_date, end_date])
        if available:
            print(i + 1, ". Hotel Name:", hotel, "| Location:", data['location'], "| Per Room Charge:", data['per_day_charge'], "INR", "| Available Rooms:", available_rooms)
            available_hotels.append(hotel)
        else:
            print(i + 1, ". Hotel Name:", hotel, "| Location:", data['location'], "| No Rooms Available")

    if not available_hotels:
        print("No available hotels for the selected dates.")
        return

    hotel_choice = int(input("Enter the number of the hotel you want to book: "))
    if hotel_choice < 1 or hotel_choice > len(available_hotels):
        print("Invalid hotel choice!")
        return

    hotel_name = available_hotels[hotel_choice - 1]

    # Room selection
    num_rooms = int(input("Enter the number of rooms you want to book: "))
    total_cost = 0
    discount_applied = 0
    current_date = start_date

    while current_date <= end_date:
        if current_date not in hotels[hotel_name]["bookings"]:
            hotels[hotel_name]["bookings"][current_date] = 0
        hotels[hotel_name]["bookings"][current_date] += num_rooms
        daily_charge = hotels[hotel_name]["per_day_charge"] * num_rooms
        if check_holiday(current_date):
            discount = daily_charge * 0.10
            daily_charge -= discount
            discount_applied += discount
        total_cost += daily_charge
        current_date += timedelta(days=1)

    # Record booking
    user_bookings[username].append({
        "hotel": hotel_name,
        "start_date": start_date,
        "end_date": end_date,
        "total_cost": total_cost,
        "rooms": num_rooms
    })

    # Update earnings
    hotels[hotel_name]["earnings"] += total_cost

    display_bill(username, hotel_name, start_date, end_date, total_cost, discount_applied, num_rooms)

# --- Cancel Booking ---
def cancel_booking(username):
    if not user_bookings[username]:
        print("No bookings to cancel.")
        return

    print("Your Bookings:")
    for i in range(len(user_bookings[username])):
        booking = user_bookings[username][i]
        print(i + 1, ". Hotel:", booking['hotel'], "| From:", booking['start_date'], "| To:", booking['end_date'])

    try:
        choice = int(input("Enter the booking number to cancel: "))
        if choice < 1 or choice > len(user_bookings[username]):
            print("Invalid choice.")
            return
        booking = user_bookings[username].pop(choice - 1)

        # Update bookings
        current_date = booking["start_date"]
        while current_date <= booking["end_date"]:
            hotels[booking["hotel"]]["bookings"][current_date] -= booking["rooms"]
            current_date += timedelta(days=1)

        # Update earnings
        hotels[booking["hotel"]]["earnings"] -= booking["total_cost"]

        print("Booking canceled successfully!")

    except ValueError:
        print("Invalid input!")

# --- Viewing Panel ---
def view_hotels():
    print("\n----- Viewing Panel -----\n")
    hotel_list = list(hotels.items())
    for i in range(len(hotel_list)):
        hotel, data = hotel_list[i]
        print(i + 1, ". Hotel Name:", hotel, "| Location:", data['location'], "| Rating:", data['rating'], "| Per Room Charge:", data['per_day_charge'], "INR")
    print("\n-----------------------------------------------\n")

# --- Admin Panel ---
def admin_panel():
    print("\n----- Admin Panel -----\n")

    # Display hotel room status and earnings
    print("Hotel Room Status and Earnings:")
    hotel_list = list(hotels.items())
    for i in range(len(hotel_list)):
        hotel, data = hotel_list[i]
        print("\nHotel:", hotel, "| Location:", data["location"])
        print("Total Rooms:", data["total_rooms"])
        print("Earnings:", data["earnings"], "INR")
        print("Room Bookings:")
        total_bookings = 0

        # Display bookings for each date
        date_keys = sorted(data["bookings"].items())
        for j in range(len(date_keys)):
            date_key, count = date_keys[j]
            print("Date:", date_key, "- Rooms Booked:", count, "- Rooms Available:", data["total_rooms"] - count)
            total_bookings += count

        print("Total Rooms Booked:", total_bookings)
        print("-" * 40)

        # Display customer booking details for the hotel
        print("Customer Booking Details:")
        user_list = list(user_bookings.items())
        for k in range(len(user_list)):
            username, bookings = user_list[k]
            for l in range(len(bookings)):
                if bookings[l]["hotel"] == hotel:
                    print("Customer:", username, "| Booking:", l + 1)
                    print("From:", bookings[l]["start_date"], "| To:", bookings[l]["end_date"])
                    print("Rooms:", bookings[l]["rooms"], "| Total Cost:", bookings[l]["total_cost"], "INR")
                    print("-" * 40)

# --- Main Menu ---
intro()
while True:
    print("\n1. Login")
    print("2. Create Account")
    print("3. About Us")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")

        if authenticate(username, password):
            print("Welcome,", username)
            if username == "admin":
                admin_panel()
            else:
                while True:
                    print("\n1. View Hotels")
                    print("2. Book a Hotel Room")
                    print("3. Cancel a Booking")
                    print("4. View My Bookings")
                    print("5. Log Out")
                    user_choice = input("Enter your choice: ")
                    
                    if user_choice == "1":
                        view_hotels()
                    elif user_choice == "2":
                        book_room(username)
                    elif user_choice == "3":
                        cancel_booking(username)
                    elif user_choice == "4":
                        if user_bookings[username]:
                            for booking in user_bookings[username]:
                                print("Hotel:", booking["hotel"], "|", "From:", booking["start_date"], "To:", booking["end_date"], "|", "Total Cost:", booking["total_cost"], "|", "Rooms Booked:", booking["rooms"])
                        else:
                            print("No bookings found.")
                    elif user_choice == "5":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice.")

        else:
            print("Invalid credentials!")

    elif choice == "2":
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        if register(username, password):
            print("Account created successfully!")
        else:
            print("Username already exists.")

    elif choice == "3":
        about_us()
    elif choice == "4":
        print("Thank you for using the Hotel Booking System. Goodbye!")
        break

    else:
        print("Invalid choice.")


''' OUTPUT 

Welcome to RomieStay the Finest Hotel Booking System!

Your one-stop solution for hassle-free hotel bookings, exclusive discounts, and premium comfort.

-----------------------------------------------


1. Login
2. Create Account
3. About Us
4. Exit
Enter your choice: 3

--- About Us ---
Welcome to RomieStay the Finest Hotel Booking System! 🌟
We are committed to revolutionizing your hotel booking experience with:
- A curated selection of top-rated hotels across the globe.
- Transparent pricing and exclusive discounts.
- A seamless and user-friendly booking process.
- 24/7 customer support to assist you every step of the way.

Whether you're traveling for business or leisure, we ensure that your stay is comfortable,
luxurious, and unforgettable experience you would ever had.

-----------------------------------------------


1. Login
2. Create Account
3. About Us
4. Exit
Enter your choice: 1
Enter username: abc
Enter password: abc
Invalid credentials!

1. Login
2. Create Account
3. About Us
4. Exit
Enter your choice: 2
Enter a username: joseph
Enter a password: joseph
Account created successfully!

1. Login
2. Create Account
3. About Us
4. Exit
Enter your choice: 1
Enter username: joseph
Enter password: joseph
Welcome, joseph

1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 1

----- Viewing Panel -----

1 . Hotel Name: Trinity Hotel | Location: Paris | Rating: 5-Star | Per Room Charge: 5000 INR
2 . Hotel Name: Grand Palace | Location: New York | Rating: 4.5-Star | Per Room Charge: 800 INR
3 . Hotel Name: Sunrise Inn | Location: Tokyo | Rating: 3.5-Star | Per Room Charge: 700 INR
4 . Hotel Name: Ocean View | Location: Maldives | Rating: 4-Star | Per Room Charge: 600 INR
5 . Hotel Name: Mountain Retreat | Location: Switzerland | Rating: 5-Star | Per Room Charge: 1200 INR

-----------------------------------------------


1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 2
Enter the start date (YYYY-MM-DD): 2024-09-08
Enter the end date (YYYY-MM-DD): 2024-09-12
Bookings are only allowed between 2025 and 2027.

1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 2
Enter the start date (YYYY-MM-DD): 2025-08-15
Enter the end date (YYYY-MM-DD): 2025-08-20

Available Hotels from 2025-08-15 to 2025-08-20
1 . Hotel Name: Trinity Hotel | Location: Paris | Per Room Charge: 5000 INR | Available Rooms: 100
2 . Hotel Name: Grand Palace | Location: New York | Per Room Charge: 800 INR | Available Rooms: 150
3 . Hotel Name: Sunrise Inn | Location: Tokyo | Per Room Charge: 700 INR | Available Rooms: 100
4 . Hotel Name: Ocean View | Location: Maldives | Per Room Charge: 600 INR | Available Rooms: 120
5 . Hotel Name: Mountain Retreat | Location: Switzerland | Per Room Charge: 1200 INR | Available Rooms: 50
Enter the number of the hotel you want to book: 1
Enter the number of rooms you want to book: 5


******** BILL ********
Customer Name: joseph
Hotel Booked: Trinity Hotel
Location: Paris
Check-in Date: 2025-08-15
Check-out Date: 2025-08-20
Rooms Booked: 5
Total Cost: 147500.0 INR
Discount Applied (10% for holidays): 2500.0 INR

Thank you for booking with RomieStay!
*******************************


1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 2
Enter the start date (YYYY-MM-DD): 2025-08-15
Enter the end date (YYYY-MM-DD): 2024-08-21
End date cannot be before the start date!

1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 2
Enter the start date (YYYY-MM-DD): 2025-08-15
Enter the end date (YYYY-MM-DD): 2025-08-21

Available Hotels from 2025-08-15 to 2025-08-21
1 . Hotel Name: Trinity Hotel | Location: Paris | Per Room Charge: 5000 INR | Available Rooms: 95
2 . Hotel Name: Grand Palace | Location: New York | Per Room Charge: 800 INR | Available Rooms: 150
3 . Hotel Name: Sunrise Inn | Location: Tokyo | Per Room Charge: 700 INR | Available Rooms: 100
4 . Hotel Name: Ocean View | Location: Maldives | Per Room Charge: 600 INR | Available Rooms: 120
5 . Hotel Name: Mountain Retreat | Location: Switzerland | Per Room Charge: 1200 INR | Available Rooms: 50
Enter the number of the hotel you want to book: 3
Enter the number of rooms you want to book: 11


******** BILL ********
Customer Name: joseph
Hotel Booked: Sunrise Inn
Location: Tokyo
Check-in Date: 2025-08-15
Check-out Date: 2025-08-21
Rooms Booked: 11
Total Cost: 53130.0 INR
Discount Applied (10% for holidays): 770.0 INR

Thank you for booking with RomieStay!
*******************************


1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 4
Hotel: Trinity Hotel | From: 2025-08-15 To: 2025-08-20 | Total Cost: 147500.0 | Rooms Booked: 5
Hotel: Sunrise Inn | From: 2025-08-15 To: 2025-08-21 | Total Cost: 53130.0 | Rooms Booked: 11

1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 3
Your Bookings:
1 . Hotel: Trinity Hotel | From: 2025-08-15 | To: 2025-08-20
2 . Hotel: Sunrise Inn | From: 2025-08-15 | To: 2025-08-21
Enter the booking number to cancel: 1
Booking canceled successfully!

1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 5
Logging out...

1. Login
2. Create Account
3. About Us
4. Exit
Enter your choice: 2
Enter a username: marry
Enter a password: marry
Account created successfully!

1. Login
2. Create Account
3. About Us
4. Exit
Enter your choice: 1
Enter username: marry
Enter password: marry
Welcome, marry

1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 1

----- Viewing Panel -----

1 . Hotel Name: Trinity Hotel | Location: Paris | Rating: 5-Star | Per Room Charge: 5000 INR
2 . Hotel Name: Grand Palace | Location: New York | Rating: 4.5-Star | Per Room Charge: 800 INR
3 . Hotel Name: Sunrise Inn | Location: Tokyo | Rating: 3.5-Star | Per Room Charge: 700 INR
4 . Hotel Name: Ocean View | Location: Maldives | Rating: 4-Star | Per Room Charge: 600 INR
5 . Hotel Name: Mountain Retreat | Location: Switzerland | Rating: 5-Star | Per Room Charge: 1200 INR

-----------------------------------------------


1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 2
Enter the start date (YYYY-MM-DD): 2025-08-17
Enter the end date (YYYY-MM-DD): 2025-08-23

Available Hotels from 2025-08-17 to 2025-08-23
1 . Hotel Name: Trinity Hotel | Location: Paris | Per Room Charge: 5000 INR | Available Rooms: 100
2 . Hotel Name: Grand Palace | Location: New York | Per Room Charge: 800 INR | Available Rooms: 150
3 . Hotel Name: Sunrise Inn | Location: Tokyo | Per Room Charge: 700 INR | Available Rooms: 89
4 . Hotel Name: Ocean View | Location: Maldives | Per Room Charge: 600 INR | Available Rooms: 120
5 . Hotel Name: Mountain Retreat | Location: Switzerland | Per Room Charge: 1200 INR | Available Rooms: 50
Enter the number of the hotel you want to book: 4
Enter the number of rooms you want to book: 3


******** BILL ********
Customer Name: marry
Hotel Booked: Ocean View
Location: Maldives
Check-in Date: 2025-08-17
Check-out Date: 2025-08-23
Rooms Booked: 3
Total Cost: 12600 INR

Thank you for booking with RomieStay!
*******************************


1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 5
Logging out...

1. Login
2. Create Account
3. About Us
4. Exit
Enter your choice: 1
Enter username: joseph
Enter password: joseph
Welcome, joseph

1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 4
Hotel: Sunrise Inn | From: 2025-08-15 To: 2025-08-21 | Total Cost: 53130.0 | Rooms Booked: 11

1. View Hotels
2. Book a Hotel Room
3. Cancel a Booking
4. View My Bookings
5. Log Out
Enter your choice: 5
Logging out...

1. Login
2. Create Account
3. About Us
4. Exit
Enter your choice: admin
Invalid choice.

1. Login
2. Create Account
3. About Us
4. Exit
Enter your choice: 1
Enter username: admin
Enter password: admin
Welcome, admin

----- Admin Panel -----

Hotel Room Status and Earnings:

Hotel: Trinity Hotel | Location: Paris
Total Rooms: 100
Earnings: 0.0 INR
Room Bookings:
Date: 2025-08-15 - Rooms Booked: 0 - Rooms Available: 100
Date: 2025-08-16 - Rooms Booked: 0 - Rooms Available: 100
Date: 2025-08-17 - Rooms Booked: 0 - Rooms Available: 100
Date: 2025-08-18 - Rooms Booked: 0 - Rooms Available: 100
Date: 2025-08-19 - Rooms Booked: 0 - Rooms Available: 100
Date: 2025-08-20 - Rooms Booked: 0 - Rooms Available: 100
Total Rooms Booked: 0
----------------------------------------
Customer Booking Details:

Hotel: Grand Palace | Location: New York
Total Rooms: 150
Earnings: 0 INR
Room Bookings:
Total Rooms Booked: 0
----------------------------------------
Customer Booking Details:

Hotel: Sunrise Inn | Location: Tokyo
Total Rooms: 100
Earnings: 53130.0 INR
Room Bookings:
Date: 2025-08-15 - Rooms Booked: 11 - Rooms Available: 89
Date: 2025-08-16 - Rooms Booked: 11 - Rooms Available: 89
Date: 2025-08-17 - Rooms Booked: 11 - Rooms Available: 89
Date: 2025-08-18 - Rooms Booked: 11 - Rooms Available: 89
Date: 2025-08-19 - Rooms Booked: 11 - Rooms Available: 89
Date: 2025-08-20 - Rooms Booked: 11 - Rooms Available: 89
Date: 2025-08-21 - Rooms Booked: 11 - Rooms Available: 89
Total Rooms Booked: 77
----------------------------------------
Customer Booking Details:
Customer: joseph | Booking: 1
From: 2025-08-15 | To: 2025-08-21
Rooms: 11 | Total Cost: 53130.0 INR
----------------------------------------

Hotel: Ocean View | Location: Maldives
Total Rooms: 120
Earnings: 12600 INR
Room Bookings:
Date: 2025-08-17 - Rooms Booked: 3 - Rooms Available: 117
Date: 2025-08-18 - Rooms Booked: 3 - Rooms Available: 117
Date: 2025-08-19 - Rooms Booked: 3 - Rooms Available: 117
Date: 2025-08-20 - Rooms Booked: 3 - Rooms Available: 117
Date: 2025-08-21 - Rooms Booked: 3 - Rooms Available: 117
Date: 2025-08-22 - Rooms Booked: 3 - Rooms Available: 117
Date: 2025-08-23 - Rooms Booked: 3 - Rooms Available: 117
Total Rooms Booked: 21
----------------------------------------
Customer Booking Details:
Customer: marry | Booking: 1
From: 2025-08-17 | To: 2025-08-23
Rooms: 3 | Total Cost: 12600 INR
----------------------------------------

Hotel: Mountain Retreat | Location: Switzerland
Total Rooms: 50
Earnings: 0 INR
Room Bookings:
Total Rooms Booked: 0
----------------------------------------
Customer Booking Details:

1. Login
2. Create Account
3. About Us
4. Exit
Enter your choice: 4
Thank you for using the Hotel Booking System. Goodbye! '''
