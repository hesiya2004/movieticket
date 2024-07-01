import mysql.connector

db_host = 'localhost'
db_user = 'root'
db_password = '12345'
db_name = 'movieticket_booking'

try:
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    print("Connected to MySQL database")
except mysql.connector.Error as err:
    print(f"Error: {err}")

def create_movbookings_table():
    try:
        cursor = conn.cursor()
        create_table_query = """
        create table movbookings(id int auto_increment primary key,movie_name varchar(100) not NULL,show_time int(20) not NULL,total_seats int not NULL,total_cost decimal(10,2) not NULL); 
        """
        cursor.execute(create_table_query)
        print("Created 'movbookings' table in database.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

def book_ticket():
    print("Welcome to the movie ticket booking system.....\n")
    movies = {1: "Star", 2: "Pushpa 2", 3: "PT Sir", 4: "Joker"}
    show_time = {1: "10:00 AM", 2: "1:00 PM", 3: "4:00 PM", 4: "7:00 PM"}
    
    print("Available movies:")
    for key, value in movies.items():
        print(f"{key}. {value}")

    total_tickets = 0
    while True:
        movie_choice = int(input("\nEnter the number corresponding to the movie you want to book (0 to finish): "))
        if movie_choice == 0:
            break
        elif movie_choice not in movies:
            print("Invalid movie choice. Please choose again.")
            continue
        
        print(f"Movie selected: {movies[movie_choice]}")
        print("Available show times:")
        for key, value in show_time.items():
            print(f"{key}. {value}")
        
        show_time_choice = int(input("Enter the number corresponding to the show time: "))
        if show_time_choice not in show_time:
            print("Invalid show time choice. Please choose again.")
            continue
        
        total_seats = int(input(f"Enter the total number of seats you want to book: "))
        booking_system = MovieBookingSystem(total_seats, show_time[show_time_choice])

        if movie_choice == 1:
            total_cost = 150 * total_seats
        elif movie_choice == 2:
            total_cost = 130 * total_seats
        elif movie_choice == 3:
            total_cost = 170 * total_seats
        elif movie_choice == 4:
            total_cost = 200 * total_seats
        else:
            print("Invalid movie choice. Please choose again.")
            continue

        print(f"Total amount is: {total_cost} INR")
        
        print("\nBooking Summary:")
        print(f"Movie: {movies[movie_choice]}")
        print(f"Show Time: {show_time[show_time_choice]}")
        print(f"Total seats booked: {total_seats}")
        result = booking_system.book_seat(total_seats)
        print(result)
        print(f"Total cost for {total_seats} seat(s) is Rs. {total_cost}")

        
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO movbookings (movie_name, show_time, total_seats, total_cost) VALUES (%s, %s, %s, %s)"
            values = (movies[movie_choice], show_time[show_time_choice], total_seats, total_cost)
            cursor.execute(sql, values)
            conn.commit()
            print("Booking details recorded in database.")
        except mysql.connector.Error as err:
            print(f"Error inserting into MySQL table: {err}")
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

        total_tickets += total_seats

    conn.close()
    print(f"\nTotal tickets booked: {total_tickets}")

class MovieBookingSystem:
    def __init__(self, total_seats, show_time):
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.booked_seats = []
        self.show_time = show_time

    def check_available_seats(self):
        return self.available_seats

    def book_seat(self, seats_to_book):
        if seats_to_book > self.available_seats:
            return "Sorry... seats are not available"
        for _ in range(seats_to_book):
            self.booked_seats.append('x')
            self.available_seats -= 1
        return f"{seats_to_book} seat(s) booked successfully."

    def cancel_booking(self, seats_to_cancel):
        cancelled_seats = 0
        for _ in range(seats_to_cancel):
            if self.booked_seats:
                self.booked_seats.pop()
                self.available_seats += 1
                cancelled_seats += 1
            else:
                break
        return f"{cancelled_seats} seat(s) cancelled."


create_movbookings_table()

book_ticket()
