# Booking System (Concert Ticket)
import pymysql.cursors

def connect_sql():
    connection = pymysql.connect(
    host = 'YOUR_HOST',
    port = 8888,
    user = 'USER_NAME',
    password = 'PASSWORD',
    db = 'DATABASE',
    charset = 'utf8',
    cursorclass = pymysql.cursors.DictCursor,
    autocommit = True)
    return connection

connection = connect_sql()


# no.1 Create Tables
try:

# Q: how to clear tables? error - Unknown table
    with connection.cursor() as cursor:
        sql_comm = "drop table if exists Book cascade"
        cursor.execute(sql_comm)

        sql_comm = "drop table if exists Audience cascade;"
        cursor.execute(sql_comm)

        sql_comm = "drop table if exists Building cascade;"
        cursor.execute(sql_comm)

        sql_comm = "drop table if exists Performances cascade;"
        cursor.execute(sql_comm)

        sql_comm = "drop table if exists Buildings cascade;"
        cursor.execute(sql_comm)

    connection = connect_sql()
    with connection.cursor() as cursor:
        sql_comm = "create table Audience (" \
                   "aud_id varchar(10) AUTO_INCREMENT primary key," \
                   "aud_name varchar(200)," \
                   "gender varchar(1) check(gender = 'M' or gender = 'F')," \
                   "age int, check( 0 <= age <= 999))"
        cursor.execute(sql_comm)

        sql_comm = "create table Buildings (" \
                   "building_id varchar(5) AUTO_INCREMENT primary key," \
                   "building_name varchar(200)," \
                   "building_cap int default 0," \
                   "building_loc varchar(200)," \
                   "building_asgn int default 0 check(building_asgn =1 or building_asgn =0))"
        cursor.execute(sql_comm)

        sql_comm = "create table Building (" \
                   "building_id varchar(5)," \
                   "seat_number int," \
                   "constraint building_pk primary key(building_id, seat_number)," \
                   "constraint fk_buildings foreign key(building_id) references Buildings(building_id) " \
                   "on delete cascade on update cascade)"
        cursor.execute(sql_comm)

        sql_comm = "create table Performances (" \
                   "perf_id varchar(10) AUTO_INCREMENT primary key," \
                   "perf_name varchar(200)," \
                   "perf_type varchar(10)," \
                   "price int, check(0 <= price <= 1000000)," \
                   "booked int default 0," \
                   "building_id varchar(5) default null," \
                   "constraint fk_perf foreign key(building_id) references Buildings(building_id)" \
                   "on delete cascade on update cascade)"
        cursor.execute(sql_comm)

        sql_comm = "create table Book (" \
                   "booking_id varchar(10) primary key," \
                   "aud_id varchar(10) not null AUTO_INCREMENT," \
                   "perf_id varchar(10) not null," \
                   "building_id varchar(5) not null," \
                   "seat_number varchar(4) not null," \
                   "constraint fk_book_aud foreign key(aud_id) references Audience(aud_id) " \
                   "on delete cascade on update cascade," \
                   "constraint fk_book_per foreign key(perf_id) references Performances(perf_id) " \
                   "on delete cascade on update cascade," \
                   "constraint fk_book_bui foreign key(building_id, seat_number) references Building(building_id, seat_number)" \
                   "on delete cascade on update cascade)"
        cursor.execute(sql_comm)
    connection = connect_sql()
    with connection.cursor() as cursor:
        cursor.execute("show tables")
        print(cursor.fetchall(), "\nTables Are Successfully Created")

except:
    print("ERROR: Tables Failed to Be Created")
finally: pass


