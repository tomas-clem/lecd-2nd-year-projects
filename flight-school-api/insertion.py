import pandas as pd
import psycopg2
from datetime import datetime
import random

config = pd.read_json('config.json', typ='series')

def db_connection():

    db = psycopg2.connect(
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port'],
        database=config['database']
    )

    return db


conn = db_connection()
cur = conn.cursor()


def query(connection, statement, values=None):
    cur = connection.cursor()
    try:
        cur.execute(statement, values)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        connection.rollback()
        cur.close()


drop_tables = """DROP TABLE IF EXISTS pilot CASCADE;
DROP TABLE IF EXISTS aircraft CASCADE;
DROP TABLE IF EXISTS booking CASCADE;
DROP TABLE IF EXISTS airport CASCADE;
DROP TABLE IF EXISTS logbook CASCADE;
DROP TABLE IF EXISTS aircraft_type CASCADE;
DROP TABLE IF EXISTS pilot_type CASCADE;
DROP TABLE IF EXISTS booking_type CASCADE;
DROP TABLE IF EXISTS flight_license CASCADE;
DROP TABLE IF EXISTS medical_certificate CASCADE;
DROP TABLE IF EXISTS aircraft_ratings CASCADE; """
query(conn, drop_tables)

create_tables = """CREATE TABLE logbook (
	id			 BIGSERIAL,
	flight_start		 TIMESTAMP NOT NULL,
	flight_end		 TIMESTAMP NOT NULL,
	landings		 BIGINT NOT NULL,
	passengers		 BIGINT NOT NULL,
	airport_airport_code	 BIGINT NOT NULL,
	airport_airport_code1 BIGINT NOT NULL,
	booking_id		 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE pilot (
	id		 BIGINT,
	first_name	 VARCHAR(512) NOT NULL,
	last_name	 VARCHAR(512) NOT NULL,
	address	 VARCHAR(512) NOT NULL,
	home_airport	 VARCHAR(512) NOT NULL,
	pilot_type_id INTEGER NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE aircraft (
	aircraft_id		 BIGSERIAL,
	tail_number		 VARCHAR(512) NOT NULL,
	serial_number	 BIGINT NOT NULL,
	color		 VARCHAR(512) NOT NULL,
	airport_airport_code BIGINT NOT NULL,
	aircraft_type_type	 VARCHAR(512) NOT NULL,
	PRIMARY KEY(aircraft_id)
);

CREATE TABLE booking (
	id			 BIGSERIAL,
	book_start		 TIMESTAMP NOT NULL,
	book_end		 TIMESTAMP NOT NULL,
	booking_type_id	 BIGINT NOT NULL,
	aircraft_aircraft_id BIGINT NOT NULL,
	pilot_id		 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE medical_certificate (
	id	 BIGINT,
	start_date TIMESTAMP NOT NULL,
	end_date	 TIMESTAMP NOT NULL,
	pilot_id	 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE flight_license (
	id	 BIGINT,
	start_date TIMESTAMP NOT NULL,
	end_date	 TIMESTAMP NOT NULL,
	license	 VARCHAR(512) NOT NULL,
	pilot_id	 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE aircraft_ratings (
	id		 BIGSERIAL,
	start_date	 TIMESTAMP NOT NULL,
	end_date		 TIMESTAMP NOT NULL,
	aircraft_type_type VARCHAR(512) NOT NULL,
	pilot_id		 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE pilot_type (
	type VARCHAR(512) NOT NULL,
	id	 INTEGER NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE aircraft_type (
	type VARCHAR(512),
	PRIMARY KEY(type)
);

CREATE TABLE booking_type (
	id	 BIGINT,
	type VARCHAR(512),
	PRIMARY KEY(id)
);

CREATE TABLE airport (
	airport_code BIGINT,
	airport_name VARCHAR(512),
	home	 VARCHAR(512),
	PRIMARY KEY(airport_code)
);

ALTER TABLE logbook ADD CONSTRAINT logbook_fk1 FOREIGN KEY (airport_airport_code) REFERENCES airport(airport_code);
ALTER TABLE logbook ADD CONSTRAINT logbook_fk2 FOREIGN KEY (airport_airport_code1) REFERENCES airport(airport_code);
ALTER TABLE logbook ADD CONSTRAINT logbook_fk3 FOREIGN KEY (booking_id) REFERENCES booking(id);
ALTER TABLE pilot ADD CONSTRAINT pilot_fk1 FOREIGN KEY (pilot_type_id) REFERENCES pilot_type(id);
ALTER TABLE aircraft ADD CONSTRAINT aircraft_fk1 FOREIGN KEY (airport_airport_code) REFERENCES airport(airport_code);
ALTER TABLE aircraft ADD CONSTRAINT aircraft_fk2 FOREIGN KEY (aircraft_type_type) REFERENCES aircraft_type(type);
ALTER TABLE booking ADD CONSTRAINT booking_fk1 FOREIGN KEY (booking_type_id) REFERENCES booking_type(id);
ALTER TABLE booking ADD CONSTRAINT booking_fk2 FOREIGN KEY (aircraft_aircraft_id) REFERENCES aircraft(aircraft_id);
ALTER TABLE booking ADD CONSTRAINT booking_fk3 FOREIGN KEY (pilot_id) REFERENCES pilot(id);
ALTER TABLE medical_certificate ADD CONSTRAINT medical_certificate_fk1 FOREIGN KEY (pilot_id) REFERENCES pilot(id);
ALTER TABLE flight_license ADD CONSTRAINT flight_license_fk1 FOREIGN KEY (pilot_id) REFERENCES pilot(id);
ALTER TABLE aircraft_ratings ADD CONSTRAINT aircraft_ratings_fk1 FOREIGN KEY (aircraft_type_type) REFERENCES aircraft_type(type);
ALTER TABLE aircraft_ratings ADD CONSTRAINT aircraft_ratings_fk2 FOREIGN KEY (pilot_id) REFERENCES pilot(id);"""
query(conn, create_tables)

