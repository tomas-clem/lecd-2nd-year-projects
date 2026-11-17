CREATE TABLE logbook (
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
ALTER TABLE aircraft_ratings ADD CONSTRAINT aircraft_ratings_fk2 FOREIGN KEY (pilot_id) REFERENCES pilot(id);