# no.2 Insert Data
connection = connect_sql()
with connection.cursor() as cursor:
    #Audience
    sql_comm = "insert into Audience(aud_name, gender, age) " \
               "values ('Yoon Jaeyeun', 'M', 30);"
    cursor.execute(sql_comm)
    sql_comm = "insert into Audience(aud_name, gender, age) " \
               "values ('Kim Taeuk', 'M', 27);"
    cursor.execute(sql_comm)
    sql_comm = "insert into Audience(aud_name, gender, age) " \
               "values ('Ahn Chaemin', 'F', 25);"
    cursor.execute(sql_comm)

    #Buildings
    sql_comm = "insert into Buildings(building_name, building_loc) " \
               "values ('Seoul Arts Center', 'Seoul');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Buildings(building_name, building_loc) " \
               "values ('Grand Peace Palace', 'Seoul');"
    cursor.execute(sql_comm)

    #Building (seat_numbers)
    sql_comm = "insert into Building(building_id, seat_number)" \
               "values ('1', 'A001');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Building(building_id, seat_number)" \
               "values ('1', 'A002');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Building(building_id, seat_number)" \
               "values ('1', 'A003');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Building(building_id, seat_number)" \
               "values ('1', 'B001');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Building(building_id, seat_number)" \
               "values ('1', 'B002');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Building(building_id, seat_number)" \
               "values ('1', 'B003');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Building(building_id, seat_number)" \
               "values ('2', 'A001');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Building(building_id, seat_number)" \
               "values ('2', 'A002');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Building(building_id, seat_number)" \
               "values ('2', 'A003');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Building(building_id, seat_number)" \
               "values ('2', 'B001');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Building(building_id, seat_number)" \
               "values ('2', 'B002');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Building(building_id, seat_number)" \
               "values ('2', 'B003');"
    cursor.execute(sql_comm)

    #Performances
    sql_comm = "insert into Performances(perf_name, perf_type, price, building_id)" \
               "values ('Coldplay Concert', 'Concert', 100000, '1');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Performances(perf_name, perf_type, price, building_id)" \
               "values ('Jekyll & Hyde', 'Musical', 70000, '2');"
    cursor.execute(sql_comm)

    #Book
    sql_comm = "insert into Book(aud_id, perf_id, building_id, seat_number)" \
               "values ('1', '1', '1', 'A001');"
    cursor.execute(sql_comm)
    sql_comm = "insert into Book(aud_id, perf_id, building_id, seat_number)" \
               "values ('1', '1', '2', 'A002');"
    cursor.execute(sql_comm)

    # count building capacity, assigned performance, and performance bookings
    # 1) building_cap
def count_cap():
    connection = connect_sql()
    with connection.cursor() as cursor:
        cursor.execute("select distinct building_id from Building")
        result = cursor.fetchall()
        building_ids = []
        for i in range(len(result)):
            building_ids += list(result[i].values())
        for i in range(len(building_ids)):
            sql_comm = "update Buildings " \
                       "set building_cap = (select count(seat_number) " \
                       "from Building where building_id = \'%s\') " \
                       "where building_id = \'%s\'" %(building_ids[i], building_ids[i])
            cursor.execute(sql_comm)

# 2) building_asgn
def count_asgn(building_id):
    connection = connect_sql()
    with connection.cursor() as cursor:
        cursor.execute("select count(building_id) from Performances where building_id = \'%s\';"%building_id)

# 3) Performances booked
def count_booked():
    connection = connect_sql()
    with connection.cursor() as cursor:
        cursor.execute("select perf_id, count(booking_id) from Book group by perf_id")
        result = cursor.fetchall()
        for i in range(len(result)):
            sql_comm = "update Performances " \
                       "set booked = %d "\
                       "where perf_id = \'%s\'" %(result[i]['count(booking_id)'], result[i]['perf_id'])
            cursor.execute(sql_comm)

print("Data are Successfully Inserted")


# no.3 Application Classes Definitions
#id_generator
# import random
# def id_gen(num):
#     id = ''
#     for i in range(num):
#         id += str(random.randrange(10))
#     return id

#id_autoincrement