booking_types = pd.read_csv('tabelas/Booking_types.csv', delimiter=';')
for row in booking_types.values:
    query(conn, 'INSERT INTO booking_type (id, type) values(%s,%s)', (row[0], row[1],))

pilot_types = pd.read_csv('tabelas/Pilot_types.csv', delimiter=';')
for row in pilot_types.values:
    query(conn, 'INSERT INTO pilot_type (id,type) values(%s,%s)', (row[0],row[1],))

aircraft_types = pd.read_csv('tabelas/Aircraft_types.csv', delimiter=';')
for row in aircraft_types.values:
    query(conn, 'INSERT INTO aircraft_type (type) values (%s)', (row[0],))

airports = pd.read_csv('tabelas/Airports.csv', delimiter=';')
for row in airports.values:
    query(conn, 'INSERT INTO airport (airport_code, airport_name) values (%s,%s)', (row[0], row[2],))

aircrafts = pd.read_csv('tabelas/Aircrafts.csv', delimiter=';')
for row in aircrafts.values:
    query(conn, 'INSERT INTO aircraft (tail_number,serial_number,color, airport_airport_code, aircraft_type_type) values (%s,%s,%s,%s,%s)',(row[1],row[2],row[4],row[5],row[3],))

pilots = pd.read_csv('tabelas/Pilots.csv', delimiter=';')
address = ['Rua Ferreira Borges','Estrada da Beira','Rua do Quebra Costas','Avenida Sá da Bandeira','Rua do Arco de Almedina', 'Rua do Brasil', 'Rua Carlos Seixas','Largo da Portagem','Avenida Fernão Magalhães','Rua do Tunel','Rua do Ferrolho']
i = 0
for row in pilots.values:
    query(conn,'INSERT INTO pilot (id, first_name, last_name, address, home_airport, pilot_type_id) values(%s,%s,'
               '%s,%s,%s,%s)', (row[0], row[1], row[2], address[random.randint(0,10)], str(random.randint(1,26)),
                                row[9],))
    query(conn, 'INSERT INTO medical_certificate (id, start_date, end_date, pilot_id) values (%s,%s,%s,%s)',
          (i, datetime.strptime(row[7], '%d-%m-%Y'), datetime.strptime(row[8], '%d-%m-%Y'), row[0],))
    query(conn, 'INSERT INTO flight_license (id, start_date, end_date, license, pilot_id) values (%s,%s,%s,%s,%s)',
          (i, datetime.strptime(row[4], '%d-%m-%Y'), datetime.strptime(row[5], '%d-%m-%Y'), row[3], row[0],))
    i+=1

aircraft_ratings = pd.read_csv('tabelas/Aircraft_Ratings.csv', delimiter=';')
i = 1
for row in aircraft_ratings.values:
    query(conn,
          'INSERT INTO aircraft_ratings (id, start_date, end_date, aircraft_type_type, pilot_id) values (%s,%s,%s,%s,%s)',
          (i, datetime.strptime(row[2], '%d-%m-%Y'), datetime.strptime(row[3], '%d-%m-%Y'), row[1], row[0],))
    i += 1

bookings = pd.read_csv('tabelas/Bookings.csv', delimiter=';')
for row in bookings.values:
    query(conn, 'INSERT INTO booking (book_start,book_end,booking_type_id, aircraft_aircraft_id, pilot_id) values (%s,%s,%s,%s,%s)', (datetime.strptime(row[1], '%d-%m-%Y %H:%M'), datetime.strptime(row[2], '%d-%m-%Y %H:%M'),row[3],row[5],row[4],))

log_book = pd.read_csv('tabelas/Log_Book.csv', delimiter=';')
for row in log_book.values:
    query(conn, 'INSERT INTO logbook (flight_start,flight_end,landings,passengers,airport_airport_code,airport_airport_code1, booking_id) values (%s,%s,%s,%s,%s,%s,%s)', (datetime.strptime(row[4], '%d-%m-%Y %H:%M'),datetime.strptime(row[5], '%d-%m-%Y %H:%M'),row[7],random.randint(2,15),row[1],row[2], row[8]))


