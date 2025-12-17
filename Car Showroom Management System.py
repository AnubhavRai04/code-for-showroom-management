#modules

import mysql.connector as mc

#database and tables

mydb = mc.connect(host="localhost",user='root',password=" ")

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS Showroom")

mycursor.execute("USE Showroom")

mycursor.execute("CREATE TABLE IF NOT EXISTS Admin (username VARCHAR(20) NOT NULL PRIMARY KEY, password VARCHAR(15) NOT NULL)")

mycursor.execute("CREATE TABLE IF NOT EXISTS user (username VARCHAR(20) NOT NULL PRIMARY KEY, password VARCHAR(15) NOT NULL)")

mycursor.execute('''CREATE TABLE IF NOT EXISTS cars (
    car_id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    color VARCHAR(30) NOT NULL,
    price INT NOT NULL,
    fuel_type VARCHAR(20) NOT NULL,
    engine VARCHAR(50),
    seating_capacity INT,
    mileage VARCHAR(20),
    stock INT DEFAULT 1
);''')

mycursor.execute('''CREATE TABLE IF NOT EXISTS booking (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    car_id INT NOT NULL,
    booking_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    price INT NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending'
);''')

mycursor.execute('''CREATE TABLE IF NOT EXISTS testdrive (
    testdrive_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    car_id INT NOT NULL,
    drive_date DATE NOT NULL,
    drive_time VARCHAR(20),
    status VARCHAR(20) DEFAULT 'Pending'
);''')

mycursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    role VARCHAR(10) NOT NULL,
    login_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);''')

mycursor.execute('''CREATE TABLE IF NOT EXISTS car_sold (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    car_id INT NOT NULL,
    username VARCHAR(20) NOT NULL,
    booking_id INT NOT NULL,
    sold_price INT NOT NULL,
    sold_date DATETIME DEFAULT CURRENT_TIMESTAMP
);''')


mydb.commit()



#main program

print(' '*40,'Welcome  TO')

print(' '*39,'Techno Motors \n')



#user

def user():
    
    print('''1. View All Cars  
2. Search Cars    
3. Book Test Drive    
4. Book a Car  
5. View My Bookings
6. Test Drive Status
7. Logout''')

    user_choice=int(input('Choose any service'))
    
    if user_choice == 1:

        print("Car ID | Brand | Model | Color | Price | Fuel Type | Engine | Seating Capacity | Mileage | Stock")
        
        mycursor.execute('Select * from cars;')
        
        car_details = mycursor.fetchall()
        
        for i in car_details:
            
            print(i,'\n')

        user()


    elif user_choice == 2:
        
        brand1 = str(input('Enter the brand name'))
        
        model1 = str(input('Enter the model of car'))
        
        min_price = int(input('Enter your minimum budget'))
        
        max_price = int(input('Enter your maximum budget'))
        
        mycursor.execute("SELECT * FROM cars WHERE brand LIKE %s AND model LIKE %s AND price BETWEEN %s AND %s",
(f"%{brand1}%", f"%{model1}%", min_price, max_price))
        
        search_car = mycursor.fetchall()

        if search_car == []:

            print('Sorry Car is not available\n')

        else:

            print("Car ID | Brand | Model | Color | Price | Fuel Type | Engine | Seating Capacity | Mileage | Stock")

            for i in search_car:

                print(i,'\n')

        user()


    elif user_choice == 3:
        
        print("Kindly verify the full specifications and features of the car prior to booking a test drive. This will help you make an informed selection.")
        
        car_id = int(input("Please enter the Car ID of the vehicle for which you would like to book a test drive."))
        
        drive_date = str(input("Please enter the date on which you would like to schedule the test drive."))
        
        drive_time = str(input("Please enter the time at which you would like to schedule the test drive."))
        
        mycursor.execute("INSERT INTO testdrive (username, car_id, drive_date, drive_time, status) VALUES (%s, %s, %s, %s, %s)",
(username, car_id, drive_date, drive_time, "Pending"))

        print('''Wait for Staff to review your Test drive request.
Kindly check Test drive Status after sometime to make sure your drive is approved or denied''')

        mydb.commit()

        user()


    elif user_choice == 4:

        print("Kindly verify the full specifications and features of the car prior to booking a car. This will help you make an informed selection.")

        car_id = int(input("Please enter the Car ID of the vehicle which you would like to book."))

        mycursor.execute("SELECT price FROM cars WHERE car_id = %s", (car_id,))

        price = mycursor.fetchone()

        if price is None:

            print("Invalid Car ID.")

            user()

        sold_price = price[0]

        mycursor.execute("INSERT INTO booking (username, car_id, price, status) VALUES (%s, %s, %s, %s)",
(username, car_id,sold_price, "Pending"))

        print('''Wait for Staff to review your Car Booking request.