class Insert(object):
    def __init__(self):
        self.sql_comm_insert = "insert into "

    def into_buildings(self, building_name, building_cap, building_loc):
        while True:
            connection = connect_sql()
            # with connection.cursor() as cursor:
            #     sql_comm = "select building_id from Buildings"
            #     cursor.execute(sql_comm)
            #     result = cursor.fetchall()
            # building_ids= []
            # for i in range(len(result)):
            #     building_ids += result[i]['building_id']
            # while True:
                # building_id = id_gen(5)
                # if building_id not in building_ids:
                #     break
            if not (type(building_name) == str and len(building_name) <= 200):
                print("building_name must be shorter than or equal to 200 letters")
                break
            elif not (type(building_loc) == str and len(building_loc) <= 200):
                print("building_loc must be shorter than or equal to 200 letters")
                break
            else:
                connection = connect_sql()
                with connection.cursor() as cursor:
                    sql_comm = self.sql_comm_insert + "Buildings(building_name, building_cap, building_loc) values(" \
                           "\'%s\', \'%s\', \'%s\')" %(building_name, building_cap, building_loc)
                    cursor.execute(sql_comm)
                break
        return building_id

    def into_performances(self, perf_name, perf_type, price):
        while True:
            connection = connect_sql()
            with connection.cursor() as cursor:
                sql_comm = "select perf_id from Performances"
                cursor.execute(sql_comm)
                result = cursor.fetchall()
            perf_ids= []
            for i in range(len(result)):
                perf_ids += result[i]['perf_id']
            while True:
                perf_id = id_gen(10)
                if perf_id not in perf_ids:
                    break
            if not (type(perf_id) == str and len(perf_id) == 10 and perf_id.isdigit()):
                print("perf_id must be a 10 digit-long string")
                break
            elif not(type(perf_name) == str and len(perf_name) <= 200):
                print("perf_name must be shorter than or equal to 200 letters")
                break
            elif not (type(perf_type) == str and len(perf_type) <= 200):
                print("perf_type must be shorter than or equal to 200 letters")
                break
            elif not (type(price) == int and 0 <= price <= 1000000):
                print("price must be between 0 ~ 1,000,000")
                break
            else:
                connection = connect_sql()
                with connection.cursor() as cursor:
                    sql_comm = self.sql_comm_insert + \
                               "Performances(perf_id, perf_name, perf_type, price) values(" \
                       "\'%s\', \'%s\', \'%s\', \'%d\')" %(perf_id, perf_name, perf_type, price)
                    cursor.execute(sql_comm)
                break
        return perf_id

    def into_audience(self, aud_name, gender, age):
        while True:
            connection = connect_sql()
            with connection.cursor() as cursor:
                sql_comm = "select aud_id from Audience"
                cursor.execute(sql_comm)
                result = cursor.fetchall()
            aud_ids= []
            for i in range(len(result)):
                aud_ids += result[i]['aud_id']
            while True:
                aud_id = id_gen(10)
                if aud_id not in aud_ids:
                    break
            if not (type(aud_id) == str and len(aud_id) == 10 and aud_id.isdigit()):
                print("aud_id must be a 10 digit-long string")
                break
            elif not (type(aud_name) == str and len(aud_name) <= 200):
                print("aud_name must be shorter than or equal to 200 letters")
                break
            elif not (gender == 'M' or gender == 'F'):
                print("gender must be either 'M' or 'F'")
                break
            elif not (type(age) == int and 0 <= age <= 999):
                print("age must be between 0 ~ 999")
                break
            else:
                connection = connect_sql()
                with connection.cursor() as cursor:
                    sql_comm = self.sql_comm_insert + "Audience(aud_id, aud_name, gender, age) values(" \
                           "\'%s\', \'%s\', \'%s\', \'%d\')" %(aud_id, aud_name, gender, age)
                    cursor.execute(sql_comm)
                break
        return aud_id

    def into_building(self, building_id, seat_number):
        while True:
            if not (type(building_id) == str and len(building_id) == 5 and building_id.isdigit()):
                print("building_id must be a 5 digit-long string")
                break
            elif not (type(seat_number) == str and len(seat_number) <= 4):
                print("seat_number must be shorter or equal to 4 letters")
                break
            else:
                connection = connect_sql()
                with connection.cursor() as cursor:
                    sql_comm = self.sql_comm_insert + "Building(building_id, seat_number) values(" \
                                                      "\'%s\', \'%s\')" % (building_id, seat_number)
                    cursor.execute(sql_comm)
                count_cap()
                break

    def into_book(self, aud_id, perf_id, seat_number, building_id):
        connection = connect_sql()
        with connection.cursor() as cursor:
            sql_comm = "select booking_id from Book"
            cursor.execute(sql_comm)
            result = cursor.fetchall()
        booking_ids= []
        for i in range(len(result)):
            booking_ids += result[i]['booking_id']
        while True:
            booking_id = id_gen(10)
            if booking_id not in booking_ids:
                break
        connection = connect_sql()
        with connection.cursor() as cursor:
            sql_comm = self.sql_comm_insert + "Book(booking_id, aud_id, perf_id, seat_number, building_id) values(" \
                   "\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % (booking_id, aud_id, perf_id, seat_number, building_id)
            cursor.execute(sql_comm)
        count_booked()
        return booking_id



