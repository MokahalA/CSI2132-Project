CREATE TABLE HotelChain(
	chainName varchar(50),
	numHotels int,
	email varchar(50),
	phoneNumber varchar(15),
	PRIMARY KEY(chainName)
);

CREATE TABLE Hotels(
	locationName varchar(50),
	starRating int,
	numRooms int,
	street varchar(50),
	city varchar(50),
	province varchar(20),
	zip varchar(10),
	email varchar(50),
	phoneNumber varchar(15),
	managerSSN int,
	chainName varchar(50),
	PRIMARY KEY(locationName),
	FOREIGN KEY (chainName) REFERENCES HotelChain(chainName)
);

CREATE TABLE Customer(
	SSN int,
	first_name varchar(50),
	last_name varchar(50),
	street varchar(50),
	city varchar(50),
	province varchar(20),
	zip varchar(10),
	username varchar(50),
	password varchar(50),
	PRIMARY KEY(SSN)
);


CREATE TABLE Employee(
	SSN int,
	first_name varchar(50),
	last_name varchar(50),
	street varchar(50),
	city varchar(50),
	province varchar(20),
	zip varchar(10),
	positions varchar(50),
	username varchar(50),
	password varchar(50),
	PRIMARY KEY(SSN)
);


CREATE TABLE Address(
	address varchar(100),
	chainName varchar(50),
	PRIMARY KEY(address),
	FOREIGN KEY (chainName) REFERENCES HotelChain(chainName)
);


CREATE TABLE Email(
	email varchar(50),
	chainName varchar(50),
	PRIMARY KEY(email),
	FOREIGN KEY (chainName) REFERENCES HotelChain(chainName)
);


CREATE TABLE phoneNumber(
	phoneNumber varchar(25),
	chainName varchar(50),
	PRIMARY KEY(phoneNumber),
	FOREIGN KEY (chainName) REFERENCES HotelChain(chainName)
);