Kindly check View my Bookings after sometime to make sure your car is approved or denied for sale''')
        
        mydb.commit()

        user()


    elif user_choice == 5:

        mycursor.execute("SELECT * FROM booking WHERE username = %s", (username,))

        booking_detail = mycursor.fetchall()

        if booking_detail == []:
            
            print('Kindly book a Car first')

        else:

            for i in booking_detail:
                
                print(i,'\n')

        user()


    elif user_choice == 6:

        mycursor.execute("SELECT * FROM testdrive WHERE username = %s", (username,))

        testdrive_detail = mycursor.fetchall()

        if testdrive_detail == []:

            print('Kindly book a test drive first')

        else:

            for i in testdrive_detail:

                print(i,'\n')

        user()


    elif user_choice == 7:

        print("Logged out.")

        current_user = None
        
        login()


    else:

        print('Invalid Input')

        user()



#Admin

def Admin():

    print('''1.View All Cars
2.Approve or Deny Test Drive
3.Approve or Deny Car Booking
4.View Approved Test Drives
5.View Approved Car Bookings
6.View Clients History 
7.Update Car stock or Price
8.View Cars Sold
9.Add more Cars
10.Logout
''')

    admin_choice = int(input("Enter option number: "))

    if admin_choice == 1:

        print("Car ID | Brand | Model | Color | Price | Fuel Type | Engine | Seating Capacity | Mileage | Stock")

        mycursor.execute('Select * from cars;')
        
        car_details = mycursor.fetchall()
        
        for i in car_details:
            
            print(i,'\n')

        Admin()


    elif admin_choice == 2:

        print("Test Drive ID | Username | Car ID | Drive Date | Drive Time | Status")

        mycursor.execute('Select * from testdrive where status = "Pending";')

        testdrive_data = mycursor.fetchall()

        if testdrive_data == []:

            print('No Data found')

        else:

            for i in testdrive_data:

                print(i)

            print()

            print('''1.Approve
2.Deny\n''')

            test_approve_deny = int(input('Choose option number:\n'))

            if test_approve_deny == 1:

                testdrive_id = int(input('Enter the Test Drive ID you want to Approve'))

                mycursor.execute("UPDATE testdrive SET status = 'Approved' WHERE testdrive_id = %s",(testdrive_id,))

                mydb.commit()

                print('Successfully Approved\n')


            elif test_approve_deny == 2:

                testdrive_id = int(input('Enter the Test Drive ID you want to Deny'))

                mycursor.execute("UPDATE testdrive SET status = 'Denied' WHERE testdrive_id = %s",(testdrive_id,))

                mydb.commit()

                print('Successfully Denied \n')

        Admin()


    elif admin_choice == 3:

        print("Booking ID | Username | Car ID | Booking Date | Status")

        mycursor.execute('Select * from booking where status = "Pending"')

        booking_data = mycursor.fetchall()

        if booking_data == []:

            print('No Data found')

        else:

            for i in booking_data:

                print(i)

            print()

            print('''1.Approve
2.Deny\n''')

            book_approve_deny = int(input('Choose option number:\n'))

            if book_approve_deny == 1:

                booking_id = int(input('Enter the Booking ID you want to Approve'))

                mycursor.execute("UPDATE booking SET status = 'Approved' WHERE booking_id = %s",(booking_id,))

                mycursor.execute('Select car_id from booking where booking_id = %s',(booking_id,))

                car_id_data = mycursor.fetchall()

                for i in car_id_data:

                    mycursor.execute('UPDATE cars SET stock = stock - 1 where car_id = %s',(i))

                mycursor.execute('Select car_id,username,booking_id,price from booking where booking_id = %s',(booking_id,))

                car_sold_data = mycursor.fetchall()

                car_id, username, booking_id, sold_price = car_sold_data[0]


                mycursor.execute('insert into car_sold (car_id,username,booking_id,sold_price)values(%s,%s,%s,%s)',
(car_id,username,booking_id,sold_price))

                mydb.commit()

                print('Successfully Approved\n')

            elif book_approve_deny == 2:

                booking_id = int(input('Enter the Booking ID you want to Deny'))

                mycursor.execute("UPDATE booking SET status = 'Deny' WHERE booking_id = %s",(booking_id,))

                mydb.commit()

                print('Successfully Denied\n')

        Admin()

        


    elif admin_choice == 4:

        print("Test Drive ID | Username | Car ID | Drive Date | Drive Time | Status")

        mycursor.execute('Select * from testdrive where status = "Approved";')

        testdrive_data_approved = mycursor.fetchall()

        for i in testdrive_data_approved:

            print(i)

        Admin()


    elif admin_choice == 5:

        print("Booking ID | Username | Car ID | Booking Date | Status")

        mycursor.execute('Select * from booking where status = "Approved"')

        booking_data_approved = mycursor.fetchall()

        for i in booking_data_approved:

            print(i)

        Admin()


    elif admin_choice == 6:

        mycursor.execute('Select username from user')

        username_data = mycursor.fetchall()

        for i in username_data:

            print(i)

        user_history = str(input('Enter the username whose History you want to review'))

        print()

        print('Booked Cars')

        print("Booking ID | Username | Car ID | Booking Date | Status")

        mycursor.execute('Select * from booking where username = %s',(user_history,))

        booking_data01 = mycursor.fetchall()

        for i in booking_data01:

            print(i)

        print()

        print('Booked Test Drive')

        print("Test Drive ID | Username | Car ID | Drive Date | Drive Time | Status")

        mycursor.execute('Select * from testdrive where username = %s',(user_history,))

        testdrive_data01 = mycursor.fetchall()

        for i in testdrive_data01:

            print(i)

        print()

        print('Logged in sessions')

        print("Session ID | Username | Role | Login Time")

        mycursor.execute('Select * from sessions where username = %s',(user_history,))

        session_data_user = mycursor.fetchall()

        for i in session_data_user:

            print(i)

        Admin()


    elif admin_choice == 7:

        print('''1.Update Car Stock