class Delete(object):
    def __init__(self):
        self.sql_comm_del = "delete from "
    def from_buildings(self, building_id):
        while True:
            if not (type(building_id) == str and len(building_id) == 5):
                print("building_id must be a 5-digit-long string")
                break
            else:
                connection = connect_sql()
                with connection.cursor() as cursor:
                    sql_comm = self.sql_comm_del + "Buildings where building_id = %s" %building_id
                    cursor.execute(sql_comm)
                count_asgn(building_id)
                break

    def from_performances(self, perf_id):
        while True:
            if not (type(perf_id) == str and len(perf_id) == 10):
                print("perf_id must be a 10-digit-long string")
                break
            else:
                connection = connect_sql()
                with connection.cursor() as cursor:
                    result = Select('building_id', 'Performances', 'where = perf_id').execute()
                    sql_comm = self.sql_comm_del + "Performances where perf_id = %s"
                    cursor.execute(sql_comm, perf_id)
                count_asgn(result[0]['building_id'])
                break

    def from_audience(self, aud_id):
        while True:
            if not (type(aud_id) == str and len(aud_id) == 10):
                print("aud_id must be a 10-digit-long string")
                break
            else:
                connection = connect_sql()
                with connection.cursor() as cursor:
                    sql_comm = self.sql_comm_del + "Audience where aud_id = %s"
                    cursor.execute(sql_comm, aud_id)
                break

    def from_book(self, booking_id):
        while True:
            if not (type(booking_id) == str and len(booking_id) == 10):
                print("booking_id must be a 10-digit-long string")
                break
            else:
                connection = connect_sql()
                with connection.cursor() as cursor:
                    sql_comm = self.sql_comm_del + "Book where booking_id = %s"
                    cursor.execute(sql_comm, booking_id)
                count_booked()
                break


class Select(object):
    def __init__(self, column_name, Table_name, where = None):
            self.sql_comm = "select %s from %s %s" %(column_name, Table_name,where)
    def execute(self):
        connection = connect_sql()
        with connection.cursor() as cursor:
            cursor.execute(self.sql_comm)
            return cursor.fetchall()


print("Classes and Functions Were Successfully Defined")


    # no.4 Application Execution

if input("Please, press Enter to proceed: ", ):
    pass