2.Update Car Price
3.Update Car Stock and Price both''')

        update_stock_print = int(input('Choose option number'))

        if update_stock_print == 1:

            car_id = int(input('Enter the Car ID of the car you want to Update stock of'))

            stock = int(input('Enter the no. of Cars you want to add in existing stock'))

            mycursor.execute("UPDATE cars SET stock = stock + %s WHERE car_id = %s",(stock, car_id))

            mydb.commit()

            print('Stock Updated')

        elif update_stock_print == 2:

            car_id = int(input('Enter the Car ID of the car you want to Update Price of'))

            Price = int(input('Enter the new price of car'))

            mycursor.execute("Update cars SET Price = %s where car_id = %s",(Price,car_id))

            mydb.commit()

            print('Stock Updated')

        elif update_stock_print == 3:

            car_id = int(input('Enter the Car ID of the car you want to Update stock of'))

            Price = int(input('Enter the new price of car'))

            stock = int(input('Enter the no. of Cars you want to add in existing stock'))

            mycursor.execute("Update cars SET Price = %s,stock = stock + %s where car_id = %s",(Price,stock,car_id))

            mydb.commit()

            print('Stock and Price Updated')

        else:

            print('Invalid Input')

        Admin()


    elif admin_choice == 8:

        print('Sale ID | Car ID | Username | Booking ID | Sold Price | Sold date')

        mycursor.execute('Select * from car_sold')

        car_sold_data = mycursor.fetchall()

        for i in car_sold_data:

            print(i)

        Admin()


    elif admin_choice == 9:

        no_of_entries = int(input('Enter the no. of Different Cars you want to add'))

        for i in range(no_of_entries):

            brand = str(input('Enter Brand name of Car'))

            model = str(input('Enter Model of Car'))

            color = str(input('Enter Colour of Car'))

            price = int(input('Enter Price of Car'))

            fuel = str(input('Enter Fuel Type of Car'))

            engine = str(input('Enter Engine Type of Car'))

            seating_capacity = int(input('Enter Seating Capacity of The Car'))

            mileage = str(input('Enter Mileage of Car'))

            stock = int(input('Enter The availabe stock of Car'))

            mycursor.execute('''INSERT INTO cars (brand, model, color, price, fuel_type, engine, seating_capacity, mileage, stock)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',(brand, model, color, price, fuel, engine, seating_capacity, mileage, stock))

            mydb.commit()

            print('Successfully Added the Car in stock')

        Admin()
        

    elif admin_choice == 10:

        print("Logged out.")

        current_user = None
        
        login()

    else:

        print('Invalid Input')

        Admin()



#login system
        
def login():
    
    signin_up = int(input('''1.Login
2.Register:'''))
    
    print()

    if signin_up == 1:
        
        Login_category = int(input('''1.User Login
2.Admin Login
Choose Any 1 type of login:'''))
        
        print()
        
        if Login_category == 1:
            
            global username
            
            username = str(input('Enter the username:'))
            
            password = str(input('Enter the password'))
            
            mycursor.execute('Select * from user;')
            
            user_detail = mycursor.fetchall()
            
            if (username,password) in user_detail:

                current_user = username

                mycursor.execute("INSERT INTO sessions (username, role) VALUES (%s, %s)",(current_user, "user"))

                mydb.commit()
                
                user()

                
            else:

                print('Kindly ensure that your username and password are correct. \nIf you have not registered yet, please register before proceeding.')

                login()
            

        elif Login_category == 2:
            
            username = str(input('Enter the username:'))
            
            password = str(input('Enter the password'))
            
            mycursor.execute('Select * from Admin;')
            
            Admin_detail = mycursor.fetchall()
            
            if (username,password) in Admin_detail:

                current_user = username

                mycursor.execute("INSERT INTO sessions (username, role) VALUES (%s, %s)",(current_user, "Admin"))

                mydb.commit()
                
                Admin()
                
            else:
                
                print('Kindly ensure that your username and password are correct.')

                login()


        else:
            
            print('Invalid input')
            
            login()
            
    elif signin_up == 2:
        
        username = str(input('Create a username in not more then 20 character'))
        
        password = str(input('Create a password in not more then 15 character'))
        
        mycursor.execute("INSERT INTO user(username, password) VALUES (%s, %s)",(username, password))
        
        print("Account created successfully. Please log in to continue.")

        login()


    else:

        print('Invalid Input')

        login()




login()







        