line_len_1 = 60
while True:
    connection = connect_sql()
    print("="*line_len_1 + "\n"\
          "1. print all buildings \n"\
          "2. print all performances \n"\
          "3. print all audiences \n"\
          "4. insert a new building \n"\
          "5. remove a building \n"\
          "6. insert a new performance \n"\
          "7. remove a performance \n"\
          "8. insert a new audience \n"\
          "9. remove an audience \n"\
          "10. assign a performance to a building \n"\
          "11. book a performance \n"\
          "12. print all performances assigned to a building \n"\
          "13. print all audiences who booked for a performance \n"\
          "14. print ticket booking status of a performance \n"\
          "15. exit\n"+ "="*line_len_1)

    while True:
        num_choice = input("Select your action: ", )
        if 1 <=  int(num_choice) <= 15:
            print("you chose < %s >." %num_choice)
            break
        else: print("the number you chose, < %s >, is out of range (not 1~15).\n" %num_choice)


    line_len_2 = 70
    if num_choice == '1':
        connection = connect_sql()
        result = Select('*', 'Buildings').execute()
        print("-" * line_len_2 +'\nid'.ljust(8), 'name'.ljust(30), 'location'.ljust(10),
              'capacity'.ljust(10), 'assigned\n' +"-" * line_len_2)
        for i in range(len(result)):
            print(result[i]['building_id'].ljust(7), result[i]['building_name'].ljust(30),
                  result[i]['building_loc'].ljust(10), str(result[i]['building_cap']).ljust(10),
                  str(result[i]['building_asgn']).ljust(10))
        print("-" * line_len_2)


    elif num_choice == '2':
        connection = connect_sql()
        result = Select('*', 'Performances').execute()
        print("-" * line_len_2 +'\nid'.ljust(13), 'name'.ljust(27), 'type'.ljust(10),
              'price'.ljust(10), 'booked\n' +"-" * line_len_2)
        for i in range(len(result)):
            print(result[i]['perf_id'].ljust(12), result[i]['perf_name'].ljust(27),
                  result[i]['perf_type'].ljust(10), str(result[i]['price']).ljust(10),
                  str(result[i]['booked']).ljust(10))
        print("-" * line_len_2)


    elif num_choice == '3':
        connection = connect_sql()
        result = Select('*', 'Audience').execute()
        print("-" * line_len_2 +'\nid'.ljust(13), 'name'.ljust(30), 'gender'.ljust(10),
              'age'.ljust(10), '\n' + "-" * line_len_2)
        for i in range(len(result)):
            print(result[i]['aud_id'].ljust(12), result[i]['aud_name'].ljust(30),
                  result[i]['gender'].ljust(10), str(result[i]['age']).ljust(10))
        print("-" * line_len_2)


    elif num_choice == '4':
        connection = connect_sql()
        while True:
            building_name = input("building name: ",)
            if len(building_name) <= 200:
                break
            print("building name must be under 200 letters")
        while True:
            building_loc = input("building location: ", )
            if len(building_name) <= 200:
                break
            print("building location must be under 200 letters")
        print("building id is automatically created \n",
              "building capacity is automatically calculated when you insert seats data into the building table")
        building_id = Insert().into_buildings(building_name, building_loc)
        seats = []
        while True:
            seat = input("seat numbers of the building: ", )
            if len(seat) > 4:
                print("building location must be under or equal to 4 digit- or letter- long string, e.g., 'A001', 'B123")
            else:
                seats.append(seat)
                print(seat, 'added to', building_id)
            answer = input('continue inserting (press Enter)? if not, type \'exit\'', )
            if answer == 'exit':
                break
        for i in range(len(seats)):
            Insert().into_building(building_id, seats[i])
            count_cap()
        print("A building is successfully inserted:")


    elif num_choice == '5':
        connection = connect_sql()
        temp = Select('building_id', 'Buildings').execute()
        building_ids = list(map(lambda x: temp[x]['building_id'], range(len(temp))))
        while True:
            building_id = input('building id: ',)
            if building_id in building_ids:
                Delete().from_buildings(building_id)
                break
            else:
                print("The building id is not defined. Check the table")


    elif num_choice == '6':
        connection = connect_sql()
        while True:
            perf_name = input("performance name: ",)
            if len(perf_name) <= 200:
                break
            print("performance name must be under 200 letters")
        while True:
            perf_type = input("performance type: ", )
            if len(perf_type) <= 10:
                break
            print("performance type must be under 200 letters")
        while True:
            price = int(input("performance price: ",))
            if 0 <= price <= 1000000:
                break
            print("price must be between 0 and 1,000,000")
        print("performance id is automatically created \n",
              "the number of bookings is automatically calculated whenever a booking is made.\n"
              "building_id allocation is optional: default is None.")
        perf_id = Insert().into_performances(perf_name, perf_type, price)
        print("A performance is successfully created: ", perf_id)

    elif num_choice == '7':
        connection = connect_sql()
        temp = Select('perf_id', 'Performances').execute()
        perf_ids = list(map(lambda x: temp[x]['perf_id'], range(len(temp))))
        while True:
            perf_id = input('performance id: ', )
            if perf_id in perf_ids:
                Delete().from_performances(perf_id)
                break
            else:
                print("The performance id is not defined. Check the table")


    elif num_choice == '8':
        connection = connect_sql()
        while True:
            aud_name = input("audience name: ",)
            if len(aud_name) <= 200:
                break
            print("audience name must be under 200 letters")
        while True:
            gender = input("audience gender (M, F): ", )
            if gender == 'M' or gender == 'F':
                break
            print("audience gender must be either M or F")
        while True:
            age = int(input("audience age: ",))
            if 0 <= age <= 999:
                break
            print("age must be between 0 and 999")
        print("audience id is automatically created.")
        aud_id = Insert().into_audience(aud_name, gender, age)
        print("An audience is successfully created: ", aud_id)


    elif num_choice == '9':
        connection = connect_sql()
        temp = Select('aud_id', 'Audience').execute()
        aud_ids = list(map(lambda x: temp[x]['aud_id'], range(len(temp))))
        while True:
            aud_id = input('audience id: ', )
            if aud_id in aud_ids:
                Delete().from_audience(aud_id)
                break
            else:
                print("The audience id is not defined. Check the table")


    elif num_choice == '10':
        connection = connect_sql()
        temp = Select('building_id', 'Buildings').execute()
        building_ids = list(map(lambda x: temp[x]['building_id'], range(len(temp))))
        while True:
            building_id = input('building id: ',)
            if building_id in building_ids:
                break
            print("The building id is not defined. Check the table")

        temp = Select('perf_id', 'Performances', 'where building_id is null ').execute()
        perf_ids = list(map(lambda x: temp[x]['perf_id'], range(len(temp))))
        while True:
            perf_id = input("performance id: ",)
            if perf_id in perf_ids:
                break
            print("The performance id is either not defined or already assigned. Check the table")
        with connection.cursor() as cursor:
            sql_comm = "update Performances set building_id = \'%s\' where perf_id = \'%s\'"%(building_id, perf_id)
            cursor.execute(sql_comm)
        count_asgn(building_id)
        print("Successfully assigned a performance to a building")


    elif num_choice == '11':
        connection = connect_sql()
        temp = Select('perf_id', 'Performances').execute()
        perf_ids = list(map(lambda x: temp[x]['perf_id'], range(len(temp))))
        while True:
            perf_id = input("performance id: ")
            if perf_id in perf_ids:
                break
            print("The performance is not defined. Check the table")

        temp = Select('aud_id', 'Audience').execute()
        aud_ids = list(map(lambda x: temp[x]['aud_id'], range(len(temp))))
        while True:
            aud_id = input("audience id: ")
            if aud_id in aud_ids:
                break
            print("The audience is not defined. Check the table")

        temp = Select('building_id', 'Performances', 'where perf_id = \'%s\''%perf_id).execute()
        building_id = temp[0]['building_id']
        temp = Select('seat_number', 'Building', 'where building_id = \'%s\'' % building_id).execute()
        seat_numbers = list(map(lambda x: temp[x]['seat_number'], range(len(temp))))

        temp = Select('seat_number', 'Book', 'where perf_id = \'%s\''%perf_id).execute()
        booked_seat_number = list(map(lambda x: temp[x]['seat_number'], range(len(temp))))

        temp = Select('seat_number', 'Building', 'where building_id = \'%s\' and seat_number not in ('
                                                 'select seat_number from Book where perf_id = \'%s\')'%(building_id,perf_id)).execute()
        unbooked_seat_number = list(map(lambda x: temp[x]['seat_number'], range(len(temp))))

        print("Choose a seat from down below. \n", unbooked_seat_number)
        looper = True
        while looper:
            seat_number = input("seat number:  \n#for multiple seats, separate them with a comma")
            seat_number_lst = seat_number.split(',')
            for i in seat_number_lst:
                if i.strip() in seat_numbers:
                    if i.strip() not in booked_seat_number:
                        pass
                    else:
                        print("The seat, \'%s\', is already booked."%i)
                        seat_number_lst.remove(i)
                else:
                    print("The seat number, \'%s\', is not defined. Check the table."%i)
                    seat_number_lst.remove(i)
            looper = False

        if len(seat_number_lst) > 0:
            for i in seat_number_lst:
                booking_id = Insert().into_book(aud_id, perf_id, i.strip(), building_id)
                print("Successfully booked a performance: ", booking_id)


    elif num_choice == '12':
        connection = connect_sql()
        temp = Select('building_id', 'Buildings').execute()
        building_ids = list(map(lambda x: temp[x]['building_id'], range(len(temp))))
        while True:
            building_id = input('building id: ', )
            if building_id in building_ids:
                break
            print("The building id is not defined. Check the table")
        result = Select('*', 'Performances', 'where building_id = \'%s\''%building_id).execute()
        print("-" * line_len_2 + '\nid'.ljust(13), 'name'.ljust(27), 'type'.ljust(10),
              'price'.ljust(10), 'booked\n' + "-" * line_len_2)
        for i in range(len(result)):
            print(result[i]['perf_id'].ljust(12), result[i]['perf_name'].ljust(27),
                  result[i]['perf_type'].ljust(10), str(result[i]['price']).ljust(10),
                  str(result[i]['booked']).ljust(10))
        print("-" * line_len_2)


    elif num_choice == '13':
        connection = connect_sql()
        result = Select('*', 'Audience', 'where aud_id in (select aud_id from Book)').execute()
        print("-" * line_len_2 + '\nid'.ljust(13), 'name'.ljust(30), 'gender'.ljust(10),
              'age'.ljust(10), '\n' + "-" * line_len_2)
        for i in range(len(result)):
            print(result[i]['aud_id'].ljust(12), result[i]['aud_name'].ljust(30),
                  result[i]['gender'].ljust(10), str(result[i]['age']).ljust(10))
        print("-" * line_len_2)


    elif num_choice == '14':
        connection = connect_sql()
        temp = Select('perf_id', 'Performances').execute()
        perf_ids = list(map(lambda x: temp[x]['perf_id'], range(len(temp))))
        while True:
            perf_id = input("performance id: ")
            if perf_id in perf_ids:
                break
            print("The performance is not defined. Check the table")

        with connection.cursor() as cursor:
            sql_comm = "select bd.seat_number, bk.aud_id "\
            "from Building bd left join Book bk on(bd.seat_number = bk.seat_number) "\
            "where bd.building_id = (select building_id from Performances where perf_id = \'%s\')"%perf_id
            cursor.execute(sql_comm)
            result = cursor.fetchall()

        print("-" * line_len_2 + '\nseat number'.ljust(30), 'audience id'.ljust(30),'\n' + "-" * line_len_2)
        for i in range(len(result)):
            print(result[i]['seat_number'].ljust(30), result[i]['aud_id'])
        print("-" * line_len_2)


    elif num_choice == '15':
        print("Bye!")
        break


connection.close()
